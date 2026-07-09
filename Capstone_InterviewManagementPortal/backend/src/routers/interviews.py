"""
Interview Management API endpoints.

Contains:
- POST /interviews                      → HR schedules a new interview
- GET  /interviews                      → HR lists all interviews
- GET  /interviews/my                   → Interviewer lists their assigned interviews
- GET  /interviews/{id}                 → HR or Interviewer views single interview
- PUT  /interviews/{id}                 → HR updates interview details
- POST /interviews/{id}/feedback        → Interviewer submits feedback
- GET  /interviews/{id}/feedback        → HR or Interviewer views feedback
"""
import logging
from fastapi import APIRouter, Depends, Query
from src.models.users import User
from src.schemas.request.interview_request import InterviewCreate, InterviewUpdate
from src.schemas.response.interview_response import InterviewResponse
from src.schemas.response.pagination import PaginatedResponse
from src.services.interview_service import interview_service
from src.core.dependencies import require_role, get_current_user
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["Interview Management"])


@router.post("", response_model=InterviewResponse)
async def schedule_interview(
    payload: InterviewCreate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR schedules a new interview for a candidate."""
    logger.info("Schedule interview by: %s", current_user.email)
    return await interview_service.create_interview(
        payload, scheduled_by=current_user.email
    )


@router.get("", response_model=PaginatedResponse[InterviewResponse])
async def list_interviews(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR retrieves paginated list of all interviews."""
    logger.info("List interviews by: %s", current_user.email)
    return await interview_service.list_interviews(page=page, page_size=page_size)


@router.get("/my", response_model=PaginatedResponse[InterviewResponse])
async def my_interviews(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.INTERVIEWER)),
):
    """
    Interviewer retrieves their own assigned interviews.
    """
    logger.info("My interviews for: %s", current_user.email)
    return await interview_service.my_interviews(
        interviewer_id=str(current_user.id),
        page=page,
        page_size=page_size,
    )



@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    HR or assigned Interviewer views a single interview.
    """
    logger.info("Get interview %s by: %s", interview_id, current_user.email)
    return await interview_service.get_interview(
        interview_id=interview_id,
        current_user_id=str(current_user.id),
        current_user_role=current_user.role,
    )


@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: str,
    payload: InterviewUpdate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR updates interview details."""
    logger.info("Update interview %s by: %s", interview_id, current_user.email)
    return await interview_service.update_interview(
        interview_id, payload, updated_by=current_user.email
    )




