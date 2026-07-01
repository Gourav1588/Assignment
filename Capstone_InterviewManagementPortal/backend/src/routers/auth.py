"""
Defines REST routes handling security verifications, logins, and credential modifications.

Contains:
- login_user           → Validates Basic Auth and returns user profile
- POST /change-password → changes password (first login + voluntary)
"""
import logging
from fastapi import APIRouter, Depends
from src.models.users import User
from src.schemas.response.user_response import UserResponse
from src.schemas.request.user_request import  PasswordChangeRequest
from src.services.auth_service import auth_service
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.core.dependencies import get_current_user

security = HTTPBasic()


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=UserResponse)
async def login_user(
    credentials: HTTPBasicCredentials = Depends(security),
):
    
    user = await auth_service.authenticate_user(
        credentials.username,
        credentials.password,
    )
    logger.info(f"Login endpoint accessed successfully for user: {user.email}")
    return user


@router.post("/change-password", response_model=UserResponse)
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
):
    """Handles both first login forced reset and voluntary password change."""
    return await auth_service.change_password(
        current_user.email,
        payload.old_password,
        payload.new_password,
    )
