"""
Beanie document model for Interview records.

Each interview represents one round of interview for a candidate.
One candidate can have multiple interviews (multiple rounds).
Each interview is linked to exactly one interviewer.
"""
from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class Interview(Document):
    """
    Stores interview schedule information.
    candidate_id   → links to Candidate document
    interviewer_id → links to User document (Interviewer role)
    scheduled_by   → email of HR who created this interview
    """
    candidate_id:   str
    job_title:      str
    interview_date: str        # stored as string "YYYY-MM-DD"
    interview_time: str        # stored as string "HH:MM"
    interviewer_id: str
    focus_areas:    str
    scheduled_by:   str
    created_at:     datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "interviews"