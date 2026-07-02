"""
Request schemas for Job Description endpoints.
"""
from pydantic import BaseModel, Field
from src.enums.job_enums import EmploymentType


class JobCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    details: str = Field(..., min_length=10)
    role: str = Field(..., min_length=2, max_length=100)
    required_skills: str = Field(..., min_length=2)
    experience_required: str = Field(..., min_length=1)
    employment_type: EmploymentType
    location: str = Field(..., min_length=2)


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    details: str | None = Field(default=None, min_length=10)
    role: str | None = Field(default=None, min_length=2, max_length=100)
    required_skills: str | None = Field(default=None, min_length=2)
    experience_required: str | None = None
    employment_type: EmploymentType | None = None
    location: str | None = Field(default=None, min_length=2)