"""
Handles business logic operations for user verification sessions and security resets.

Contains:
- authenticate_user   → Validates credentials against registered MongoDB documents
- update_user_password → Updates password hash and deactivates first-login flags
"""

from src.models.users import User
from src.core.security import hash_password, verify_password
from src.core.exceptions import ResourceNotFoundException, UnauthorizedException
from src.core.logger import logger


class AuthService:
    """
    Business logic layer for managing user access and core credential modifications.
    """

    async def authenticate_user(self, credentials_payload) -> User:
        """
        Validates credentials against registered MongoDB database documents.
        """
        user = await User.find_one(User.email == credentials_payload.email.lower())
        if not user:
            logger.warning(f"Failed login attempt: Account {credentials_payload.email} not found.")
            raise UnauthorizedException("Invalid corporate email or password.")
            
        if not verify_password(credentials_payload.password, user.password):
            logger.warning(f"Failed login attempt: Incorrect password signature for {user.email}.")
            raise UnauthorizedException("Invalid corporate email or password.")
            
        logger.info(f"User authentication successful: {user.email} [{user.role}]")
        return user

    async def update_user_password(self, email: str, new_password: str) -> User:
        """
        Updates an account's password hash and clears the first-login reset flag.
        """
        user = await User.find_one(User.email == email.lower())
        if not user:
            raise ResourceNotFoundException(f"Account with email '{email}' does not exist.")
            
        encoded_string = hash_password(new_password)  # Converts clean password into secure cryptographic hash
        
        user.password = encoded_string
        user.is_password_reset_pending = False        # Disables forced reset prompt for subsequent logins
        
        await user.save()
        logger.info(f"Mandatory security password reset completed successfully for: {user.email}")
        return user


auth_service = AuthService()