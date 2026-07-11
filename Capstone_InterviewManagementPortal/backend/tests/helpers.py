"""
Helper functions shared across all test files.
"""
import base64
import io
from datetime import date, timedelta
from src.models.users import User
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.enums.candidate_enums import CandidateStatus
from src.core.security import hash_password
from src.schemas.request.interview_request import InterviewCreate
from src.models.interview import Interview


def auth_header(email: str, password: str) -> dict:
    token = base64.b64encode(f"{email}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


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


async def seed_interviewer(
    email="interviewer@nucleusteq.com",
    password="Int@12345",
) -> User:
    user = User(
        email=email,
        password=hash_password(password),
        role="Interviewer",
        full_name="Interviewer User",
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


async def seed_candidate(
    job_id: str,
    email: str = "rahul@gmail.com",
    mobile: str = "9876543210",
    resume_data: bytes | None = b"%PDF-1.4 fake",
) -> Candidate:
    candidate = Candidate(
        first_name="Rahul",
        last_name="Sharma",
        email=email,
        mobile_number=mobile,
        current_company="ABC Corp",
        total_experience=3.0,
        applied_job=job_id,
        resume_data=resume_data,
        status=CandidateStatus.PROFILE_CREATED,
        created_by="hr@nucleusteq.com",
    )
    await candidate.insert()
    return candidate


def candidate_form_data(job_id: str, **kwargs) -> dict:
    defaults = {
        "first_name":       "Rahul",
        "last_name":        "Sharma",
        "email":            "rahul@gmail.com",
        "mobile_number":    "9876543210",
        "current_company":  "ABC Corp",
        "total_experience": "3.0",
        "applied_job":      job_id,
    }
    defaults.update(kwargs)
    return defaults


def pdf_file(filename: str = "cv.pdf") -> dict:
    return {"resume": (filename, io.BytesIO(b"%PDF-1.4 fake content"), "application/pdf")}


def interview_payload(candidate_id: str, interviewer_id: str, **kwargs) -> dict:
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    defaults = {
        "candidate_id":   candidate_id,
        "job_title":      "Backend Developer",
        "interview_date": tomorrow,
        "interview_time": "10:00",
        "interviewer_id": interviewer_id,
        "focus_areas":    "Python, FastAPI",
    }
    defaults.update(kwargs)
    return defaults


def feedback_payload(**kwargs) -> dict:
    defaults = {
        "technical_rating":     4,
        "communication_rating": 3,
        "problem_solving":      5,
        "tech_areas_covered":   "Python, APIs",
        "comments":             "Good candidate",
        "recommendation":       "SELECT",
    }
    defaults.update(kwargs)
    return defaults

async def create_interview_via_api(
    client, candidate_id: str, interviewer_id: str, **kwargs
) -> dict:
    """Creates an interview via HTTP and returns the full response body."""
    response = await client.post(
        "/api/v1/interviews",
        json=interview_payload(candidate_id, interviewer_id, **kwargs),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    return response.json()

async def create_interview_via_service(
    service, candidate_id: str, interviewer_id: str, **kwargs
) -> Interview:
    """Creates an interview via service and returns the Interview document."""
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    defaults = dict(
        candidate_id=candidate_id,
        job_title="Backend Developer",
        interview_date=tomorrow,
        interview_time="10:00",
        interviewer_id=interviewer_id,
        focus_areas="Python, FastAPI",
    )
    defaults.update(kwargs)
    return await service.create_interview(
        InterviewCreate(**defaults),
        scheduled_by="hr@nucleusteq.com",
    )