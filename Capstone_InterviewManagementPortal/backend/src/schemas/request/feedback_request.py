"""
Request schema for Feedback submission endpoint.
"""
from pydantic import BaseModel, Field
from src.enums.interview_enums import RecommendationEnum


class FeedbackCreate(BaseModel):
    """Validates feedback submission payload from Interviewer."""
    technical_rating:     int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    problem_solving:      int = Field(..., ge=1, le=5)
    tech_areas_covered:   str = Field(..., min_length=1, max_length=500)
    comments:             str = Field(..., min_length=1, max_length=1000)
    recommendation:       RecommendationEnum