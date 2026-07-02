"""
Unit tests for JobService business logic.

Contains:
- test_create_job_success      → job created with correct fields
- test_list_jobs               → returns all jobs
- test_get_job_by_id_success   → returns correct job by ID
- test_get_job_by_id_not_found → raises ResourceNotFoundException
- test_update_job_success      → updates only provided fields
- test_update_job_not_found    → raises ResourceNotFoundException
"""
import pytest
from src.services.job_service import JobService
from src.models.jobs import Job
from src.schemas.request.job_request import JobCreate, JobUpdate
from src.core.exceptions import ResourceNotFoundException

service = JobService()


def make_payload(**kwargs) -> JobCreate:
    defaults = {
        "title": "Backend Developer",
        "details": "We are looking for a skilled backend developer.",
        "role": "Software Engineer",
        "required_skills": "Python, FastAPI, MongoDB",
        "experience_required": 2,
        "employment_type": "Full Time",
        "location": "Bangalore",
    }
    defaults.update(kwargs)
    return JobCreate(**defaults)


async def seed_job() -> Job:
    job = Job(
        title="Backend Developer",
        details="We are looking for a skilled backend developer.",
        role="Software Engineer",
        required_skills="Python, FastAPI",
        experience_required=2,
        employment_type="Full Time",
        location="Bangalore",
        created_by="hr@nucleusteq.com",
    )
    await job.insert()
    return job


async def test_create_job_success():
    """Job created with all correct fields and creator email."""
    await Job.all().delete()
    job = await service.create_job(make_payload(), created_by="hr@nucleusteq.com")

    assert job.title == "Backend Developer"
    assert job.details == "We are looking for a skilled backend developer."
    assert job.role == "Software Engineer"
    assert job.employment_type == "Full Time"
    assert job.created_by == "hr@nucleusteq.com"


async def test_list_jobs():
    """Returns all jobs in the system."""
    await Job.all().delete()
    await seed_job()
    await service.create_job(
        make_payload(title="Frontend Developer"),
        created_by="hr@nucleusteq.com"
    )

    jobs = await service.list_jobs()
    assert len(jobs) == 2


async def test_get_job_by_id_success():
    """Returns the correct job for a valid ID."""
    await Job.all().delete()
    created = await seed_job()

    found = await service.get_job_by_id(str(created.id))
    assert found.title == "Backend Developer"
    assert found.role == "Software Engineer"


async def test_get_job_by_id_not_found():
    """Non-existent ID raises ResourceNotFoundException."""
    await Job.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.get_job_by_id("000000000000000000000000")


async def test_update_job_success():
    await Job.all().delete()
    created = await seed_job()

    updated = await service.update_job(
        str(created.id),
        JobUpdate(title="Senior Backend Developer", employment_type="Internship")
    )
    assert updated.title == "Senior Backend Developer"
    assert updated.employment_type == "Internship"
    assert updated.location == "Bangalore"   
    assert updated.role == "Software Engineer"  


async def test_update_job_not_found():
    """Non-existent ID raises ResourceNotFoundException."""
    await Job.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.update_job(
            "000000000000000000000000",
            JobUpdate(title="Updated Title")
        )