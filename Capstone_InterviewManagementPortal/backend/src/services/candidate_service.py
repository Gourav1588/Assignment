"""
Handles database operations for candidate documents.

Contains:
- email_exists      → Checks whether a candidate email already exists.
- mobile_exists     → Checks whether a candidate mobile number already exists.
- create_candidate  → Inserts a new candidate document.
- find_all          → Retrieves all candidates or filters by status.
- find_by_id        → Retrieves a candidate by ID.
- update_candidate  → Updates an existing candidate document.

"""

import logging
from fastapi import UploadFile
from src.enums.candidate_enums import CandidateStatus
from src.models.candidates import Candidate
from src.models.status_history import StatusHistory
from src.repositories.candidate_repository import candidate_repository
from src.repositories.job_repository import job_repository
from src.schemas.request.candidate_request import CandidateCreate, CandidateUpdate,CandidateStatusUpdate
from src.core.exceptions import ResourceNotFoundException, ConflictException
logger = logging.getLogger(__name__)

MAX_RESUME_BYTES = 10 * 1024 * 1024


class CandidateService:
    """Handles business logic for candidate operations."""

    async def create_candidate(
        self, payload: CandidateCreate, created_by: str
    ) -> Candidate:
        """Create a new candidate."""
        job = await job_repository.find_by_id(payload.applied_job)
        if not job:
            raise ResourceNotFoundException("Applied job not found.")

        if await candidate_repository.email_exists(payload.email.lower()):
            raise ConflictException("A candidate with this email already exists.")

        if await candidate_repository.mobile_exists(payload.mobile_number):
            raise ConflictException(
                "A candidate with this mobile number already exists."
            )

        candidate = Candidate(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email.lower(),
            mobile_number=payload.mobile_number,
            current_company=payload.current_company,
            total_experience=payload.total_experience,
            applied_job=payload.applied_job,
            status=CandidateStatus.PROFILE_CREATED,
            created_by=created_by,
        )

        created = await candidate_repository.create_candidate(candidate)
        logger.info("Candidate created: %s by %s", created.email, created_by)
        return created

    async def list_candidates(
        self, status: CandidateStatus | None = None
    ) -> list[Candidate]:
        """Retrieve all candidates or filter by status."""
        return await candidate_repository.find_all(status)
    

    async def get_candidate(self, candidate_id: str) -> Candidate:
        """Retrieve a candidate by ID."""
        candidate = await candidate_repository.find_by_id(candidate_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate not found.")
        return candidate

    async def update_candidate(
        self, candidate_id: str, payload: CandidateUpdate, updated_by: str
    ) -> Candidate:
        """Update an existing candidate."""
        await self.get_candidate(candidate_id)
        if payload.mobile_number is not None:
            if await candidate_repository.mobile_exists_for_other(
                payload.mobile_number, candidate_id
        ):
                raise ConflictException(
                "A candidate with this mobile number already exists."
        )
        update_data = payload.model_dump(exclude_none=True)
        updated = await candidate_repository.update_candidate(candidate_id, update_data)
        logger.info("Candidate updated: %s by %s", candidate_id, updated_by)
        return updated
    
    async def upload_resume(
        self, candidate_id: str, file: UploadFile, uploaded_by: str
    ) -> Candidate:
        """Validates incoming PDF streams and updates document file bytes."""
        await self.get_candidate(candidate_id)

        if file.content_type != "application/pdf":
            raise ConflictException("Resume must be uploaded in PDF format.")

        data = await file.read()

        if len(data) > MAX_RESUME_BYTES:
            raise ConflictException("Resume file must not exceed 10MB.")

        updated = await candidate_repository.set_resume_data(candidate_id, data)
        logger.info("Resume saved for: %s by %s", candidate_id, uploaded_by)
        return updated

    async def get_resume_bytes(self, candidate_id: str) -> bytes:
        """Returns raw PDF bytes for streaming inline to the browser tab."""
        candidate = await self.get_candidate(candidate_id)
        if not candidate.resume_data:
            raise ResourceNotFoundException(
                "No resume uploaded for this candidate yet."
            )
        return candidate.resume_data

    async def update_status(
        self, candidate_id: str, payload: CandidateStatusUpdate, changed_by: str
    ) -> Candidate:
        """Transitions workflow status positions """
        candidate = await self.get_candidate(candidate_id)
        previous_status = candidate.status
        new_status = payload.status

        updated = await candidate_repository.update_status(candidate_id, new_status)
        await candidate_repository.add_status_history(
            candidate_id=candidate_id,
            previous_status=previous_status,
            new_status=new_status,
            changed_by=changed_by,
        )
        logger.info(
            "Candidate %s status: %s → %s by %s",
            candidate_id, previous_status, new_status, changed_by
        )
        return updated

    async def get_status_history(
        self, candidate_id: str
    ) -> list[StatusHistory]:
        """Collects the complete  history."""
        await self.get_candidate(candidate_id)
        return await candidate_repository.get_status_history(candidate_id)
    
candidate_service = CandidateService()