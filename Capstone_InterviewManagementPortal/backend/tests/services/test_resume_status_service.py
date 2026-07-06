"""
Unit tests for resume upload and status tracking service logic.
Validated against raw database document return formats.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.candidate_service import CandidateService
from src.models.candidates import Candidate
from src.models.jobs import Job
from src.models.status_history import StatusHistory
from src.schemas.request.candidate_request import CandidateStatusUpdate
from src.enums.candidate_enums import CandidateStatus
from src.core.exceptions import ResourceNotFoundException, ConflictException

service = CandidateService()


async def seed_job() -> Job:
    """Create a sample job for candidate mapping."""
    job = Job(
        title="Backend Developer",
        details="Looking for a backend developer.",
        role="Software Engineer",
        required_skills="Python",
        experience_required=2,
        employment_type="Full Time",
        location="Bangalore",
        created_by="hr@nucleusteq.com",
    )
    await job.insert()
    return job


async def seed_candidate(job_id: str) -> Candidate:
    """Create a sample candidate linked to a job."""
    candidate = Candidate(
        first_name="Rahul",
        last_name="Sharma",
        email="rahul@gmail.com",
        mobile_number="9876543210",
        current_company="ABC Corp",
        total_experience=3.0,
        applied_job=job_id,
        status=CandidateStatus.PROFILE_CREATED,
        created_by="hr@nucleusteq.com",
    )
    await candidate.insert()
    return candidate


async def test_upload_resume_success():
    await Candidate.all().delete()
    await Job.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Mock a valid PDF upload
    mock_file = MagicMock()
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"%PDF-1.4 fake content")

    response = await service.upload_resume(
        str(created.id), mock_file, uploaded_by="hr@nucleusteq.com"
    )

    assert response.resume_data is not None


async def test_upload_resume_invalid_format():
    await Candidate.all().delete()
    await Job.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Mock an unsupported file type
    mock_file = MagicMock()
    mock_file.content_type = "image/png"
    mock_file.read = AsyncMock(return_value=b"fake image")

    with pytest.raises(ConflictException):
        await service.upload_resume(
            str(created.id), mock_file, uploaded_by="hr@nucleusteq.com"
        )


async def test_upload_resume_exceeds_limit():
    await Candidate.all().delete()
    await Job.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Mock a file larger than the allowed limit
    mock_file = MagicMock()
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"x" * (11 * 1024 * 1024))

    with pytest.raises(ConflictException):
        await service.upload_resume(
            str(created.id), mock_file, uploaded_by="hr@nucleusteq.com"
        )


async def test_get_resume_bytes_not_uploaded():
    await Candidate.all().delete()
    await Job.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    with pytest.raises(ResourceNotFoundException):
        await service.get_resume_bytes(str(created.id))


async def test_update_status_success():
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    updated = await service.update_status(
        str(created.id),
        CandidateStatusUpdate(status=CandidateStatus.INTERVIEW_SCHEDULED),
        changed_by="hr@nucleusteq.com",
    )

    assert updated.status == CandidateStatus.INTERVIEW_SCHEDULED


async def test_update_status_records_history():
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    await service.update_status(
        str(created.id),
        CandidateStatusUpdate(status=CandidateStatus.INTERVIEW_SCHEDULED),
        changed_by="hr@nucleusteq.com",
    )

    history = await service.get_status_history(str(created.id))

    assert len(history) == 1
    assert history[0].previous_status == CandidateStatus.PROFILE_CREATED
    assert history[0].new_status == CandidateStatus.INTERVIEW_SCHEDULED


async def test_get_status_history_multiple():
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Apply multiple status updates
    for s in [
        CandidateStatus.INTERVIEW_SCHEDULED,
        CandidateStatus.INTERVIEW_COMPLETED,
        CandidateStatus.SELECTED,
    ]:
        await service.update_status(
            str(created.id),
            CandidateStatusUpdate(status=s),
            changed_by="hr@nucleusteq.com",
        )

    history = await service.get_status_history(str(created.id))

    assert len(history) == 3
    assert history[0].new_status == CandidateStatus.INTERVIEW_SCHEDULED
    assert history[2].new_status == CandidateStatus.SELECTED


async def test_get_status_history_empty():
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))

    history = await service.get_status_history(str(created.id))

    assert len(history) == 0