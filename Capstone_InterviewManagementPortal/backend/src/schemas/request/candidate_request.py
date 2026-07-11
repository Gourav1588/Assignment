"""
Request schemas for Candidate Management endpoints.
CandidateCreate is used only for field validation in the service layer.
The router receives fields via Form() and resume via File().
"""
from pydantic import BaseModel, EmailStr, Field, field_validator,model_validator
from src.enums.candidate_enums import CandidateStatus
import re


def _validate_mobile(v: str) -> str:
    digits = v.replace("+", "").replace("-", "").replace(" ", "")
    if not digits.isdigit():
        raise ValueError("Mobile number must contain only digits.")
    if len(digits) != 10:
        raise ValueError("Mobile number must be exactly 10 digits.")
    
    if digits[0] not in {"6", "7", "8", "9"}:
        raise ValueError(
            "Mobile number must start with 6, 7, 8, or 9."
        )
    return digits


def _validate_name(v: str) -> str:
    if not v.strip():
        raise ValueError("Field cannot be empty or contain only spaces.")
    if not v.strip().replace(" ", "").isalpha():
        raise ValueError("Field must contain only letters.")
    return v.strip()

class CandidateCreate(BaseModel):
    """Validates payload when HR creates a new candidate profile."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    mobile_number: str
    current_company: str = Field(..., min_length=1, max_length=100)
    total_experience: float = Field(..., ge=0, le=50)
    applied_job: str = Field(..., min_length=1, max_length=24) 

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        return _validate_mobile(v)
    
    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        return _validate_name(v)
    
    @field_validator("current_company")
    @classmethod
    def validate_company(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces.")
        return v.strip()
    
    @field_validator("applied_job")
    @classmethod
    def validate_applied_job(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Applied job is required.")
        return v.strip()
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: EmailStr) -> str:
        email = str(v).strip().lower()

        email_regex = re.compile(
            r"^[A-Za-z0-9]+([._-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$"
        )

        if not email_regex.fullmatch(email):
            raise ValueError("Enter a valid email address.")

        return email



class CandidateUpdate(BaseModel):
    """Validates payload when HR updates a candidate profile.
    Only these fields can be changed — email and mobile are immutable after creation.
    """
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    mobile_number: str | None = None
    current_company: str | None = Field(default=None, min_length=2, max_length=100)
    total_experience: float | None = Field(default=None, ge=0, le=50)

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _validate_mobile(v)

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _validate_name(v)

    @field_validator("current_company")
    @classmethod
    def validate_company(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only spaces.")
        return v.strip()
    
    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if all(
            getattr(self, field) is None
            for field in ("first_name", "last_name", "mobile_number", "current_company", "total_experience")
        ):
            raise ValueError("At least one field must be provided to update.")
        return self


class CandidateStatusUpdate(BaseModel):
    """Validates payload when HR updates candidate status."""
    status: CandidateStatus