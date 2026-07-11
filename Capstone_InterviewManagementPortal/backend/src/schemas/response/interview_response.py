"""
Response schema for Interview Management endpoints.
"""
from datetime import datetime
from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict


class InterviewResponse(BaseModel):
    """Response model returned for interview operations."""
    id:             PydanticObjectId
    candidate_id:   str
    job_title:      str
    interview_date: str
    interview_time: str
    interviewer_id: str
    focus_areas:    str
    scheduled_by:   str
    created_at:     datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )