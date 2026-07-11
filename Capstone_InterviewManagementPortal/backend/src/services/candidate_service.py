"""
Business logic for Candidate Management module.

Contains:
- create_candidate   → validates fields, saves profile and resume atomically
- list_candidates    → returns paginated candidates
- get_candidate      → returns a single candidate
- update_candidate   → updates editable profile fields
- get_resume_bytes   → returns raw PDF bytes for streaming
- update_status      → HR records the final hiring decision
- get_status_history → returns full status transition history

Status is largely system driven. Scheduling an interview moves a candidate to
INTERVIEW_SCHEDULED, and the status advances to INTERVIEW_COMPLETED on read
once every scheduled interview has taken place. HR only makes the final call.
"""

import logging
import math
from fastapi import UploadFile
from src.core.time_utils import has_interview_passed
from src.enums.candidate_enums import CandidateStatus
from src.models.candidates import Candidate
from src.models.status_history import StatusHistory
from src.repositories.candidate_repository import candidate_repository
from src.repositories.interview_repository import interview_repository
from src.repositories.feedback_repository import feedback_repository
from src.repositories.job_repository import job_repository
from src.schemas.request.candidate_request import CandidateUpdate, CandidateStatusUpdate
from src.core.exceptions import ResourceNotFoundException, ConflictException
from src.schemas.response.candidate_response import CandidateResponse
from src.schemas.response.pagination import PaginatedResponse
from src.enums.interview_enums import RecommendationEnum

logger = logging.getLogger(__name__)

MAX_RESUME_BYTES = 10 * 1024 * 1024
MIN_RESUME_BYTES = 100

SYSTEM_ACTOR = "system"

VALID_TRANSITIONS: dict[str, list[str]] = {
    CandidateStatus.PROFILE_CREATED:     [CandidateStatus.INTERVIEW_SCHEDULED],
    CandidateStatus.INTERVIEW_SCHEDULED: [CandidateStatus.INTERVIEW_COMPLETED],
    CandidateStatus.INTERVIEW_COMPLETED: [
        CandidateStatus.INTERVIEW_SCHEDULED,
        CandidateStatus.SELECTED,
        CandidateStatus.REJECTED,
    ],
    CandidateStatus.SELECTED:            [],
    CandidateStatus.REJECTED:            [],
}

# HR may only record the final decision. Earlier stages are set by the system.
HR_ALLOWED_STATUSES = (CandidateStatus.SELECTED, CandidateStatus.REJECTED)


class CandidateService:
    """Handles business logic for candidate operations."""

    async def create_candidate(
        self,
        first_name: str,
        last_name: str,
        email: str,
        mobile_number: str,
        current_company: str,
        total_experience: float,
        applied_job: str,
        resume: UploadFile,
        created_by: str,
    ) -> Candidate:
        """
        Creates a candidate profile and saves the resume atomically.
        Resume is mandatory, so a candidate without one can never exist.
        """
        if not first_name.strip() or not first_name.strip().replace(" ", "").isalpha():
            raise ConflictException("First name must contain only letters.")

        if not last_name.strip() or not last_name.strip().replace(" ", "").isalpha():
            raise ConflictException("Last name must contain only letters.")

        if not current_company.strip():
            raise ConflictException("Current company is required.")

        if total_experience < 0 or total_experience > 50:
            raise ConflictException("Total experience must be between 0 and 50 years.")

        digits = mobile_number.replace("+", "").replace("-", "").replace(" ", "")
        if not digits.isdigit() or len(digits) != 10:
            raise ConflictException("Mobile number must be exactly 10 digits.")
        mobile_number = digits

        if not await job_repository.find_by_id(applied_job):
            raise ResourceNotFoundException("Applied job not found.")

        if await candidate_repository.email_exists(email.lower()):
            raise ConflictException("A candidate with this email already exists.")

        if await candidate_repository.mobile_exists(mobile_number):
            raise ConflictException(
                "A candidate with this mobile number already exists."
            )

        if resume.content_type != "application/pdf":
            raise ConflictException("Resume must be uploaded in PDF format.")

        resume_bytes = await resume.read()

        if len(resume_bytes) < MIN_RESUME_BYTES:
            raise ConflictException("Resume file appears to be empty or corrupted.")

        if len(resume_bytes) > MAX_RESUME_BYTES:
            raise ConflictException("Resume file must not exceed 10MB.")

        candidate = Candidate(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.lower(),
            mobile_number=mobile_number,
            current_company=current_company.strip(),
            total_experience=total_experience,
            applied_job=applied_job,
            resume_data=resume_bytes,
            status=CandidateStatus.PROFILE_CREATED,
            created_by=created_by,
        )

        created = await candidate_repository.create_candidate(candidate)
        logger.info("Candidate created: %s by %s", created.email, created_by)
        return created

    async def _apply_status_change(
        self,
        candidate_id: str,
        previous_status: CandidateStatus,
        new_status: CandidateStatus,
        changed_by: str,
    ) -> Candidate:
        """
        Writes a status change and records it in the transition history.
        Used by both the system and HR, so it performs no permission checks.
        """
        updated = await candidate_repository.update_status(candidate_id, new_status)
        await candidate_repository.add_status_history(
            candidate_id=candidate_id,
            previous_status=previous_status,
            new_status=new_status,
            changed_by=changed_by,
        )
        logger.info(
            "Candidate %s status: %s → %s by %s",
            candidate_id, previous_status, new_status, changed_by,
        )
        return updated

    async def mark_interview_scheduled(self, candidate_id: str) -> Candidate:
        """
        Moves a candidate to INTERVIEW_SCHEDULED when an interview is booked.
        Safe to call when the candidate is already scheduled.
        """
        candidate = await candidate_repository.find_by_id(candidate_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate not found.")

        if candidate.status == CandidateStatus.INTERVIEW_SCHEDULED:
            return candidate

        return await self._apply_status_change(
            candidate_id,
            candidate.status,
            CandidateStatus.INTERVIEW_SCHEDULED,
            SYSTEM_ACTOR,
        )

    async def _refresh_elapsed_status(self, candidate: Candidate) -> Candidate:
        """
        Advances a candidate to INTERVIEW_COMPLETED once every interview they
        have scheduled has taken place. Called whenever a candidate is read,
        keeping the stored status in step with the passage of time.
        """
        if candidate.status != CandidateStatus.INTERVIEW_SCHEDULED:
            return candidate

        latest = await interview_repository.find_latest_for_candidate(str(candidate.id))
        if not latest:
            return candidate

        if not has_interview_passed(latest.interview_date, latest.interview_time):
            return candidate

        return await self._apply_status_change(
            str(candidate.id),
            candidate.status,
            CandidateStatus.INTERVIEW_COMPLETED,
            SYSTEM_ACTOR,
        )

    async def list_candidates(
        self,
        page: int = 1,
        page_size: int = 10,
        status: CandidateStatus | None = None,
    ) -> PaginatedResponse[CandidateResponse]:
        """Returns a paginated list of candidates with optional status filter."""
        candidates, total = await candidate_repository.find_paginated(
            page, page_size, status
        )

        refreshed = [await self._refresh_elapsed_status(c) for c in candidates]

        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedResponse(
            items=refreshed,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def get_candidate(self, candidate_id: str) -> Candidate:
        """Retrieve a candidate by ID."""
        candidate = await candidate_repository.find_by_id(candidate_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate not found.")
        return await self._refresh_elapsed_status(candidate)

    async def update_candidate(
        self, candidate_id: str, payload: CandidateUpdate, updated_by: str
    ) -> Candidate:
        """Update an existing candidate."""
        await self.get_candidate(candidate_id)

        if payload.mobile_number is not None:
            if await candidate_repository.mobile_exists_for_other(
                payload.mobile_number, candidate_id
            ):
                raise ConflictException(
                    "A candidate with this mobile number already exists."
                )

        update_data = payload.model_dump(exclude_none=True)
        updated = await candidate_repository.update_candidate(candidate_id, update_data)
        logger.info("Candidate updated: %s by %s", candidate_id, updated_by)
        return updated

    async def get_resume_bytes(self, candidate_id: str) -> bytes:
        """Returns raw PDF bytes for streaming inline to the browser tab."""
        candidate = await self.get_candidate(candidate_id)
        if not candidate.resume_data:
            raise ResourceNotFoundException("No resume found for this candidate")
        return candidate.resume_data

    async def update_status(
        self, candidate_id: str, payload: CandidateStatusUpdate, changed_by: str
    ) -> Candidate:
        """"
          HR records the final hiring decision.

        Only SELECTED and REJECTED may be set by hand. A decision can only be
        made when the interviewer's most recent feedback recommended SELECT or
        REJECT. While the latest recommendation is NEXT_ROUND, the candidate
        stays in the interviewing loop and HR must schedule another interview
        instead of deciding.
        """
        candidate = await self.get_candidate(candidate_id)
        previous_status = candidate.status
        new_status = payload.status

        if new_status not in HR_ALLOWED_STATUSES:
            raise ConflictException(
                "Only SELECTED and REJECTED can be set manually. Earlier stages "
                "are updated automatically when interviews are scheduled and held."
            )

        if previous_status == new_status:
            raise ConflictException(f"Candidate is already in {new_status} status.")

        allowed = VALID_TRANSITIONS.get(previous_status, [])
        if new_status not in allowed:
            if not allowed:
                raise ConflictException(
                    f"Status '{previous_status}' is a terminal state. "
                    "No further changes allowed."
                )
            raise ConflictException(
                f"Cannot transition from '{previous_status}' to '{new_status}'."
            )

        latest = await interview_repository.find_latest_for_candidate(candidate_id)
        if not latest:
            raise ConflictException(
                "Cannot decide on a candidate who has not been interviewed."
            )

        feedback = await feedback_repository.find_by_interview(str(latest.id))
        if not feedback:
            raise ConflictException(
                "Cannot decide on this candidate until the interviewer has "
                "submitted feedback for their most recent interview."
            )
        
        if feedback.recommendation == RecommendationEnum.NEXT_ROUND:
            raise ConflictException(
                "The interviewer recommended another round. Schedule the next "
                "interview instead of making a hiring decision."
            )

        return await self._apply_status_change(
            candidate_id, previous_status, new_status, changed_by
        )


    async def get_status_history(self, candidate_id: str) -> list[StatusHistory]:
        """Returns the complete status transition history."""
        await self.get_candidate(candidate_id)
        return await candidate_repository.get_status_history(candidate_id)
    
    
    async def get_last_recommendation(self, candidate_id: str) -> str | None:
        """
        Returns the recommendation from the candidate's most recent interview
        feedback, or None if there is no interview or no feedback yet.
        """
        latest = await interview_repository.find_latest_for_candidate(candidate_id)
        if not latest:
            return None

        feedback = await feedback_repository.find_by_interview(str(latest.id))
        if not feedback:
            return None

        return feedback.recommendation


candidate_service = CandidateService()