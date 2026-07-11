"""
Business logic for Interview Management module.

Contains:
- create_interview → validates candidate and interviewer then creates interview
- list_interviews  → returns paginated interviews for HR
- my_interviews    → returns paginated interviews for the current interviewer
- get_interview    → returns single interview or raises 404
- update_interview → validates and updates interview fields

Scheduling an interview moves the candidate to INTERVIEW_SCHEDULED. Once an
interview's slot has passed it becomes read only, and further rounds are only
permitted when the previous interviewer recommended NEXT_ROUND.
"""
import logging
import math
from src.core.time_utils import has_interview_passed
from src.models.interview import Interview
from src.repositories.interview_repository import interview_repository
from src.repositories.candidate_repository import candidate_repository
from src.repositories.feedback_repository import feedback_repository
from src.repositories.user_repository import user_repository
from src.schemas.request.interview_request import InterviewCreate, InterviewUpdate
from src.schemas.response.interview_response import InterviewResponse
from src.schemas.response.pagination import PaginatedResponse
from src.core.exceptions import ResourceNotFoundException, ConflictException, ForbiddenException
from src.enums.roles import UserRole
from src.enums.candidate_enums import CandidateStatus
from src.enums.interview_enums import RecommendationEnum

logger = logging.getLogger(__name__)

TERMINAL_STATUSES = (CandidateStatus.SELECTED, CandidateStatus.REJECTED)


class InterviewService:

    async def _assert_candidate_can_be_scheduled(self, candidate_id: str) -> None:
        """
        A candidate may be scheduled when they have no interview history, or when
        their most recent interview produced a NEXT_ROUND recommendation. A hiring
        decision, whether recorded on the candidate or implied by a SELECT or
        REJECT recommendation, closes the process.
        """
        candidate = await candidate_repository.find_by_id(candidate_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate not found.")

        if candidate.status in TERMINAL_STATUSES:
            raise ConflictException(
                f"Cannot schedule an interview for a candidate who has already "
                f"been {candidate.status.lower()}."
            )

        latest = await interview_repository.find_latest_for_candidate(candidate_id)
        if not latest:
            return

        feedback = await feedback_repository.find_by_interview(str(latest.id))
        if not feedback:
            raise ConflictException(
                "Cannot schedule another interview until the interviewer has "
                "submitted feedback for the candidate's most recent interview."
            )

        if feedback.recommendation != RecommendationEnum.NEXT_ROUND:
            raise ConflictException(
                "The last interviewer did not recommend another round. "
                "Record the hiring decision instead of scheduling again."
            )

    async def create_interview(
        self, payload: InterviewCreate, scheduled_by: str
    ) -> Interview:
        """
        Creates a new interview after validating:
        1. Candidate exists and is still in the running
        2. Interviewer exists, is active, and has Interviewer role
        3. Candidate is not already booked at the same date and time
        4. Interviewer is not already booked at the same date and time

        Also advances the candidate to INTERVIEW_SCHEDULED.
        """
        # Imported here to avoid a circular import between the two services.
        from src.services.candidate_service import candidate_service

        await self._assert_candidate_can_be_scheduled(payload.candidate_id)

        interviewer = await user_repository.find_by_id(payload.interviewer_id)
        if not interviewer:
            raise ResourceNotFoundException("Interviewer not found.")

        if not interviewer.is_active:
            raise ConflictException("Cannot assign an inactive interviewer.")

        if interviewer.role != UserRole.INTERVIEWER:
            raise ConflictException("Assigned user must have the Interviewer role.")

        candidate_conflict = await interview_repository.find_conflict_for_candidate(
            candidate_id=payload.candidate_id,
            interview_date=payload.interview_date,
            interview_time=payload.interview_time,
        )
        if candidate_conflict:
            raise ConflictException(
                f"Candidate already has an interview scheduled on "
                f"{payload.interview_date} at {payload.interview_time}."
            )

        interviewer_conflict = await interview_repository.find_conflict_for_interviewer(
            interviewer_id=payload.interviewer_id,
            interview_date=payload.interview_date,
            interview_time=payload.interview_time,
        )
        if interviewer_conflict:
            raise ConflictException(
                f"Interviewer already has an interview scheduled on "
                f"{payload.interview_date} at {payload.interview_time}."
            )

        interview = Interview(
            candidate_id=payload.candidate_id,
            job_title=payload.job_title,
            interview_date=payload.interview_date,
            interview_time=payload.interview_time,
            interviewer_id=payload.interviewer_id,
            focus_areas=payload.focus_areas,
            scheduled_by=scheduled_by,
        )
        created = await interview_repository.create_interview(interview)

        await candidate_service.mark_interview_scheduled(payload.candidate_id)

        logger.info(
            "Interview scheduled for candidate %s by %s",
            payload.candidate_id, scheduled_by,
        )
        return created

    async def list_interviews(
        self, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[InterviewResponse]:
        """Returns paginated list of all interviews."""
        interviews, total = await interview_repository.find_all_paginated(
            page, page_size
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedResponse(
            items=interviews,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def my_interviews(
        self, interviewer_id: str, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[InterviewResponse]:
        """Returns paginated interviews assigned to the current interviewer."""
        interviews, total = await interview_repository.find_by_interviewer(
            interviewer_id, page, page_size
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedResponse(
            items=interviews,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def get_interview(
        self, interview_id: str, current_user_id: str, current_user_role: str
    ) -> Interview:
        """
        Returns a single interview.
        HR can see any interview, an interviewer only their own.
        Reading an interview also refreshes the candidate's status.
        """
        from src.services.candidate_service import candidate_service

        if current_user_role == UserRole.ADMIN:
            raise ForbiddenException("Admins are not authorized to view interviews.")

        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")

        if current_user_role == UserRole.INTERVIEWER:
            if interview.interviewer_id != current_user_id:
                raise ForbiddenException(
                    "You can only view interviews assigned to you."
                )

        await candidate_service.get_candidate(interview.candidate_id)

        return interview

    async def update_interview(
        self, interview_id: str, payload: InterviewUpdate, updated_by: str
    ) -> Interview:
        """
        Updates interview fields.
        An interview becomes read only once its scheduled slot has passed.
        Validates interviewer role if changing interviewer, and checks for
        double booking on both the candidate and the interviewer.
        """
        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")

        if has_interview_passed(interview.interview_date, interview.interview_time):
            raise ConflictException(
                "Cannot modify an interview that has already taken place."
            )

        if payload.interviewer_id is not None:
            interviewer = await user_repository.find_by_id(payload.interviewer_id)
            if not interviewer:
                raise ResourceNotFoundException("Interviewer not found.")

            if not interviewer.is_active:
                raise ConflictException("Cannot assign an inactive interviewer.")

            if interviewer.role != UserRole.INTERVIEWER:
                raise ConflictException(
                    "Assigned user must have the Interviewer role."
                )

        update_data = payload.model_dump(exclude_none=True)

        final_date = update_data.get("interview_date", interview.interview_date)
        final_time = update_data.get("interview_time", interview.interview_time)
        final_candidate_id = interview.candidate_id
        final_interviewer_id = update_data.get(
            "interviewer_id", interview.interviewer_id
        )

        candidate_conflict = await interview_repository.find_conflict_for_candidate(
            candidate_id=final_candidate_id,
            interview_date=final_date,
            interview_time=final_time,
            exclude_id=interview_id,
        )
        if candidate_conflict:
            raise ConflictException(
                f"Candidate already has an interview scheduled on "
                f"{final_date} at {final_time}."
            )

        interviewer_conflict = await interview_repository.find_conflict_for_interviewer(
            interviewer_id=final_interviewer_id,
            interview_date=final_date,
            interview_time=final_time,
            exclude_id=interview_id,
        )
        if interviewer_conflict:
            raise ConflictException(
                f"Interviewer already has an interview scheduled on "
                f"{final_date} at {final_time}."
            )

        updated = await interview_repository.update_interview(
            interview_id, update_data
        )

        logger.info("Interview %s updated by %s", interview_id, updated_by)
        return updated


interview_service = InterviewService()