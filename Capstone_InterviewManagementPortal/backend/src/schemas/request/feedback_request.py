"""
Request schema for Feedback submission endpoint.
"""
from pydantic import BaseModel, Field,field_validator
from src.enums.interview_enums import RecommendationEnum


class FeedbackCreate(BaseModel):
    """Validates feedback submission payload from Interviewer."""
    technical_rating:     int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    problem_solving:      int = Field(..., ge=1, le=5)
    tech_areas_covered:   str = Field(..., min_length=1, max_length=500)
    comments:             str = Field(..., min_length=1, max_length=1000)
    recommendation:       RecommendationEnum

    @field_validator("tech_areas_covered", "comments")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty or contain only spaces.")

        if value.strip().isdigit():
            raise ValueError("Field cannot contain only numbers.")

        return value.strip() 