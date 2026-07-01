"""
This module defines HTTP API endpoints for user management.
All endpoints are restricted to Admin role only.

Contains:
- POST   /users              → create a new user
- GET    /users              → list all users
- GET    /users/{user_id}    → get user by ID
- PUT    /users/{user_id}    → update user
- PATCH  /users/{user_id}/disable → disable user
"""
import logging
from fastapi import APIRouter, Depends, status
from src.schemas.request.user_request import UserCreate, UserUpdate
from src.schemas.response.user_response import UserResponse
from src.services.user_service import user_service
from src.core.dependencies import require_role
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["User Management"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin creates a new HR or Interviewer account."""
    logger.info(f"Create user request received for {payload.email}")
    return await user_service.create_user(payload)


@router.get("", response_model=list[UserResponse])
async def list_users(
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin retrieves all user accounts."""
    logger.info("List users request received.")
    return await user_service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin retrieves a single user by their ID."""
    logger.info(f"Get user request received for ID: {user_id}")
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdate,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin updates a user's full_name or role."""
    logger.info(f"Update user request received for ID: {user_id}")
    return await user_service.update_user(user_id, payload)


@router.patch("/{user_id}/disable", response_model=UserResponse)
async def disable_user(
    user_id: str,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """
    Admin disables a user account.
    Sets is_active to False — does not delete the user.
    """
    logger.info(f"Disable user request received for ID: {user_id}")
    return await user_service.disable_user(user_id)

@router.patch("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: str,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin reactivates a disabled user account."""
    return await user_service.activate_user(user_id)