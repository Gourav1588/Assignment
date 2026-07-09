"""
Response schema for Feedback endpoints.
"""
from datetime import datetime
from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict
from src.enums.interview_enums import RecommendationEnum


class FeedbackResponse(BaseModel):
    """Response model returned for feedback operations."""
    id:                   PydanticObjectId
    interview_id:         str
    candidate_id:         str
    interviewer_id:       str
    technical_rating:     int
    communication_rating: int
    problem_solving:      int
    tech_areas_covered:   str
    comments:             str
    recommendation:       RecommendationEnum
    submitted_at:         datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )