"""
Job Description API endpoints.
All endpoints restricted to HR.

Contains:
- POST /jobs           → create a job description
- GET  /jobs           → list all job descriptions
- GET  /jobs/{job_id}  → get a single job description
- PUT  /jobs/{job_id}  → update a job description
"""
import logging
from fastapi import APIRouter, Depends, status
from src.models.users import User
from src.schemas.request.job_request import JobCreate, JobUpdate
from src.schemas.response.job_response import JobResponse
from src.services.job_service import job_service
from src.core.dependencies import  require_role
from src.enums.roles import UserRole
logger =logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Job Description"])


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreate,
    current_user: User = Depends(require_role(UserRole.HR)),
):
    """HR creates a new job description."""
    logger.info(f"Create job request received from {current_user.email}")
    return await job_service.create_job(payload, created_by=current_user.email)


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    _=Depends(require_role(UserRole.HR)),
):
    """HR retrieves all job descriptions."""
    logger.info("List jobs request received.")
    return await job_service.list_jobs()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    _=Depends(require_role(UserRole.HR)),
):
    """HR retrieves a single job description by ID."""
    logger.info(f"Get job request received for ID: {job_id}")
    return await job_service.get_job_by_id(job_id)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    payload: JobUpdate,
    _=Depends(require_role(UserRole.HR)),
):
    """HR updates an existing job description."""
    logger.info(f"Update job request received for ID: {job_id}")
    return await job_service.update_job(job_id, payload)