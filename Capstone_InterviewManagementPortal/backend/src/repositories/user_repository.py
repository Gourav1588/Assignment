
"""
This module handles direct database operations for the User collection.
"""

from typing import Optional
from src.models.users import User
from beanie import PydanticObjectId
from src.enums.roles import UserRole

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
    async def find_paginated(page: int, page_size: int) -> tuple[list[User], int]:
        """
        Returns a page of users and the total count.
        skip calculates how many records to jump over based on current page.
        """
        skip = (page - 1) * page_size
        total = await User.count()
        users = await User.find_all().sort("-_id").skip(skip).limit(page_size).to_list()
        return users, total


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
    
    @staticmethod
    async def activate_user(user_id: str) -> Optional[User]:
        """
        Finds a user by ID and sets is_active to True.
        Reactivates the user document. Returns the updated user document.
        """
        user = await UserRepository.find_by_id(user_id)
        if not user:
            return None
            
        await user.set({"is_active": True})
        return user
    
    @staticmethod
    async def count_all() -> int:
        """Returns the total number of user accounts."""
        return await User.count()
    

    @staticmethod
    async def count_active() -> int:
        """Returns the number of accounts that are currently enabled."""
        return await User.find({"is_active": True}).count()
    

    @staticmethod
    async def count_by_role(role: UserRole) -> int:
        """Returns the number of accounts holding the given role."""
        return await User.find({"role": role}).count()
    
user_repository = UserRepository()