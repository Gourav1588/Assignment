"""
Request schemas for Interview Management endpoints.

InterviewCreate → validates payload when HR schedules a new interview
InterviewUpdate → validates payload when HR updates an existing interview
                  all fields optional so HR can update just one field
"""
from pydantic import BaseModel, Field


class InterviewCreate(BaseModel):
    """Validates interview scheduling payload from HR."""
    candidate_id:   str
    job_title:      str = Field(..., min_length=1, max_length=100)
    interview_date: str = Field(..., description="Format: YYYY-MM-DD")
    interview_time: str = Field(..., description="Format: HH:MM")
    interviewer_id: str
    focus_areas:    str = Field(..., min_length=1, max_length=500)


class InterviewUpdate(BaseModel):
    """Validates interview update payload. All fields optional."""
    job_title:      str | None = Field(default=None, min_length=1, max_length=100)
    interview_date: str | None = None
    interview_time: str | None = None
    interviewer_id: str | None = None
    focus_areas:    str | None = Field(default=None, min_length=1, max_length=500)