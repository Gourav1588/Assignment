"""
Response schemas for Candidate Management endpoints.
"""
from datetime import datetime
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
    status: CandidateStatus
    created_by:str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
class StatusHistoryResponse(BaseModel):
    """
    Response schema for returning candidate workflow status history logs.
    Captures exact state transition logs for auditing.
    """
    id: PydanticObjectId = Field(...)
    candidate_id: str
    previous_status: str
    new_status: str
    changed_by: str
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)