"""
Request schemas for Candidate Management endpoints.
CandidateCreate is used only for field validation in the service layer.
The router receives fields via Form() and resume via File().
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.enums.candidate_enums import CandidateStatus

class CandidateCreate(BaseModel):
    """Validates payload when HR creates a new candidate profile."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    mobile_number: str
    current_company: str = Field(..., min_length=1, max_length=100)
    total_experience: float = Field(..., ge=0, le=50)
    applied_job: str

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        digits = v.replace("+", "").replace("-", "").replace(" ", "")
        if not digits.isdigit():
            raise ValueError("Mobile number must contain only digits.")
        if len(digits) != 10:
            raise ValueError("Mobile number must be exactly 10 digits.")
        return digits


class CandidateUpdate(BaseModel):
    """Validates payload when HR updates a candidate profile.
    Only these fields can be changed — email and mobile are immutable after creation."""
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    mobile_number: str| None = None
    current_company: str | None = Field(default=None, min_length=2, max_length=100)
    total_experience: float | None = Field(default=None, ge=0, le=50)
    
    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        digits = v.replace("+", "").replace("-", "").replace(" ", "")
        if not digits.isdigit():
            raise ValueError("Mobile number must contain only digits.")
        if len(digits) != 10:
            raise ValueError("Mobile number must be exactly 10 digits.")
        return digits

class CandidateStatusUpdate(BaseModel):
    """Validates payload when HR updates candidate status."""
    status: CandidateStatus