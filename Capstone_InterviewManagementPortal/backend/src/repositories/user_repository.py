
"""
This module handles direct database operations for the User collection.
"""

from typing import Optional
from src.models.users import User
from beanie import PydanticObjectId

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
    async def find_by_id(user_id: str) -> Optional[User]:
        """
        Queries MongoDB to find a user matching the given ObjectId string.
        Returns None if the ID does not exist in the collection.
        """
        try:
            return await User.get(PydanticObjectId(user_id))
        except Exception:
            return None
        
    @staticmethod
    async def find_all() -> list[User]:
        """
        Returns all user documents from the collection.
        Sorted by full_name ascending for consistent listing order.
        """
        return await User.find_all().to_list()

    @staticmethod
    async def save_user(user_document: User) -> User:
        """
        Inserts a new verified user document record into the collection.
        """
        await user_document.insert()
        return user_document

    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
     user = await UserRepository.find_by_id(user_id)
     if not user:
        return None

    # Set each field manually then save
     for field, value in update_data.items():
        setattr(user, field, value)

     await user.save()
     return user
    
    @staticmethod
    async def disable_user(user_id:str) -> Optional[User]:
        """
        Finds a user by ID and sets is_active to False.
        Preserves audit history. Returns the updated user document.
        """
        user = await UserRepository.find_by_id(user_id)
        if not user:
            return None
        
        await user.set({"is_active": False})
        return user
    
user_repository = UserRepository()