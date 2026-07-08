"""
Business logic for job description management.

Contains:
- create_job    → creates a new job description
- list_jobs     → returns all job descriptions
- get_job_by_id → returns single job or raises 404
- update_job    → updates provided fields only
"""
import logging
import math
from src.models.jobs import Job
from src.repositories.job_repository import job_repository
from src.schemas.request.job_request import JobCreate, JobUpdate
from src.core.exceptions import ResourceNotFoundException
from src.schemas.response.pagination import PaginatedResponse
from src.schemas.response.job_response import JobResponse


logger = logging.getLogger(__name__)


class JobService:

    async def create_job(self, payload: JobCreate, created_by: str) -> Job:
        job = Job(
            title=payload.title,
            details=payload.details,
            role=payload.role,
            required_skills=payload.required_skills,
            experience_required=payload.experience_required,
            employment_type=payload.employment_type,
            location=payload.location,
            created_by=created_by,
        )
        created = await job_repository.create_job(job)
        logger.info("Job created: %s by %s", created.title, created_by)
        return created

    
    async def list_jobs(
        self, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[JobResponse]:
        """
        Returns a paginated list of job descriptions.
        """
        jobs, total = await job_repository.find_paginated(page, page_size)
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedResponse(
            items=jobs,         
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def get_job_by_id(self, job_id: str) -> Job:
        job = await job_repository.find_by_id(job_id)
        if not job:
            raise ResourceNotFoundException(f"Job with ID '{job_id}' not found.")
        return job

    async def update_job(self, job_id: str, payload: JobUpdate) -> Job:
        await self.get_job_by_id(job_id)
        update_data = payload.model_dump(exclude_none=True)
        updated = await job_repository.update_job(job_id, update_data)
        logger.info("Job updated: %s", job_id)
        return updated


job_service = JobService()