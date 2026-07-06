"""
Handles database operations for candidate documents.

Contains:
- email_exists      → Checks if a candidate email already exists.
- mobile_exists     → Checks if a candidate mobile number already exists.
- create_candidate  → Inserts a new candidate document.
- find_all          → Retrieves all candidates or filters by status.
- find_by_id        → Retrieves a candidate by ID.
- update_candidate  → Updates an existing candidate document.
"""

from typing import Optional
from src.models.candidates import Candidate
from src.enums.candidate_enums import CandidateStatus
from src.models.status_history import StatusHistory
from src.schemas.response import candidate_response


class CandidateRepository:
    """Handles database operations for Candidate documents."""

    @staticmethod
    async def email_exists(email: str) -> bool:
        """Check if a candidate email already exists."""
        return await Candidate.find_one(
            Candidate.email == email.lower()
        ) is not None

    @staticmethod
    async def mobile_exists(mobile: str) -> bool:
        """Check if a candidate mobile number already exists."""
        return await Candidate.find_one(
            Candidate.mobile_number == mobile
        ) is not None

    @staticmethod
    async def create_candidate(document: Candidate) -> Candidate:
        """Insert a new candidate document."""
        await document.insert()
        return document

    @staticmethod
    async def find_all(status: CandidateStatus | None = None) -> list[Candidate]:
        """Retrieve all candidates or filter by status."""
        if status:
            return await Candidate.find(Candidate.status == status).project(candidate_response.CandidateResponse).to_list()
        return await Candidate.find_all().project(candidate_response.CandidateResponse).to_list()

    @staticmethod
    async def find_by_id(candidate_id: str) -> Optional[Candidate]:
        """Retrieve a candidate by ID."""
        try:
            return await Candidate.get(candidate_id)
        except Exception:
            return None

    @staticmethod
    async def update_candidate(
        candidate_id: str, update_data: dict
    ) -> Optional[Candidate]:
        """Update an existing candidate."""
        candidate = await CandidateRepository.find_by_id(candidate_id)
        if not candidate:
            return None

        for field, value in update_data.items():
            setattr(candidate, field, value)

        await candidate.save()
        return candidate
    
    @staticmethod
    async def mobile_exists_for_other(mobile: str, candidate_id: str) -> bool:
        """Check if a mobile number exists for another candidate."""
        candidate = await Candidate.find_one(
            Candidate.mobile_number == mobile
        )
        if not candidate:
            return False
        return str(candidate.id) != candidate_id
    
    @staticmethod
    async def set_resume_data(candidate_id: str, data: bytes) -> Optional[Candidate]:
        return await CandidateRepository.update_candidate(
            candidate_id, {"resume_data": data}
        )

    @staticmethod
    async def update_status(
        candidate_id: str, new_status: CandidateStatus
    ) -> Optional[Candidate]:
        return await CandidateRepository.update_candidate(
            candidate_id, {"status": new_status}
        )

    @staticmethod
    async def add_status_history(
        candidate_id: str,
        previous_status: str,
        new_status: str,
        changed_by: str,
    ) -> None:
        await StatusHistory(
            candidate_id=candidate_id,
            previous_status=previous_status,
            new_status=new_status,
            changed_by=changed_by,
        ).insert()

    @staticmethod
    async def get_status_history(candidate_id: str) -> list[StatusHistory]:
        return await StatusHistory.find(
            StatusHistory.candidate_id == candidate_id
        ).sort("changed_at").to_list()


candidate_repository = CandidateRepository()