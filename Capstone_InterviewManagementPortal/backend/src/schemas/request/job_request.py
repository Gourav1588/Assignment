"""
Request schemas for Job Description endpoints.
"""
from pydantic import BaseModel, Field,field_validator,model_validator
from src.enums.job_enums import EmploymentType

def _validate_non_empty(value: str) -> str:   
    if not value.strip():
        raise ValueError("Field cannot be empty or contain only spaces.")
    return value.strip()


def _validate_non_numeric(value: str) -> str: 
    stripped = value.strip()
    if stripped.isdigit():
        raise ValueError("Field cannot contain only numbers.")
    return stripped



class JobCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    details: str = Field(..., min_length=10, max_length=3000)
    role: str = Field(..., min_length=2, max_length=100)
    required_skills: str = Field(..., min_length=2,max_length=500)
    experience_required: float = Field(..., ge=0,)
    employment_type: EmploymentType
    location: str = Field(..., min_length=2, max_length=100)
    
    @field_validator("title", "role", "location")  
    @classmethod
    def validate_non_numeric_fields(cls, v: str) -> str:
        v = _validate_non_empty(v)
        return _validate_non_numeric(v)

    @field_validator("details", "required_skills")   
    @classmethod
    def validate_non_empty_fields(cls, v: str) -> str:
        return _validate_non_empty(v)



class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    details: str | None = Field(default=None, min_length=10)
    role: str | None = Field(default=None, min_length=2, max_length=100)
    required_skills: str | None = Field(default=None, min_length=2 , max_length=500)
    experience_required: float | None = Field(default=None, ge=0)
    employment_type: EmploymentType | None = None
    location: str | None = Field(default=None, min_length=2)
    
    @field_validator("title", "role", "location") 
    @classmethod
    def validate_non_numeric_fields(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = _validate_non_empty(v)
        return _validate_non_numeric(v)

    @field_validator("details", "required_skills")  
    @classmethod
    def validate_non_empty_fields(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _validate_non_empty(v)
    
    @model_validator(mode="after")  
    def validate_at_least_one_field(self):
        if all(
            getattr(self, field) is None
            for field in (
                "title", "details", "role", "required_skills",
                "experience_required", "employment_type", "location",
            )
        ):
            raise ValueError("At least one field must be provided to update.")
        return self