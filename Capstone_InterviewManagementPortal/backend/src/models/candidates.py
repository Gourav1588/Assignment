"""
Beanie document model representing candidate records stored in MongoDB.
"""

from beanie import Document
from src.enums.candidate_enums import CandidateStatus


class Candidate(Document):
    """
    Stores candidate profile information along with the current interview status.
    """

    first_name: str
    last_name: str
    email: str
    mobile_number: str
    current_company: str
    total_experience: float
    applied_job: str
    resume_data: bytes | None = None
    status: CandidateStatus = CandidateStatus.PROFILE_CREATED
    created_by: str

    class Settings:
        """
        Beanie configuration for the Candidate document.
        """

        # MongoDB collection name.
        name = "candidates"