"""
Unit tests for InterviewService business logic.
"""
import pytest
from src.services.interview_service import InterviewService
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.schemas.request.interview_request import InterviewUpdate
from src.core.exceptions import (
    ResourceNotFoundException,
    ConflictException,
    ForbiddenException,
)
from tests.helpers import (
    seed_hr, seed_interviewer, seed_job, seed_candidate,
    create_interview_via_service,
)

service = InterviewService()


async def test_create_interview_success():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    result = await create_interview_via_service(service, str(candidate.id), str(interviewer.id))
    assert result.candidate_id == str(candidate.id)
    assert result.interviewer_id == str(interviewer.id)
    assert result.scheduled_by == "hr@nucleusteq.com"


async def test_create_interview_invalid_candidate():
    await User.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()

    with pytest.raises(ResourceNotFoundException):
        await create_interview_via_service(service, "000000000000000000000000", str(interviewer.id))


async def test_create_interview_invalid_interviewer():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    with pytest.raises(ResourceNotFoundException):
        await create_interview_via_service(service, str(candidate.id), "000000000000000000000000")


async def test_create_interview_wrong_role():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    hr = await seed_hr()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    with pytest.raises(ConflictException):
        await create_interview_via_service(service, str(candidate.id), str(hr.id))


async def test_list_interviews():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    result = await service.list_interviews(page=1, page_size=10)
    assert result.total == 1
    assert len(result.items) == 1


async def test_my_interviews():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    result = await service.my_interviews(
        interviewer_id=str(interviewer.id), page=1, page_size=10
    )
    assert result.total == 1
    assert result.items[0].interviewer_id == str(interviewer.id)


async def test_get_interview_not_found():
    await Interview.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.get_interview(
            "000000000000000000000000",
            current_user_id="any",
            current_user_role="HR",
        )


async def test_get_interview_admin_blocked():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    with pytest.raises(ForbiddenException):
        await service.get_interview(
            str(created.id),
            current_user_id="admin_id",
            current_user_role="Admin",
        )


async def test_get_interview_wrong_interviewer():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    with pytest.raises(ForbiddenException):
        await service.get_interview(
            str(created.id),
            current_user_id="different_id",
            current_user_role="Interviewer",
        )


async def test_update_interview_success():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    updated = await service.update_interview(
        str(created.id),
        InterviewUpdate(interview_date="2024-09-01", interview_time="14:00"),
        updated_by="hr@nucleusteq.com",
    )
    assert updated.interview_date == "2024-09-01"
    assert updated.interview_time == "14:00"
    assert updated.focus_areas == "Python, FastAPI"


async def test_update_interview_wrong_role():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    hr = await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(service, str(candidate.id), str(interviewer.id))

    with pytest.raises(ConflictException):
        await service.update_interview(
            str(created.id),
            InterviewUpdate(interviewer_id=str(hr.id)),
            updated_by="hr@nucleusteq.com",
        )