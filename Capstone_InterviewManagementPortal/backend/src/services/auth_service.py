"""
Handles business logic operations for user verification sessions and security resets.

Contains:
- authenticate_user   → Validates credentials against registered MongoDB documents
- change_password      → Verifies current credentials and applies a voluntary update
"""
import logging
from src.models.users import User
from src.core.security import hash_password, verify_password
from src.core.exceptions import ResourceNotFoundException, UnauthorizedException

logger = logging.getLogger(__name__)


class AuthService:
    """
    Business logic layer for managing user access and core credential modifications.
    """

    async def authenticate_user(self,   email: str, password: str,) -> User:
        """
        Validates credentials against registered MongoDB database documents.
        """
        user = await User.find_one(User.email == email.lower())
        if not user:
            logger.warning(f"Failed login attempt: Account {email} not found.")
            raise UnauthorizedException("Invalid corporate email or password.")
            
        if not verify_password(password, user.password):
            logger.warning(f"Failed login attempt: Incorrect password signature for {user.email}.")
            raise UnauthorizedException("Invalid corporate email or password.")
            
        logger.info(f"User authentication successful: {user.email} [{user.role}]")
        return user

    
    async def change_password(self, email: str, old_password: str, new_password: str) -> User:
        """
        Single method for both first login reset and voluntary change.
        Always verifies old password — proves identity before allowing update.
        """
        user = await User.find_one(User.email == email.lower())
        if not user:
            raise ResourceNotFoundException(f"Account not found.")

        if not verify_password(old_password, user.password):
            raise UnauthorizedException("Current password is incorrect.")

        user.password = hash_password(new_password)
        user.is_password_reset_pending = False
        await user.save()
        logger.info(f"Password changed voluntarily for: {user.email}")
        return user
    

auth_service = AuthService()