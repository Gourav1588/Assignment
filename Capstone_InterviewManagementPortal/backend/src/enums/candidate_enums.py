"""
Enums for Candidate Management module.
"""
from enum import StrEnum


class CandidateStatus(StrEnum):
    PROFILE_CREATED      = "PROFILE_CREATED"
    INTERVIEW_SCHEDULED  = "INTERVIEW_SCHEDULED"
    INTERVIEW_COMPLETED  = "INTERVIEW_COMPLETED"
    SELECTED             = "SELECTED"
    REJECTED             = "REJECTED"