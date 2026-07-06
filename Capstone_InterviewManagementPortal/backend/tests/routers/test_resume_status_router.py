"""
Integration tests for resume and status tracking API endpoints.
"""

import base64
import io
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.status_history import StatusHistory
from src.core.security import hash_password


def auth_header(email: str, password: str) -> dict:
    """Generate Basic Authentication header."""
    token = base64.b64encode(f"{email}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


async def seed_hr() -> User:
    """Create a sample HR user for authenticated requests."""
    user = User(
        email="hr@nucleusteq.com",
        password=hash_password("Hr@12345"),
        role="HR",
        full_name="HR User",
        is_password_reset_pending=False,
        is_active=True,
    )
    await user.insert()
    return user


async def seed_job() -> Job:
    """Create a sample job."""
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
        created_by="hr@nucleusteq.com",
    )
    await candidate.insert()
    return candidate


async def test_upload_resume_success(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Upload a valid PDF resume
    response = await client.post(
        f"/api/v1/candidates/{created.id}/resume",
        files={"file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 content"), "application/pdf")},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(created.id)


async def test_upload_resume_wrong_format(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Upload an unsupported file type
    response = await client.post(
        f"/api/v1/candidates/{created.id}/resume",
        files={"file": ("photo.png", io.BytesIO(b"fake image"), "image/png")},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 409


async def test_upload_resume_exceeds_limit(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()

    await seed_hr()
    job = await seed_job()
    created = await seed_candidate(str(job.id))

    # Upload a file larger than the allowed size
    response = await client.post(
        f"/api/v1/candidates/{created.id}/resume",
        files={"file": ("big.pdf", io.BytesIO(b"x" * (11 * 1024 * 1024)), "application/pdf")},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )

    assert response.status_code == 409


async def test_get_resume_not_uploaded(client):
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

    assert response.status_code == 404


async def test_update_status_success(client):
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


async def test_get_status_history_success(client):
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