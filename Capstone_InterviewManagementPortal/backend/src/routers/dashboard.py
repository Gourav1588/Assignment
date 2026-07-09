"""
Dashboard API endpoints.

Contains:
- GET /dashboard/hr          → HR dashboard counts
- GET /dashboard/interviewer → Interviewer dashboard counts
"""
import logging
from fastapi import APIRouter, Depends
from src.models.users import User
from src.schemas.response.dashboard_response import (
    HRDashboardResponse,
    InterviewerDashboardResponse,
)
from src.services.dashboard_service import dashboard_service
from src.core.dependencies import require_role
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/hr", response_model=HRDashboardResponse)
async def hr_dashboard(
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """Returns counts for HR dashboard."""
    logger.info("HR dashboard accessed by: %s", current_user.email)
    return await dashboard_service.get_hr_dashboard()


@router.get("/interviewer", response_model=InterviewerDashboardResponse)
async def interviewer_dashboard(
    current_user: User = Depends(require_role(UserRole.INTERVIEWER)),
):
    """Returns counts for Interviewer dashboard scoped to current user."""
    logger.info("Interviewer dashboard accessed by: %s", current_user.email)
    return await dashboard_service.get_interviewer_dashboard(
        interviewer_id=str(current_user.id)
    )