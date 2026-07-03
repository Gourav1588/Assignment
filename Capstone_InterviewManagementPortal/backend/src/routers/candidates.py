"""
Candidate Management API endpoints.
All endpoints restricted to HR role.

Contains:
- POST /candidates              → create a new candidate profile
- GET  /candidates              → list all candidates with optional status filter
- GET  /candidates/{id}         → get a single candidate by ID
- PUT  /candidates/{id}         → update candidate profile fields
"""
import logging
from fastapi import APIRouter, Depends, Query, status
from src.models.users import User
from src.enums.candidate_enums import CandidateStatus
from src.schemas.request.candidate_request import CandidateCreate, CandidateUpdate
from src.schemas.response.candidate_response import CandidateResponse
from src.services.candidate_service import candidate_service
from src.core.dependencies import require_role
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/candidates", tags=["Candidate Management"])


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    payload: CandidateCreate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR creates a new candidate profile with default PROFILE_CREATED status."""
    logger.info("Create candidate request by: %s", current_user.email)
    return await candidate_service.create_candidate(
        payload, created_by=current_user.email
    )


@router.get("", response_model=list[CandidateResponse])
async def list_candidates(
    candidate_status: CandidateStatus | None = Query(default=None),
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR retrieves all candidates with an optional status filter."""
    logger.info("List candidates request by: %s", current_user.email)
    return await candidate_service.list_candidates(candidate_status)


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR retrieves a single candidate by their ID."""
    logger.info("Get candidate %s request by: %s", candidate_id, current_user.email)
    return await candidate_service.get_candidate(candidate_id)


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: str,
    payload: CandidateUpdate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR updates allowed candidate profile fields."""
    logger.info("Update candidate %s request by: %s", candidate_id, current_user.email)
    return await candidate_service.update_candidate(
        candidate_id, payload, updated_by=current_user.email
    )