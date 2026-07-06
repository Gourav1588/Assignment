"""
This module handles our database connection.
"""
import logging
from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import settings
from src.models.users import User

logger = logging.getLogger(__name__)

class Database:
    """
    Manages starting and stopping the database client.
    """
    client: Optional[Any] = None
    db = None

    @classmethod
    async def connect_db(cls) -> None:
        """
        Connects to the database and initializes our data models.
        """
        try:
            cls.client = AsyncIOMotorClient(settings.MONGO_URI)
            cls.db = cls.client[settings.DATABASE_NAME]
        
            await cls.client.admin.command("ping") 
        
            await init_beanie(database=cls.db, document_models=[User])
            logger.info(f"Connected to database: {settings.DATABASE_NAME}")
        
        except Exception as e:
            logger.critical(f"Database initialization failed during startup: {e}")
            raise e
            

    @classmethod
    def close_db(cls) -> None:
        """
        Closes the database connection when the app shuts down.
        """
        if cls.client is not None:
            cls.client.close()
            logger.info("Database connection closed cleanly.")