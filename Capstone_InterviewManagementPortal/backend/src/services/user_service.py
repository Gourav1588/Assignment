"""
Handles business logic for all user management operations.

Contains:
- create_user    → validates, hashes password, saves new user
- list_users     → returns all users in the system
- get_user_by_id → returns single user or raises 404
- update_user    → updates full_name and/or role
- disable_user   → sets is_active to False
"""

from src.models.users import User, UserCreate, UserUpdate
from src.repositories.user_repository import user_repository
from src.core.security import hash_password
from src.core.exceptions import ResourceNotFoundException, DuplicateEmailException,ConflictException
from src.core.logger import logger


class UserService:

    async def create_user(self, payload: UserCreate) -> User:
        """
        Creates a new user account.
        Checks for duplicate email before saving.
        Password is Base64 encoded before storage.
        is_password_reset_pending defaults to True — user must reset on first login.
        """
        existing = await user_repository.find_by_email(payload.email)
        if existing:
            raise DuplicateEmailException("A user with this email already exists.")

        user = User(
            email=payload.email,
            password=hash_password(payload.password),
            role=payload.role,
            full_name=payload.full_name,
            is_password_reset_pending=True,
            is_active=True,
        )
        created = await user_repository.save_user(user)
        logger.info("User created: %s [%s]", created.email, created.role)
        return created

    async def list_users(self) -> list[User]:
        """Returns all users. Admin sees everyone."""
        return await user_repository.find_all()

    async def get_user_by_id(self, user_id: str) -> User:
        """Returns a single user by ID or raises 404."""
        user = await user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID '{user_id}' not found.")
        return user

    async def update_user(self, user_id: str, payload: UserUpdate) -> User:
        """
        Updates only the fields provided in the payload.
        model_dump(exclude_none=True) ensures fields not sent
        are not overwritten with None.
        """
        await self.get_user_by_id(user_id)  # raises 404 if not found

        update_data = payload.model_dump(exclude_none=True)
        updated = await user_repository.update_user(user_id, update_data)
        logger.info("User updated: %s", user_id)
        return updated

    async def disable_user(self, user_id: str) -> User:
        """
        Sets is_active to False.
        Does not delete the user — keeps history and audit trail intact.
        """
        await self.get_user_by_id(user_id)  # raises 404 if not found

        disabled = await user_repository.disable_user(user_id)
        logger.info("User disabled: %s", user_id)
        return disabled
    
    async def activate_user(self, user_id: str) -> User:
        """
        Sets is_active to True.
        Reactivates a previously disabled user account back into active service.
        """
        user = await self.get_user_by_id(user_id)
        if user.is_active:
           raise ConflictException("User is already active.")
        activated = await user_repository.activate_user(user_id)
        logger.info("User reactivated: %s", user_id)
        return activated
    


user_service = UserService()