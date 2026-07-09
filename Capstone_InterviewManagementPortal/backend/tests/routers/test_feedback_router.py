"""
Integration tests for Feedback API endpoints.
"""
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.models.feedback import Feedback
from tests.helpers import (
    auth_header, seed_admin, seed_hr, seed_interviewer,
    seed_job, seed_candidate, feedback_payload,
    create_interview_via_api,  
)

async def test_submit_feedback_success(client):
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

    response = await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 200
    assert response.json()["recommendation"] == "SELECT"
    assert response.json()["technical_rating"] == 4


async def test_submit_feedback_wrong_interviewer(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    await seed_hr()
    interviewer1 = await seed_interviewer()
    interviewer2 = await seed_interviewer(
        email="interviewer2@nucleusteq.com",
        password="Int2@12345",
    )
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview = await create_interview_via_api(
        client, str(candidate.id), str(interviewer1.id)
    )

    response = await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer2@nucleusteq.com", "Int2@12345"),
    )
    assert response.status_code == 403


async def test_submit_feedback_duplicate(client):
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

    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    response = await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 409


async def test_submit_feedback_invalid_rating(client):
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

    response = await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(technical_rating=6),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 422


async def test_get_feedback_as_hr(client):
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

    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    response = await client.get(
        f"/api/v1/interviews/{interview['id']}/feedback",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["interview_id"] == interview["id"]


async def test_get_feedback_as_assigned_interviewer(client):
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

    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    response = await client.get(
        f"/api/v1/interviews/{interview['id']}/feedback",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 200


async def test_get_feedback_as_other_interviewer(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    await seed_hr()
    interviewer1 = await seed_interviewer()
    interviewer2 = await seed_interviewer(
        email="interviewer2@nucleusteq.com",
        password="Int2@12345",
    )
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview = await create_interview_via_api(
        client, str(candidate.id), str(interviewer1.id)
    )

    # interviewer1 submits feedback
    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    # interviewer2 tries to view it — should be blocked
    response = await client.get(
        f"/api/v1/interviews/{interview['id']}/feedback",
        headers=auth_header("interviewer2@nucleusteq.com", "Int2@12345"),
    )
    assert response.status_code == 403

async def test_get_feedback_as_admin_forbidden(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()
    await Feedback.all().delete()

    await seed_admin()
    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview = await create_interview_via_api(
        client, str(candidate.id), str(interviewer.id)
    )

    await client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_payload(),
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )

    response = await client.get(
        f"/api/v1/interviews/{interview['id']}/feedback",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 403


async def test_get_feedback_not_submitted(client):
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
        f"/api/v1/interviews/{interview['id']}/feedback",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404