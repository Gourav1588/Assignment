from src.core.config import settings
from src.repositories.user_repository import user_repository
from src.models.users import User
from src.enums.roles import UserRole
from src.core.security import hash_password
import logging

logger = logging.getLogger(__name__)

class SeedService:

    async def seed_admin(self):
        
        

        existing = await user_repository.find_by_email(
            settings.DEFAULT_ADMIN_EMAIL
        )

        if existing:
            logger.warning("Default admin already exists.")
            
            return

        admin = User(
            full_name=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=hash_password(
                settings.DEFAULT_ADMIN_PASSWORD
            ),
            role=UserRole.ADMIN,
            is_active=True,
            is_password_reset_pending=True,
        )

        await user_repository.save_user(admin)
        logger.info("Default admin created successfully.")

seed_service = SeedService()