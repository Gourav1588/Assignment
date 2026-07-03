"""
Response schemas for Candidate Management endpoints.
"""

from pydantic import BaseModel, ConfigDict, Field
from beanie import PydanticObjectId
from src.enums.candidate_enums import CandidateStatus


class CandidateResponse(BaseModel):
    """
    Response model returned for candidate operations.
    """

    id: PydanticObjectId = Field(..., validation_alias="_id")
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    current_company: str
    total_experience: float
    applied_job: str
    resume_path: str | None = None
    status: CandidateStatus
    created_by:str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )