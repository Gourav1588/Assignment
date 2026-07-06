"""
This module contains reusable FastAPI dependencies for authentication and role-based access control.
"""


from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from src.core.security import security_scheme, verify_password
from src.repositories.user_repository import user_repository
from src.models.users import User
from src.enums.roles import UserRole
from src.core.exceptions import ForbiddenException,UnauthorizedException


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security_scheme)) -> User:
    """
    Validates Basic Auth credentials on every incoming request.
    """
    
    user = await user_repository.find_by_email(credentials.username.lower())
    
    if not user or not verify_password(credentials.password, user.password):
      raise UnauthorizedException("Invalid email or password credentials.")
    return user

def require_role(*allowed_roles: UserRole):
    """
    Dependency factory for restricting a route to specific user roles.
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(f"This action requires one of the following roles: {[r.value for r in allowed_roles]}")
        return current_user
    return role_checker