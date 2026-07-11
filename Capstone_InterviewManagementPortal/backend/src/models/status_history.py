"""
Defines the StatusHistory database model.
Tracks candidate workflow state changes.
"""
from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class StatusHistory(Document):
    """
    Database document for candidate status history.
    Logs previous and new states with timestamps and author details.
    """
    candidate_id: str
    previous_status: str
    new_status: str
    changed_by: str
    changed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "status_history"