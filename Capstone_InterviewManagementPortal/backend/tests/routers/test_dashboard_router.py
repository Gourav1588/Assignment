"""
Integration tests for Dashboard API endpoints.

Contains:
- test_hr_dashboard_success              → HR gets dashboard counts
- test_hr_dashboard_as_interviewer       → Interviewer blocked (403)
- test_hr_dashboard_as_admin             → Admin blocked (403)
- test_interviewer_dashboard_success     → Interviewer gets their counts
- test_interviewer_dashboard_as_hr       → HR blocked (403)
- test_hr_dashboard_counts_correct       → counts match actual data
- test_interviewer_dashboard_counts      → counts match actual data
"""
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.models.feedback import Feedback
from src.models.status_history import StatusHistory
from tests.helpers import (
    auth_header, seed_admin, seed_hr, seed_interviewer,
    seed_job, seed_candidate, feedback_payload,
    create_interview_via_api,
)


async def test_hr_dashboard_success(client):
    """HR can access the dashboard."""
    await User.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/dashboard/hr",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert "total_jobs" in response.json()
    assert "total_candidates" in response.json()
    assert "scheduled_interviews" in response.json()
    assert "selected_candidates" in response.json()
    assert "rejected_candidates" in response.json()


async def test_hr_dashboard_as_interviewer(client):
    """Interviewer cannot access HR dashboard."""
    await User.all().delete()
    await seed_interviewer()

    response = await client.get(
        "/api/v1/dashboard/hr",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 403


async def test_hr_dashboard_as_admin(client):
    """Admin cannot access HR dashboard."""
    await User.all().delete()
    await seed_admin()

    response = await client.get(
        "/api/v1/dashboard/hr",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 403


async def test_interviewer_dashboard_success(client):
    """Interviewer can access their dashboard."""
    await User.all().delete()
    await seed_interviewer()

    response = await client.get(
        "/api/v1/dashboard/interviewer",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 200
    assert "assigned_interviews" in response.json()
    assert "pending_feedback" in response.json()
    assert "completed_feedback" in response.json()


async def test_interviewer_dashboard_as_hr(client):
    """HR cannot access Interviewer dashboard."""
    await User.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/dashboard/interviewer",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 403


async def test_hr_dashboard_counts_correct(client):
    """Dashboard counts match actual data in the system."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()
    await StatusHistory.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview = await create_interview_via_api(
        client, str(candidate.id), str(interviewer.id)
    )

    response = await client.get(
        "/api/v1/dashboard/hr",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["total_candidates"] == 1
    assert data["scheduled_interviews"] == 1   # interview exists, no feedback yet
    assert data["selected_candidates"] == 0
    assert data["rejected_candidates"] == 0

    # submit feedback
    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    response = await client.get(
        "/api/v1/dashboard/hr",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    data = response.json()
    assert data["scheduled_interviews"] == 0   # feedback submitted so no longer scheduled


async def test_interviewer_dashboard_counts(client):
    """Interviewer dashboard counts match actual assigned interviews."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview = await create_interview_via_api(
        client, str(candidate.id), str(interviewer.id)
    )

    response = await client.get(
        "/api/v1/dashboard/interviewer",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    data = response.json()
    assert data["assigned_interviews"] == 1
    assert data["pending_feedback"] == 1    # interview assigned, no feedback yet
    assert data["completed_feedback"] == 0

    # submit feedback
    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    response = await client.get(
        "/api/v1/dashboard/interviewer",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    data = response.json()
    assert data["assigned_interviews"] == 1
    assert data["pending_feedback"] == 0    # feedback submitted
    assert data["completed_feedback"] == 1