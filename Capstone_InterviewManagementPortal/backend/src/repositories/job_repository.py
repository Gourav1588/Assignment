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
    async def find_paginated(page: int, page_size: int) -> tuple[list[Job], int]:
        """
        Returns a page of jobs and the total count.
        skip calculates how many records to jump over based on current page.
        """
        skip = (page - 1) * page_size
        total = await Job.count()
        jobs = await Job.find_all().sort("-_id").skip(skip).limit(page_size).to_list()
        return jobs, total

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