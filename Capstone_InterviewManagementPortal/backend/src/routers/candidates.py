"""
Candidate Management API endpoints.
All endpoints restricted to HR role.

Contains:
- POST /candidates              → create candidate with mandatory PDF resume
- GET  /candidates              → list all candidates with optional status filter
- GET  /candidates/{id}         → get a single candidate by ID
- PUT  /candidates/{id}         → update candidate profile fields
- GET   /candidates/{id}/resume           → view candidate resume
- PATCH /candidates/{id}/status           → update candidate status
- GET   /candidates/{id}/status-history   → retrieve candidate status history
"""
import io
from fastapi import Form
import logging
from fastapi import APIRouter, Depends, Query, status,UploadFile,File
from fastapi.responses import StreamingResponse
from src.models.users import User
from src.enums.candidate_enums import CandidateStatus
from src.schemas.request.candidate_request import CandidateUpdate,CandidateStatusUpdate
from src.schemas.response.candidate_response import CandidateResponse,StatusHistoryResponse
from src.schemas.response.pagination import PaginatedResponse
from src.services.candidate_service import candidate_service
from src.core.dependencies import require_role
from src.enums.roles import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/candidates", tags=["Candidate Management"])


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    current_company: str = Form(...),
    total_experience: float = Form(...),
    applied_job: str = Form(...),
    resume: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """
    Creates a candidate profile with a mandatory PDF resume in one request.
    Sent as multipart/form-data — profile fields and file together.
    Resume cannot be omitted — the backend rejects the request without it.
    """
    logger.info("Create candidate request by: %s", current_user.email)
    return await candidate_service.create_candidate(
      first_name=first_name,
    last_name=last_name,
    email=email,
    mobile_number=mobile_number,
    current_company=current_company,
    total_experience=total_experience,
    applied_job=applied_job,
    resume=resume,
    created_by=current_user.email,
    )


@router.get("", response_model=PaginatedResponse[CandidateResponse])
async def list_candidates(
    page: int = Query(default=1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of records per page"),
    candidate_status: CandidateStatus | None = Query(default=None),
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR retrieves all candidates with an optional status filter."""
    logger.info("List candidates request by: %s", current_user.email)
    return await candidate_service.list_candidates(page=page,page_size=page_size,status=candidate_status)


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR retrieves a single candidate by their ID."""
    logger.info("Get candidate %s request by: %s", candidate_id, current_user.email)
    candidate = await candidate_service.get_candidate(candidate_id)
    last_recommendation = await candidate_service.get_last_recommendation(candidate_id)
    response = CandidateResponse.model_validate(candidate)
    response.last_recommendation = last_recommendation
    return response


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

@router.get("/{candidate_id}/resume")
async def get_resume(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """Streams stored PDF inline so browser opens it in a new tab."""
    logger.info("Resume view for %s by: %s", candidate_id, current_user.email)
    pdf_bytes = await candidate_service.get_resume_bytes(candidate_id)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=resume.pdf"},
    )


@router.patch("/{candidate_id}/status", response_model=CandidateResponse)
async def update_status(
    candidate_id: str,
    payload: CandidateStatusUpdate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR updates candidate status and records transition in history."""
    logger.info("Status update for %s by: %s", candidate_id, current_user.email)
    return await candidate_service.update_status(
        candidate_id, payload, changed_by=current_user.email
    )


@router.get("/{candidate_id}/status-history", response_model=list[StatusHistoryResponse])
async def get_status_history(
    candidate_id: str,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR views the full status transition history for a candidate."""
    logger.info("Status history for %s by: %s", candidate_id, current_user.email)
    return await candidate_service.get_status_history(candidate_id)