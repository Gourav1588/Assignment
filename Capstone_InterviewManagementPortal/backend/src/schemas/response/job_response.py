"""
Response schema for Job Description endpoints.
"""
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict
from src.enums.job_enums import EmploymentType


class JobResponse(BaseModel):
    id: PydanticObjectId = Field(..., validation_alias="_id")
    title: str
    details: str
    role: str
    required_skills: str
    experience_required: float
    employment_type: EmploymentType
    location: str
    created_by: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)