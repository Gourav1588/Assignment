"""
Job Description database document model.
"""
from beanie import Document
from src.enums.job_enums import EmploymentType


class Job(Document):
    title: str
    details: str
    role: str
    required_skills: str
    experience_required: float
    employment_type: EmploymentType
    location: str
    created_by: str

    class Settings:
        name = "jobs"