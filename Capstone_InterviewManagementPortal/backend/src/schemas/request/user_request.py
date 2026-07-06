import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.enums.roles import UserRole


def validate_complexity(v: str) -> str:
    if len(v) < 6 or len(v) > 12:
        raise ValueError("Password must be between 6 and 12 characters long.")
    if not any(c.isalpha() for c in v):
        raise ValueError("Password must contain at least one letter.")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least one number.")
    if not any(c in "@$!%*#?&" for c in v):
        raise ValueError("Password must contain at least one special character (@$!%*#?&).")
    return v


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)
    role: UserRole
    full_name: str = Field(..., min_length=2)

    @field_validator("email")
    @classmethod
    def validate_corporate_email(cls, v: str) -> str:
        email_clean = v.lower()
        if not email_clean.endswith("@nucleusteq.com"):
            raise ValueError("Email must be a @nucleusteq.com address.")
        return email_clean

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_complexity(v)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2)
    role: UserRole | None = None



class PasswordChangeRequest(BaseModel):
    """Voluntary password change — old password required."""
    old_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., description="New password to replace current")

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_complexity(v)