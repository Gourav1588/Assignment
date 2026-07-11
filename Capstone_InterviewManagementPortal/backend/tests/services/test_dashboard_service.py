"""
Unit tests for DashboardService business logic.

Contains:
- test_hr_dashboard_empty              → all counts zero on empty DB
- test_hr_dashboard_with_data          → counts match seeded data
- test_hr_dashboard_scheduled_count    → scheduled decreases after feedback
- test_interviewer_dashboard_empty     → all counts zero before assignment
- test_interviewer_dashboard_assigned  → assigned count after interview created
- test_interviewer_dashboard_completed → completed count after feedback submitted
"""
from src.services.dashboard_service import DashboardService
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.models.feedback import Feedback
from src.models.status_history import StatusHistory
from src.enums.candidate_enums import CandidateStatus
from src.enums.interview_enums import RecommendationEnum
from src.schemas.request.feedback_request import FeedbackCreate
from src.services.feedback_service import FeedbackService
from src.services.interview_service import interview_service
from tests.helpers import (
    seed_interviewer, seed_job, seed_candidate,
    create_interview_via_service,
)

service           = DashboardService()
feedback_service  = FeedbackService()


async def submit_feedback(interview_id: str, interviewer_id: str) -> None:
    """Submits feedback for an interview."""
    await feedback_service.submit_feedback(
        interview_id=interview_id,
        payload=FeedbackCreate(
            technical_rating=4,
            communication_rating=3,
            problem_solving=5,
            tech_areas_covered="Python",
            comments="Good",
            recommendation=RecommendationEnum.SELECT,
        ),
        submitted_by_id=interviewer_id,
    )


async def test_hr_dashboard_empty():
    """All counts are zero when DB is empty."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    result = await service.get_hr_dashboard()
    assert result.total_jobs == 0
    assert result.total_candidates == 0
    assert result.scheduled_interviews == 0
    assert result.selected_candidates == 0
    assert result.rejected_candidates == 0


async def test_hr_dashboard_with_data():
    """Counts match the seeded data."""
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

    result = await service.get_hr_dashboard()
    assert result.total_jobs == 1
    assert result.total_candidates == 1
    assert result.scheduled_interviews == 1
    assert result.selected_candidates == 0
    assert result.rejected_candidates == 0


async def test_hr_dashboard_scheduled_count():
    """Scheduled count decreases after feedback is submitted."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    from src.services.interview_service import InterviewService
    interview_service = InterviewService()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    result = await service.get_hr_dashboard()
    assert result.scheduled_interviews == 1

    await submit_feedback(str(created.id), str(interviewer.id))

    result = await service.get_hr_dashboard()
    assert result.scheduled_interviews == 0


async def test_hr_dashboard_selected_rejected():
    """Selected and rejected counts match candidate statuses."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()
    await StatusHistory.all().delete()

    job = await seed_job()
    await seed_candidate(str(job.id), email="selected@gmail.com", mobile="9876543210")
    await seed_candidate(str(job.id), email="rejected@gmail.com", mobile="9876543211")

    # manually set statuses
    from src.models.candidates import Candidate as CandidateModel
    selected = await CandidateModel.find_one({"email": "selected@gmail.com"})
    selected.status = CandidateStatus.SELECTED
    await selected.save()

    rejected = await CandidateModel.find_one({"email": "rejected@gmail.com"})
    rejected.status = CandidateStatus.REJECTED
    await rejected.save()

    result = await service.get_hr_dashboard()
    assert result.selected_candidates == 1
    assert result.rejected_candidates == 1


async def test_interviewer_dashboard_empty():
    """All counts zero before any interview is assigned."""
    await User.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    interviewer = await seed_interviewer()

    result = await service.get_interviewer_dashboard(str(interviewer.id))
    assert result.assigned_interviews == 0
    assert result.pending_feedback == 0
    assert result.completed_feedback == 0


async def test_interviewer_dashboard_assigned():
    """Assigned count increases after interview is created."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    from src.services.interview_service import InterviewService
    interview_service = InterviewService()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    result = await service.get_interviewer_dashboard(str(interviewer.id))
    assert result.assigned_interviews == 1
    assert result.pending_feedback == 1
    assert result.completed_feedback == 0


async def test_interviewer_dashboard_completed():
    """Completed count increases after feedback is submitted."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    from src.services.interview_service import InterviewService
    interview_service = InterviewService()

    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    created = await create_interview_via_service(
        interview_service, str(candidate.id), str(interviewer.id)
    )

    await submit_feedback(str(created.id), str(interviewer.id))

    result = await service.get_interviewer_dashboard(str(interviewer.id))
    assert result.assigned_interviews == 1
    assert result.pending_feedback == 0
    assert result.completed_feedback == 1