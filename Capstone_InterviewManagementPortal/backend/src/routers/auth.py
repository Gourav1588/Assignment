"""
Defines REST routes handling security verifications, logins, and credential modifications.

Contains:
- login_user           → Validates Basic Auth and returns user profile
- reset_temporary_password → Updates temporary password on first login
- terminate_session        → Logs and handles client session termination
"""

from fastapi import APIRouter, Depends, status
from src.models.users import User, UserResponse, PasswordResetRequest
from src.services.auth_service import auth_service
from src.core.dependencies import get_current_user
from src.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=UserResponse)
async def login_user(current_user: User = Depends(get_current_user)):
    """
    Returns user metadata after successful Basic Auth verification.
    """
    logger.info(f"Login endpoint accessed successfully for user: {current_user.email}")
    return current_user


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(
    payload: PasswordResetRequest, 
    current_user: User = Depends(get_current_user)  # Extract identity from authenticated context
):
    """
    Modifies temporary credentials and fully activates corporate accounts.
    """
    logger.info(f"Password reset requested for email: {current_user.email}")
    return await auth_service.update_user_password(current_user.email, payload.new_password)
