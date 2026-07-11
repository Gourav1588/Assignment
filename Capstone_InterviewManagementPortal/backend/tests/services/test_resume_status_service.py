"""
Unit tests for resume access and status tracking service logic.
Contains:
- test_get_resume_bytes_success        → returns PDF bytes when resume exists
- test_get_resume_bytes_not_found      → raises ResourceNotFoundException when missing
- test_update_status_success           → forward transition succeeds
- test_update_status_invalid_transition → backward/skip transition raises ConflictException
- test_update_status_terminal_state    → updating terminal status raises ConflictException
- test_update_status_records_history   → previous status captured in history
- test_get_status_history_multiple     → returns transitions in correct order
- test_get_status_history_empty        → empty list before any change
"""

import pytest
from src.services.candidate_service import CandidateService
from src.models.candidates import Candidate
from src.models.jobs import Job
from src.models.status_history import StatusHistory
from src.schemas.request.candidate_request import CandidateStatusUpdate
from src.enums.candidate_enums import CandidateStatus
from src.core.exceptions import ResourceNotFoundException, ConflictException
from tests.helpers import seed_job, seed_candidate

service = CandidateService()

async def test_get_resume_bytes_success():
    """Returns PDF bytes when resume exists."""
    await Candidate.all().delete()
    await Job.all().delete()

    job = await seed_job()
    created = await seed_candidate(str(job.id))
    
    pdf_bytes = await service.get_resume_bytes(str(created.id))
    assert bytes(pdf_bytes)== b"%PDF-1.4 fake"
    


async def test_get_resume_bytes_not_found():
    """Raises ResourceNotFoundException when no resume uploaded."""
    await Candidate.all().delete()
    await Job.all().delete()
    job = await seed_job()
    created = await seed_candidate(str(job.id), resume_data=None)

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

async def test_update_status_invalid_transition():
    """Skipping a status step raises ConflictException."""
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    with pytest.raises(ConflictException):
        await service.update_status(
            str(created.id),
            CandidateStatusUpdate(status=CandidateStatus.INTERVIEW_COMPLETED),
            changed_by="hr@nucleusteq.com",
        )
        
async def test_update_status_terminal_state():
    """Updating from a terminal status raises ConflictException."""
    await Candidate.all().delete()
    await Job.all().delete()
    await StatusHistory.all().delete()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Move to terminal state step by step
    await service.update_status(
        str(created.id),
        CandidateStatusUpdate(status=CandidateStatus.INTERVIEW_SCHEDULED),
        changed_by="hr@nucleusteq.com",
    )
    await service.update_status(
        str(created.id),
        CandidateStatusUpdate(status=CandidateStatus.INTERVIEW_COMPLETED),
        changed_by="hr@nucleusteq.com",
    )
    await service.update_status(
        str(created.id),
        CandidateStatusUpdate(status=CandidateStatus.SELECTED),
        changed_by="hr@nucleusteq.com",
    )

    with pytest.raises(ConflictException):
        await service.update_status(
            str(created.id),
            CandidateStatusUpdate(status=CandidateStatus.REJECTED),
            changed_by="hr@nucleusteq.com",
        )

async def test_update_status_records_history():
    """Previous and new status both captured in history."""
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