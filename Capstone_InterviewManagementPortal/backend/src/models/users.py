"""
This module defines our user database models and request/response validation schemas.

Contains:
- User         → Beanie Document mapped to the MongoDB 'users' collection
- UserCreate   → Validates incoming payload when Admin creates a new user
- UserUpdate         → Validates payload when Admin updates a user
- UserResponse → Safe outbound shape — never exposes password field
- PasswordResetRequest → Validates payload for first-login password reset
"""

import re
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from src.enums.roles import UserRole


class User(Document):
    """
    Primary database collection document for the users collection.
    Mapped to MongoDB via Beanie's Document base class.
    
    is_password_reset_pending defaults to True because every user
    created by Admin must reset their password on first login.
    """
    email: EmailStr = Field(..., index=True, unique=True)
    password: str                              
    role: UserRole                             
    full_name: str
    is_password_reset_pending: bool = True     
    is_active: bool = True

    class Settings:
        name = "users"                         


class UserCreate(BaseModel):
    """
    Request schema for Admin creating a new user account.
    Validates email domain, password complexity, and role assignment.
    """
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=12,
        description="Password must be 6-12 characters"
    )
    role: UserRole
    full_name: str = Field(..., min_length=2)

    @field_validator("email")
    @classmethod
    def validate_corporate_email(cls, v: str) -> str:
        """Restricts registration to @nucleusteq.com domain only."""
        email_clean = v.lower()
        if not email_clean.endswith("@nucleusteq.com"):
            raise ValueError(
                "Email registration restricted exclusively to @nucleusteq.com domain."
            )
        return email_clean

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        """
        Enforces password must have:
        - At least one letter
        - At least one digit
        - At least one special character from (@$!%*#?&)
        - Length between 6 and 12 characters
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,12}$", v
        ):
            raise ValueError(
                "Password must be alphanumeric and contain "
                "at least one special character (@$!%*#?&)."
            )
        return v
    


class UserUpdate(BaseModel):
    """
    Request schema for Admin updating an existing user account.
    All fields are optional — only provided fields are updated.
    Email and password cannot be changed via this endpoint.
    """
    full_name: str | None = Field(default=None, min_length=2)
    role: UserRole | None = None


class UserResponse(BaseModel):
    """
    Outbound response schema for user data.
    
    validation_alias="_id" maps MongoDB's internal _id field
    to the cleaner Python name 'id'.
    """
    id: PydanticObjectId = Field(..., validation_alias="_id")
    email: EmailStr
    role: UserRole
    full_name: str
    is_password_reset_pending: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,    # allows reading from Beanie model objects
        populate_by_name=True    # allows using 'id' or '_id' interchangeably
    )


class PasswordResetRequest(BaseModel):

    new_password: str = Field(..., description="New password replacing the Admin-assigned one")

    @field_validator("new_password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        """
        Enforces the same complexity rules as UserCreate.
        Regex covers length (6-12) so no separate len() check needed.
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,12}$", v
        ):
            raise ValueError(
                "Password must contain letters, numbers, "
                "and special characters (@$!%*#?&)."
            )
        return v