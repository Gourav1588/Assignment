"""
Business logic for Interview Management module.

Contains:
- create_interview → validates candidate and interviewer then creates interview
- list_interviews  → returns paginated interviews for HR (all interviews)
- my_interviews    → returns paginated interviews for current interviewer only
- get_interview    → returns single interview or raises 404
- update_interview → validates and updates interview fields
"""
import logging
import math
from src.models.interview import Interview
from src.repositories.interview_repository import interview_repository
from src.repositories.candidate_repository import candidate_repository
from src.repositories.user_repository import user_repository
from src.schemas.request.interview_request import InterviewCreate, InterviewUpdate
from src.schemas.response.interview_response import InterviewResponse
from src.schemas.response.pagination import PaginatedResponse
from src.core.exceptions import ResourceNotFoundException, ConflictException, ForbiddenException
from src.enums.roles import UserRole
from src.enums.candidate_enums import CandidateStatus

logger = logging.getLogger(__name__)


class InterviewService:

    async def create_interview(
        self, payload: InterviewCreate, scheduled_by: str
    ) -> Interview:
        """
        Creates a new interview after validating:
        1. Candidate exists
        2. Interviewer exists, is active, and has Interviewer role
        3. Candidate is not already booked at the same date and time
        4. Interviewer is not already booked at the same date and time
        """
        candidate = await candidate_repository.find_by_id(payload.candidate_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate not found.")

        if candidate.status != CandidateStatus.PROFILE_CREATED:
            raise ConflictException(
                "Interview cannot be scheduled for this candidate."
            )

        interviewer = await user_repository.find_by_id(payload.interviewer_id)
        if not interviewer:
            raise ResourceNotFoundException("Interviewer not found.")

        if not interviewer.is_active:
            raise ConflictException(
                "Cannot assign an inactive interviewer."
            )

        if interviewer.role != UserRole.INTERVIEWER:
            raise ConflictException(
                "Assigned user must have the Interviewer role."
            )

        # check candidate is not already booked at same slot
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

        # check interviewer is not already booked at same slot
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
        logger.info(
            "Interview scheduled for candidate %s by %s",
            payload.candidate_id,
            scheduled_by,
        )
        return created

    async def list_interviews(
        self, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[InterviewResponse]:
        """
        Returns paginated list of all interviews.
        """
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
        """
        Returns paginated interviews assigned to the current interviewer.
        Interviewers can only see their own assigned interviews.
        """
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
        Returns single interview.
        HR can see any interview.
        Interviewer can only see interviews assigned to them.
        """

        # Admin has no access to interviews
        if current_user_role == UserRole.ADMIN:
            raise ForbiddenException(
                "Admins are not authorized to view interviews."
            )

        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")

        if current_user_role == UserRole.INTERVIEWER:
            if interview.interviewer_id != current_user_id:
                raise ForbiddenException(
                    "You can only view interviews assigned to you."
                )

        return interview

    async def update_interview(
        self, interview_id: str, payload: InterviewUpdate, updated_by: str
    ) -> Interview:
        """
        Updates interview fields.
        Validates interviewer role if changing interviewer.
        Checks for double booking on candidate and interviewer.
        Excludes the current interview from conflict checks.
        """
        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")

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

        final_date = update_data.get(
            "interview_date",
            interview.interview_date,
        )

        final_time = update_data.get(
            "interview_time",
            interview.interview_time,
        )

        final_candidate_id = interview.candidate_id

        final_interviewer_id = update_data.get(
            "interviewer_id",
            interview.interviewer_id,
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
            interview_id,
            update_data,
        )

        logger.info("Interview %s updated by %s", interview_id, updated_by)
        return updated


interview_service = InterviewService()