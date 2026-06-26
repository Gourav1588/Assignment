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

from fastapi import APIRouter, Depends, status
from src.models.users import UserCreate, UserUpdate, UserResponse
from src.services.user_service import user_service
from src.core.dependencies import require_role
from src.enums.roles import UserRole

router = APIRouter(prefix="/users", tags=["User Management"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin creates a new HR or Interviewer account."""
    return await user_service.create_user(payload)


@router.get("", response_model=list[UserResponse])
async def list_users(
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin retrieves all user accounts."""
    return await user_service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin retrieves a single user by their ID."""
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdate,
    _=Depends(require_role(UserRole.ADMIN)),
):
    """Admin updates a user's full_name or role."""
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
    return await user_service.disable_user(user_id)