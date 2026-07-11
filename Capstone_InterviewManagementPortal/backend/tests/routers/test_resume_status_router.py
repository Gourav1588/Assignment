"""
Integration tests for resume and status tracking API endpoints.

Contains:
- test_get_resume_success              → PDF streamed successfully
- test_get_resume_candidate_not_found  → unknown candidate returns 404
- test_update_status_success           → valid transition returns 200
- test_update_status_invalid_value     → unknown status value returns 422
- test_update_status_invalid_transition → backward transition returns 409
- test_update_status_terminal_state    → updating terminal status returns 409
- test_get_status_history_success      → returns history after status change
- test_get_status_history_empty        → empty list before any change
"""

from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.status_history import StatusHistory
from tests.helpers import auth_header, seed_hr, seed_job, seed_candidate


async def test_get_resume_success(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    response = await client.get(
        f"/api/v1/candidates/{created.id}/resume",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


async def test_get_resume_candidate_not_found(client):
    """Unknown candidate ID returns 404."""
    await User.all().delete()
    await Candidate.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/candidates/000000000000000000000000/resume",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404



async def test_update_status_success(client):
    """Valid forward transition returns 200."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await StatusHistory.all().delete()
    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    response = await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "INTERVIEW_SCHEDULED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "INTERVIEW_SCHEDULED"


async def test_update_status_invalid(client):
    """Unknown status value returns 422."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    response = await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "WRONG_STATUS"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 422
    
async def test_update_status_invalid_transition(client):
    """Skipping a status step returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await StatusHistory.all().delete()
    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    response = await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "INTERVIEW_COMPLETED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409
    
async def test_update_status_terminal_state(client):
    """Updating a terminal status returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await StatusHistory.all().delete()
    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Move to terminal state
    await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "INTERVIEW_SCHEDULED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "INTERVIEW_COMPLETED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "SELECTED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    # Try to change from terminal state
    response = await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "REJECTED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409


async def test_get_status_history_success(client):
    """Returns history after a status change."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await StatusHistory.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Create a status change before fetching history
    await client.patch(
        f"/api/v1/candidates/{created.id}/status",
        json={"status": "INTERVIEW_SCHEDULED"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    response = await client.get(
        f"/api/v1/candidates/{created.id}/status-history",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["new_status"] == "INTERVIEW_SCHEDULED"


async def test_get_status_history_empty(client):
    """Empty list before any status change."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await StatusHistory.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    response = await client.get(
        f"/api/v1/candidates/{created.id}/status-history",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 200
    assert len(response.json()) == 0