"""
This module defines our user database models.

Contains:
- User         → Beanie Document mapped to the MongoDB 'users' 
"""
from typing import Annotated
from beanie import Document,Indexed
from pydantic import  EmailStr, Field
from src.enums.roles import UserRole


class User(Document):
    """
    Primary database collection document for the users collection.
    Mapped to MongoDB via Beanie's Document base class.
    
    is_password_reset_pending defaults to True because every user
    created by Admin must reset their password on first login.
    """
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str                              
    role: UserRole                             
    full_name: str
    is_password_reset_pending: bool = True   
    is_active: bool = True  

    class Settings:
        name = "users"                         


