"""
Handles database operations for candidate documents.

Contains:
- email_exists      → Checks whether a candidate email already exists.
- mobile_exists     → Checks whether a candidate mobile number already exists.
- create_candidate  → Inserts a new candidate document.
- find_all          → Retrieves all candidates or filters by status.
- find_by_id        → Retrieves a candidate by ID.
- update_candidate  → Updates an existing candidate document.
- get_resume_bytes   → returns raw PDF bytes for streaming
- update_status      → changes status and records transition in history
- get_status_history → returns full status transition history

"""

import logging
import math
from fastapi import UploadFile
from src.enums.candidate_enums import CandidateStatus
from src.models.candidates import Candidate
from src.models.status_history import StatusHistory
from src.repositories.candidate_repository import candidate_repository
from src.repositories.job_repository import job_repository
from src.schemas.request.candidate_request import  CandidateUpdate,CandidateStatusUpdate
from src.core.exceptions import ResourceNotFoundException, ConflictException
from src.schemas.response.candidate_response import CandidateResponse
from src.schemas.response.pagination import PaginatedResponse
logger = logging.getLogger(__name__)

MAX_RESUME_BYTES = 5 * 1024 * 1024

VALID_TRANSITIONS: dict[str, list[str]] = {
    CandidateStatus.PROFILE_CREATED:     [CandidateStatus.INTERVIEW_SCHEDULED],
    CandidateStatus.INTERVIEW_SCHEDULED: [CandidateStatus.INTERVIEW_COMPLETED],
    CandidateStatus.INTERVIEW_COMPLETED: [CandidateStatus.SELECTED, CandidateStatus.REJECTED],
    CandidateStatus.SELECTED:            [],
    CandidateStatus.REJECTED:            [],
}


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
        """Creates a candidate profile and saves the resume atomically.
        Resume is mandatory — both the profile and the file are saved
        in one operation so a candidate without a resume can never exist"""
        
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

        if len(resume_bytes) > MAX_RESUME_BYTES:
            raise ConflictException("Resume file must not exceed 5MB.")

        candidate = Candidate(
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            mobile_number=mobile_number,
            current_company=current_company,
            total_experience=total_experience,
            applied_job=applied_job,
            resume_data=resume_bytes,
            status=CandidateStatus.PROFILE_CREATED,
            created_by=created_by,
        )

        created = await candidate_repository.create_candidate(candidate)
        logger.info("Candidate created: %s by %s", created.email, created_by)
        return created
    
    
    async def list_candidates(
        self,
        page: int = 1,
        page_size: int = 10,
        status: CandidateStatus | None = None,
    ) -> PaginatedResponse[CandidateResponse]:
        """
        Returns a paginated list of candidates with optional status filter.
        """
        candidates, total = await candidate_repository.find_paginated(
            page, page_size, status
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedResponse(
            items=candidates,   
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
        return candidate

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
            raise ResourceNotFoundException(
                "No resume found for this candidate"
            )
        return candidate.resume_data

    async def update_status(
        self, candidate_id: str, payload: CandidateStatusUpdate, changed_by: str
    ) -> Candidate:
        """Transitions workflow status positions """
        candidate = await self.get_candidate(candidate_id)
        previous_status = candidate.status
        new_status = payload.status
        
        if previous_status == new_status:
            raise ConflictException(
                f"Candidate is already in {new_status} status."
        )
            
        allowed = VALID_TRANSITIONS.get(previous_status, [])
        if new_status not in allowed:
            if not allowed:
                raise ConflictException(
                    f"Status '{previous_status}' is a terminal state. No further changes allowed."
            )
            raise ConflictException(
                f"Cannot transition from '{previous_status}' to '{new_status}'. "
                f"Allowed: {', '.join(allowed)}"
        )

        updated = await candidate_repository.update_status(candidate_id, new_status)
        await candidate_repository.add_status_history(
            candidate_id=candidate_id,
            previous_status=previous_status,
            new_status=new_status,
            changed_by=changed_by,
        )
        logger.info(
            "Candidate %s status: %s → %s by %s",
            candidate_id, previous_status, new_status, changed_by
        )
        return updated

    async def get_status_history(
        self, candidate_id: str
    ) -> list[StatusHistory]:
        """Collects the complete  history."""
        await self.get_candidate(candidate_id)
        return await candidate_repository.get_status_history(candidate_id)
    
candidate_service = CandidateService()