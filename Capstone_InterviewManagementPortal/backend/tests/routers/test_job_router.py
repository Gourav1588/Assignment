"""
Integration tests for job description API endpoints.

Contains:
- test_create_job_as_hr              → HR can create a job (201)
- test_create_job_as_admin_forbidden → Admin cannot create jobs (403)
- test_list_jobs_as_hr               → HR gets all jobs
- test_get_job_by_id_success         → HR gets a single job
- test_get_job_by_id_not_found       → unknown ID returns 404
- test_update_job_success            → HR updates a job
- test_update_job_not_found          → unknown ID returns 404
"""
import base64
from src.models.users import User
from src.models.jobs import Job
from src.core.security import hash_password


def auth_header(email: str, password: str) -> dict:
    token = base64.b64encode(f"{email}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


async def seed_hr() -> User:
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


async def seed_admin() -> User:
    user = User(
        email="admin@nucleusteq.com",
        password=hash_password("Admin@123"),
        role="Admin",
        full_name="Admin User",
        is_password_reset_pending=False,
        is_active=True,
    )
    await user.insert()
    return user


def job_payload(**kwargs):
    defaults = {
        "title": "Backend Developer",
        "details": "We are looking for a skilled backend developer.",
        "role": "Software Engineer",
        "required_skills": "Python, FastAPI",
        "experience_required": 2,
        "employment_type": "Full Time",
        "location": "Bangalore",
    }
    defaults.update(kwargs)
    return defaults


async def test_create_job_as_hr(client):
    """HR can create a job — returns 201 with all job fields."""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    response = await client.post(
        "/api/v1/jobs",
        json=job_payload(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Backend Developer"
    assert body["role"] == "Software Engineer"
    assert body["employment_type"] == "Full Time"
    assert body["created_by"] == "hr@nucleusteq.com"


async def test_create_job_as_admin_forbidden(client):
    """Admin cannot create jobs — returns 403."""
    await User.all().delete()
    await Job.all().delete()
    await seed_admin()

    response = await client.post(
        "/api/v1/jobs",
        json=job_payload(),
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 403


async def test_list_jobs_as_hr(client):
    """HR gets all job descriptions."""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    await client.post(
        "/api/v1/jobs",
        json=job_payload(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    response = await client.get(
        "/api/v1/jobs",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_job_by_id_success(client):
    """HR retrieves a single job by ID."""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    create_response = await client.post(
        "/api/v1/jobs",
        json=job_payload(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    job_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Backend Developer"
    assert response.json()["employment_type"] == "Full Time"


async def test_get_job_by_id_not_found(client):
    """Non-existent ID returns 404."""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/jobs/000000000000000000000000",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404
    assert response.json()["error_code"] == "RESOURCE_NOT_FOUND"


async def test_update_job_success(client):
    """HR updates a job description"""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    create_response = await client.post(
        "/api/v1/jobs",
        json=job_payload(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    job_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/jobs/{job_id}",
        json={"title": "Senior Backend Developer"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Senior Backend Developer"
    assert response.json()["location"] == "Bangalore" 


async def test_update_job_not_found(client):
    """Non-existent ID returns 404."""
    await User.all().delete()
    await Job.all().delete()
    await seed_hr()

    response = await client.put(
        "/api/v1/jobs/000000000000000000000000",
        json={"title": "Updated Title"},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404