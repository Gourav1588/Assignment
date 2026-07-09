"""
Unit tests for FeedbackService business logic.
"""
import pytest
from src.services.interview_service import InterviewService
from src.services.feedback_service import FeedbackService
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.models.feedback import Feedback
from src.schemas.request.feedback_request import FeedbackCreate
from src.enums.interview_enums import RecommendationEnum
from src.core.exceptions import (
    ResourceNotFoundException,
    ConflictException,
    ForbiddenException,
)
from tests.helpers import (
    seed_interviewer, seed_job, seed_candidate,
    create_interview_via_service,
)

interview_service = InterviewService()
feedback_service  = FeedbackService()


def make_feedback_payload(**kwargs) -> FeedbackCreate:
    defaults = dict(
        technical_rating=4,
        communication_rating=3,
        problem_solving=5,
        tech_areas_covered="Python, APIs",
        comments="Good candidate",
        recommendation=RecommendationEnum.SELECT,
    )
    defaults.update(kwargs)
    return FeedbackCreate(**defaults)


async def test_submit_feedback_success():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    result = await feedback_service.submit_feedback(
        interview_id=str(created.id),
        payload=make_feedback_payload(),
        submitted_by_id=str(interviewer.id),
    )
    assert result.recommendation == RecommendationEnum.SELECT
    assert result.technical_rating == 4
    assert result.interview_id == str(created.id)


async def test_submit_feedback_wrong_interviewer():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    with pytest.raises(ForbiddenException):
        await feedback_service.submit_feedback(
            interview_id=str(created.id),
            payload=make_feedback_payload(),
            submitted_by_id="different_id",
        )


async def test_submit_feedback_duplicate():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    await feedback_service.submit_feedback(
        interview_id=str(created.id),
        payload=make_feedback_payload(),
        submitted_by_id=str(interviewer.id),
    )

    with pytest.raises(ConflictException):
        await feedback_service.submit_feedback(
            interview_id=str(created.id),
            payload=make_feedback_payload(),
            submitted_by_id=str(interviewer.id),
        )


async def test_get_feedback_success():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    await feedback_service.submit_feedback(
        interview_id=str(created.id),
        payload=make_feedback_payload(),
        submitted_by_id=str(interviewer.id),
    )

    result = await feedback_service.get_feedback(
        interview_id=str(created.id),
        current_user_id="hr_id",
        current_user_role="HR",
    )
    assert result.interview_id == str(created.id)
    assert result.recommendation == RecommendationEnum.SELECT


async def test_get_feedback_admin_blocked():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    with pytest.raises(ForbiddenException):
        await feedback_service.get_feedback(
            interview_id=str(created.id),
            current_user_id="admin_id",
            current_user_role="Admin",
        )


async def test_get_feedback_wrong_interviewer():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    await feedback_service.submit_feedback(
        interview_id=str(created.id),
        payload=make_feedback_payload(),
        submitted_by_id=str(interviewer.id),
    )

    with pytest.raises(ForbiddenException):
        await feedback_service.get_feedback(
            interview_id=str(created.id),
            current_user_id="different_id",
            current_user_role="Interviewer",
        )


async def test_get_feedback_not_found():
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    with pytest.raises(ResourceNotFoundException):
        await feedback_service.get_feedback(
            interview_id=str(created.id),
            current_user_id="hr_id",
            current_user_role="HR",
        )