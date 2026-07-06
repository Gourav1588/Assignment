
"""
This module handles direct database operations for the User collection.
"""

from typing import Optional
from src.models.users import User

class UserRepository:
    """
    Encapsulates all direct MongoDB database queries for users.
    """

    @staticmethod
    async def find_by_email(email: str) -> Optional[User]:
        """
        Queries MongoDB to find a user matching the given email address in lowercase.
        """
        # Enforce lowercase lookup to prevent case-sensitive authentication collisions
        return await User.find_one(User.email == email.lower())

    @staticmethod
    async def save_user(user_document: User) -> User:
        """
        Inserts a new verified user document record into the collection.
        """
        await user_document.insert()
        return user_document
    
user_repository = UserRepository()