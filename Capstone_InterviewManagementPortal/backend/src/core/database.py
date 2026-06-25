"""
This module handles our database connection.
"""
from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import settings
from src.models.users import User

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
        cls.client = AsyncIOMotorClient(settings.MONGO_URI)
        cls.db = cls.client[settings.DATABASE_NAME]
        
        await init_beanie(database=cls.db, document_models=[User])
        print(f"Connected to database: {settings.DATABASE_NAME}")

    @classmethod
    def close_db(cls) -> None:
        """
        Closes the database connection when the app shuts down.
        """
        if cls.client is not None:
            cls.client.close()
            print("Database connection closed.")