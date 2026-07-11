"""
Shared helpers for interpreting interview date and time strings.
"""
from datetime import datetime


def interview_datetime(interview_date: str, interview_time: str) -> datetime:
    """Combines the stored date and time strings into a single datetime."""
    return datetime.fromisoformat(f"{interview_date}T{interview_time}")


def has_interview_passed(interview_date: str, interview_time: str) -> bool:
    """Returns True once the interview's scheduled start time has elapsed."""
    return datetime.now() > interview_datetime(interview_date, interview_time)