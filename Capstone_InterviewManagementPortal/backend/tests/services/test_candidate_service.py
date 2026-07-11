"""
Unit tests for CandidateService business logic.

Contains:
- test_create_candidate_success          → candidate created with PROFILE_CREATED status
- test_create_candidate_duplicate_email  → duplicate email raises ConflictException
- test_create_candidate_duplicate_mobile → duplicate mobile raises ConflictException
- test_create_candidate_invalid_job      → non-existent job raises ResourceNotFoundException
- test_create_candidate_invalid_resume   → non-PDF raises ConflictException
- test_list_candidates                   → returns all candidates
- test_list_candidates_by_status         → filters by status correctly
- test_get_candidate_not_found           → raises ResourceNotFoundException
- test_update_candidate_success          → updates provided fields only
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.candidate_service import CandidateService
from src.models.candidates import Candidate
from src.models.jobs import Job
from src.schemas.request.candidate_request import  CandidateUpdate
from src.enums.candidate_enums import CandidateStatus
from src.core.exceptions import ResourceNotFoundException, ConflictException
from tests.helpers import seed_job, seed_candidate

service = CandidateService()

def make_pdf_file(content_type: str = "application/pdf") -> MagicMock:
    """Returns a mock UploadFile with PDF content."""
    mock_file = MagicMock()
    mock_file.content_type = content_type
    mock_file.read = AsyncMock(return_value=b"%PDF-1.4 fake content")
    return mock_file

async def create_candidate_via_service(job_id: str, **kwargs) -> Candidate:
    defaults = dict(
        first_name="Rahul",
        last_name="Sharma",
        email="rahul@gmail.com",
        mobile_number="9876543210",
        current_company="ABC Corp",
        total_experience=3.0,
        applied_job=job_id,
        resume=make_pdf_file(),
        created_by="hr@nucleusteq.com",
    )
    defaults.update(kwargs)
    return await service.create_candidate(**defaults)


async def test_create_candidate_success():
    """Candidate created with resume and PROFILE_CREATED status."""
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()

    candidate = await create_candidate_via_service(str(job.id))
    assert candidate.email == "rahul@gmail.com"
    assert candidate.status == CandidateStatus.PROFILE_CREATED
    assert candidate.resume_data is not None



async def test_create_candidate_duplicate_email():
    """Duplicate email raises ConflictException."""
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()

    await create_candidate_via_service(str(job.id))
    with pytest.raises(ConflictException):
        await create_candidate_via_service(str(job.id))

async def test_create_candidate_duplicate_mobile():
    """Duplicate mobile raises ConflictException."""
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()

    
    await create_candidate_via_service(str(job.id))
    with pytest.raises(ConflictException):
        await create_candidate_via_service(str(job.id), email="other@gmail.com")


async def test_create_candidate_invalid_job():
    await Candidate.all().delete()
    await Job.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await create_candidate_via_service("000000000000000000000000")


async def test_create_candidate_invalid_resume():
    """Non-PDF file raises ConflictException."""
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()

    with pytest.raises(ConflictException):
        await create_candidate_via_service(
            str(job.id),
            resume=make_pdf_file(content_type="image/png"),
        )

async def test_list_candidates():
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()
    await seed_candidate(job_id=str(job.id))
    await seed_candidate(
        email="other@gmail.com",
        mobile="9876543211",
        job_id=str(job.id)
    )

    result = await service.list_candidates(page=1,page_size=10)
    assert result.total == 2
    assert len(result.items)==2

async def test_list_candidates_by_status():
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()
    await seed_candidate(job_id=str(job.id))

    results = await service.list_candidates(
        page=1,page_size=10,
        status=CandidateStatus.PROFILE_CREATED
    )
    assert len(results.items) == 1

    empty = await service.list_candidates(
        page=1, page_size=10,
        status=CandidateStatus.SELECTED
    )
    assert len(empty.items) == 0


async def test_get_candidate_not_found():
    await Candidate.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.get_candidate("000000000000000000000000")


async def test_update_candidate_success():
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()
    created = await seed_candidate(job_id=str(job.id))

    updated = await service.update_candidate(
        str(created.id),
        CandidateUpdate(current_company="XYZ Corp", total_experience=5.0),
        updated_by="hr@nucleusteq.com",
    )
    assert updated.current_company == "XYZ Corp"
    assert updated.total_experience == 5.0
    assert updated.email == "rahul@gmail.com"