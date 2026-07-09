"""
Integration tests for Interview Management API endpoints.
"""
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from datetime import date, timedelta
from tests.helpers import (
    auth_header, seed_admin, seed_hr, seed_interviewer,
    seed_job, seed_candidate, interview_payload,
)


async def create_interview(client, candidate_id: str, interviewer_id: str) -> str:
    """Creates an interview and returns its ID."""
    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload(candidate_id, interviewer_id),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    return response.json()["id"]


async def test_schedule_interview_success(client):
    """HR schedules interview with valid candidate and interviewer."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload(str(candidate.id), str(interviewer.id)),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["candidate_id"] == str(candidate.id)
    assert response.json()["interviewer_id"] == str(interviewer.id)
    assert response.json()["job_title"] == "Backend Developer"


async def test_schedule_interview_invalid_candidate(client):
    """Unknown candidate ID returns 404."""
    await User.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()

    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload("000000000000000000000000", str(interviewer.id)),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404


async def test_schedule_interview_invalid_interviewer(client):
    """Unknown interviewer ID returns 404."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload(str(candidate.id), "000000000000000000000000"),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404


async def test_schedule_interview_wrong_role(client):
    """Assigning HR user as interviewer returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    hr = await seed_hr()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))

    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload(str(candidate.id), str(hr.id)),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409


async def test_list_interviews_as_hr(client):
    """HR lists all interviews — returns paginated response."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.get(
        "/api/v1/interviews?page=1&page_size=10",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


async def test_list_interviews_as_interviewer_forbidden(client):
    """Interviewer cannot access the all-interviews list."""
    await User.all().delete()
    await seed_interviewer()

    response = await client.get(
        "/api/v1/interviews?page=1&page_size=10",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 403


async def test_my_interviews_as_interviewer(client):
    """Interviewer lists their own assigned interviews."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.get(
        "/api/v1/interviews/my?page=1&page_size=10",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


async def test_my_interviews_as_hr_forbidden(client):
    """HR cannot access the /my endpoint."""
    await User.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/interviews/my?page=1&page_size=10",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 403


async def test_get_interview_success_as_hr(client):
    """HR views single interview successfully."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.get(
        f"/api/v1/interviews/{interview_id}",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["id"] == interview_id


async def test_get_interview_as_assigned_interviewer(client):
    """Assigned interviewer can view their own interview."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.get(
        f"/api/v1/interviews/{interview_id}",
        headers=auth_header("interviewer@nucleusteq.com", "Int@12345"),
    )
    assert response.status_code == 200


async def test_get_interview_as_other_interviewer(client):
    """Interviewer cannot view interview assigned to someone else."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer1 = await seed_interviewer()
    interviewer2 = await seed_interviewer(
        email="interviewer2@nucleusteq.com",
        password="Int2@12345",
    )
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer1.id))

    response = await client.get(
        f"/api/v1/interviews/{interview_id}",
        headers=auth_header("interviewer2@nucleusteq.com", "Int2@12345"),
    )
    assert response.status_code == 403


async def test_get_interview_as_admin_forbidden(client):
    """Admin cannot view interviews."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_admin()
    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.get(
        f"/api/v1/interviews/{interview_id}",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 403


async def test_get_interview_not_found(client):
    """Unknown interview ID returns 404."""
    await User.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/interviews/000000000000000000000000",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404


async def test_update_interview_success(client):
    """HR updates interview date and time."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer.id))
    
    new_date = (date.today() + timedelta(days=2)).isoformat()
    
    response = await client.put(
        f"/api/v1/interviews/{interview_id}",
        json={"interview_date": new_date, "interview_time": "14:00"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["interview_date"] == new_date
    assert response.json()["interview_time"] == "14:00"


async def test_update_interview_wrong_role(client):
    """Assigning HR user as new interviewer returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await Interview.all().delete()

    hr = await seed_hr()
    interviewer = await seed_interviewer()
    job = await seed_job()
    candidate = await seed_candidate(str(job.id))
    interview_id = await create_interview(client, str(candidate.id), str(interviewer.id))

    response = await client.put(
        f"/api/v1/interviews/{interview_id}",
        json={"interviewer_id": str(hr.id)},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409