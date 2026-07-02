"""
Direct database operations for the Job collection.
"""
from typing import Optional
from src.models.jobs import Job


class JobRepository:

    @staticmethod
    async def create_job(job_document: Job) -> Job:
        await job_document.insert()
        return job_document

    @staticmethod
    async def find_all() -> list[Job]:
        return await Job.find_all().to_list()

    @staticmethod
    async def find_by_id(job_id: str) -> Optional[Job]:
        try:
            return await Job.get(job_id)
        except Exception:
            return None

    @staticmethod
    async def update_job(job_id: str, update_data: dict) -> Optional[Job]:
        job = await JobRepository.find_by_id(job_id)
        if not job:
            return None
        for field, value in update_data.items():
            setattr(job, field, value)
        await job.save()
        return job


job_repository = JobRepository()