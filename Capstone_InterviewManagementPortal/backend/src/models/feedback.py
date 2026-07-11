"""
Beanie document model for Interview Feedback records.
One interview can have exactly one feedback document.
"""
from datetime import datetime, timezone
from beanie import Document
from pydantic import Field
from src.enums.interview_enums import RecommendationEnum


class Feedback(Document):
    """
    Stores interviewer feedback for a completed interview.
    interview_id   → links to Interview document
    candidate_id   → links to Candidate document
    interviewer_id → links to User who submitted feedback
    """
    interview_id:         str
    candidate_id:         str
    interviewer_id:       str
    technical_rating:     int
    communication_rating: int
    problem_solving:      int
    tech_areas_covered:   str
    comments:             str
    recommendation:       RecommendationEnum
    submitted_at:         datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "feedback"