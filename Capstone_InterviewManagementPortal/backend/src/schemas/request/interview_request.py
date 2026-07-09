"""
Request schemas for Interview Management endpoints.

InterviewCreate → validates payload when HR schedules a new interview
InterviewUpdate → validates payload when HR updates an existing interview
                  all fields optional so HR can update just one field
"""
import re
from pydantic import BaseModel, Field, field_validator
from datetime import date, timedelta

OBJECT_ID_PATTERN = r"^[0-9a-fA-F]{24}$"

class InterviewCreate(BaseModel):
    """Validates interview scheduling payload from HR."""
    candidate_id:   str = Field(..., min_length=1, max_length=24)
    job_title:      str = Field(..., min_length=2, max_length=100)
    interview_date: str = Field(..., description="Format: YYYY-MM-DD")
    interview_time: str = Field(..., description="Format: HH:MM")
    interviewer_id: str = Field(..., min_length=1, max_length=24) 
    focus_areas:    str = Field(..., min_length=2, max_length=500)
    
    @field_validator("candidate_id", "interviewer_id")  
    @classmethod
    def validate_object_id(cls, v: str) -> str:
        if not re.match(OBJECT_ID_PATTERN, v):
            raise ValueError("Must be a valid 24-character ID.")
        return v

    @field_validator("interview_date")
    @classmethod
    def validate_interview_date(cls, v: str) -> str:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("Date must be in YYYY-MM-DD format.")

        try:
            parsed = date.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid date value.")

        today = date.today()

        if parsed < today:
            raise ValueError("Interview date cannot be in the past.")

        if parsed > today + timedelta(days=30):
            raise ValueError("Interview date cannot be more than 1 month in the future.")

        return v

    @field_validator("interview_time")
    @classmethod
    def validate_office_hours(cls, v: str) -> str:
        if not re.match(r"^\d{2}:\d{2}$", v):
            raise ValueError("Time must be in HH:MM format.")

        hour, minute = map(int, v.split(":"))

        if hour > 23 or minute > 59:
            raise ValueError("Invalid time value.")

        if hour < 9 or (hour == 18 and minute > 0) or hour > 18:
            raise ValueError("Interview time must be between 09:00 AM and 06:00 PM.")

        return v

    @field_validator("job_title", "focus_areas")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty or contain only spaces.")

        if value.strip().isdigit():
            raise ValueError("Field cannot contain only numbers.")

        return value.strip()


class InterviewUpdate(BaseModel):
    """Validates interview update payload. All fields optional."""
    job_title:      str | None = Field(default=None, min_length=2, max_length=100)
    interview_date: str | None = None
    interview_time: str | None = None
    interviewer_id: str | None = Field(default=None, min_length=1, max_length=24) 
    focus_areas:    str | None = Field(default=None, min_length=1, max_length=500)
    
    @field_validator("interviewer_id")   
    @classmethod
    def validate_object_id(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.match(OBJECT_ID_PATTERN, v):
            raise ValueError("Must be a valid 24-character ID.")
        return v


    @field_validator("interview_date")
    @classmethod
    def validate_interview_date(cls, v: str | None) -> str | None:
        if v is None:
            return v

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("Date must be in YYYY-MM-DD format.")

        try:
            parsed = date.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid date value.")

        today = date.today()

        if parsed < today:
            raise ValueError("Interview date cannot be in the past.")

        if parsed > today + timedelta(days=180):
            raise ValueError("Interview date cannot be more than 6 months in the future.")

        return v

    @field_validator("interview_time")
    @classmethod
    def validate_office_hours(cls, v: str | None) -> str | None:
        if v is None:
            return v

        if not re.match(r"^\d{2}:\d{2}$", v):
            raise ValueError("Time must be in HH:MM format.")

        hour, minute = map(int, v.split(":"))

        if hour > 23 or minute > 59:
            raise ValueError("Invalid time value.")

        if hour < 9 or (hour == 18 and minute > 0) or hour > 18:
            raise ValueError("Interview time must be between 09:00 AM and 06:00 PM.")

        return v

    @field_validator("job_title", "focus_areas")
    @classmethod
    def validate_non_empty_strings(cls, value: str | None) -> str | None:
        if value is None:
            return value

        if not value.strip():
            raise ValueError("Field cannot be empty or contain only spaces.")

        if value.strip().isdigit():
            raise ValueError("Field cannot contain only numbers.")

        return value.strip()
