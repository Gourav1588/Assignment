"""
Feedback API endpoints.
"""
import logging
from fastapi import APIRouter, Depends
from src.models.users import User
from src.schemas.request.feedback_request import FeedbackCreate
from src.schemas.response.feedback_response import FeedbackResponse
from src.services.feedback_service import feedback_service
from src.core.dependencies import require_role, get_current_user
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["Feedback"])


@router.post("/{interview_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    interview_id: str,
    payload: FeedbackCreate,
    current_user: User = Depends(require_role(UserRole.INTERVIEWER)),
):
    """Interviewer submits feedback for their assigned interview."""
    logger.info("Feedback submitted for %s by: %s", interview_id, current_user.email)
    return await feedback_service.submit_feedback(
        interview_id=interview_id,
        payload=payload,
        submitted_by_id=str(current_user.id),
    )


@router.get("/{interview_id}/feedback", response_model=FeedbackResponse)
async def get_feedback(
    interview_id: str,
    current_user: User = Depends(get_current_user),
):
    """HR or assigned Interviewer views feedback for a specific interview."""
    logger.info("Get feedback for %s by: %s", interview_id, current_user.email)
    return await feedback_service.get_feedback(
        interview_id=interview_id,
        current_user_id=str(current_user.id),
        current_user_role=current_user.role,
    )