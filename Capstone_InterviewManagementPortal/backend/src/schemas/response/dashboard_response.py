"""
Response schemas for Dashboard endpoints.
"""
from pydantic import BaseModel


class HRDashboardResponse(BaseModel):
    """Counts for the HR dashboard."""
    total_jobs:           int
    total_candidates:     int
    scheduled_interviews: int
    selected_candidates:  int
    rejected_candidates:  int


class InterviewerDashboardResponse(BaseModel):
    """Counts for the Interviewer dashboard — scoped to current user only."""
    assigned_interviews: int
    pending_feedback:    int
    completed_feedback:  int