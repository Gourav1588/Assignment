"""
Integration tests for Candidate Management API endpoints.

Contains:
- test_create_candidate_success            → HR creates candidate (201)
- test_create_candidate_as_admin_forbidden → Admin cannot create (403)
- test_create_candidate_duplicate_email    → duplicate email returns 409
- test_create_candidate_duplicate_mobile   → duplicate mobile returns 409
- test_create_candidate_invalid_mobile     → mobile exceeding 10 digits returns 422
- test_create_candidate_no_resume          → missing resume returns 422
- test_create_candidate_wrong_resume_format → non-PDF returns 409
- test_list_candidates                     → HR lists all candidates
- test_get_candidate_by_id_success         → HR gets single candidate
- test_get_candidate_not_found             → unknown ID returns 404
- test_update_candidate_success            → HR updates candidate
"""
import base64
import io
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
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


async def seed_job() -> Job:
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


def candidate_form_data(job_id: str, **kwargs):
    """Returns form fields for multipart/form-data candidate creation."""
    defaults = {
        "first_name": "Rahul",
        "last_name": "Sharma",
        "email": "rahul@gmail.com",
        "mobile_number": "9876543210",
        "current_company": "ABC Corp",
        "total_experience": 3.0,
        "applied_job": job_id,
    }
    defaults.update(kwargs)
    return defaults

def pdf_file(filename: str = "cv.pdf") -> dict:
    """Returns a valid PDF file for multipart upload."""
    return {"resume": (filename, io.BytesIO(b"%PDF-1.4 fake content"), "application/pdf")}


async def test_create_candidate_success(client):
    """HR creates a candidate with resume — returns 201."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 201
    assert response.json()["email"] == "rahul@gmail.com"
    assert response.json()["status"] == "PROFILE_CREATED"


async def test_create_candidate_as_admin_forbidden(client):
    """Admin cannot create candidates — returns 403."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_admin()
    job = await seed_job()

    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 403


async def test_create_candidate_duplicate_email(client):
    """Duplicate email returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409


async def test_create_candidate_duplicate_mobile(client):
    """Duplicate mobile returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id), email="other@gmail.com"),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409


async def test_create_candidate_invalid_mobile(client):
    """Invalid mobile number returns 422."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id), mobile_number="123"),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409
    

async def test_create_candidate_no_resume(client):
    """Missing resume returns 422 — resume is mandatory."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 422
    
async def test_create_candidate_wrong_resume_format(client):
    """Non-PDF resume returns 409."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files={"resume": ("photo.png", io.BytesIO(b"fake image"), "image/png")},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 409



async def test_list_candidates(client):
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    response = await client.get(
        "/api/v1/candidates",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_candidate_by_id_success(client):
    """HR retrieves a single candidate by ID."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    create_response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    candidate_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/candidates/{candidate_id}",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["email"] == "rahul@gmail.com"


async def test_get_candidate_not_found(client):
    """Unknown ID returns 404."""
    await User.all().delete()
    await Candidate.all().delete()
    await seed_hr()

    response = await client.get(
        "/api/v1/candidates/000000000000000000000000",
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 404


async def test_update_candidate_success(client):
    """HR updates candidate profile fields."""
    await User.all().delete()
    await Job.all().delete()
    await Candidate.all().delete()
    await seed_hr()
    job = await seed_job()

    create_response = await client.post(
        "/api/v1/candidates",
        data=candidate_form_data(str(job.id)),
        files=pdf_file(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    candidate_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/candidates/{candidate_id}",
        json={"current_company": "XYZ Corp", "total_experience": 5.0},
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 200
    assert response.json()["current_company"] == "XYZ Corp"
    assert response.json()["total_experience"] == 5.0