"""
Business logic for Feedback Management module.

Contains:
- submit_feedback → validates interviewer, prevents duplicates, saves feedback
- get_feedback    → returns feedback for a specific interview
"""
import logging
from src.models.feedback import Feedback
from src.repositories.feedback_repository import feedback_repository
from src.repositories.interview_repository import interview_repository
from src.schemas.request.feedback_request import FeedbackCreate
from src.core.exceptions import (
    ResourceNotFoundException,
    ConflictException,
    ForbiddenException,
)

logger = logging.getLogger(__name__)


class FeedbackService:

    async def submit_feedback(
        self,
        interview_id: str,
        payload: FeedbackCreate,
        submitted_by_id: str,
    ) -> Feedback:
        """
        Submits feedback for an interview.
        """
        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")

        # Only assigned interviewer can submit feedback
        if interview.interviewer_id != submitted_by_id:
            raise ForbiddenException(
                "Only the assigned interviewer can submit feedback."
            )

        # Prevent duplicate feedback
        if await feedback_repository.exists_for_interview(interview_id):
            raise ConflictException(
                "Feedback already submitted for this interview."
            )

        feedback = Feedback(
            interview_id=interview_id,
            candidate_id=interview.candidate_id,
            interviewer_id=submitted_by_id,
            technical_rating=payload.technical_rating,
            communication_rating=payload.communication_rating,
            problem_solving=payload.problem_solving,
            tech_areas_covered=payload.tech_areas_covered,
            comments=payload.comments,
            recommendation=payload.recommendation,
        )
        created = await feedback_repository.create_feedback(feedback)
        logger.info(
            "Feedback submitted for interview %s by %s",
            interview_id, submitted_by_id
        )
        return created

    async def get_feedback(
        self,
        interview_id: str,
        current_user_id: str,
        current_user_role: str,
    ) -> Feedback:
        """
        Returns feedback for a specific interview.
        """
        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            raise ResourceNotFoundException("Interview not found.")
       
         # Admin has no access to feedback
        if current_user_role == "Admin":
            raise ForbiddenException(
                "Admins are not authorized to view interview feedback."
        )

        # Interviewer can only view feedback for their assigned interview
        if current_user_role == "Interviewer":
            if interview.interviewer_id != current_user_id:
                raise ForbiddenException(
                    "You can only view feedback for interviews assigned to you."
                )

        feedback = await feedback_repository.find_by_interview(interview_id)
        if not feedback:
            raise ResourceNotFoundException(
                "No feedback submitted for this interview yet."
            )
        return feedback


feedback_service = FeedbackService()