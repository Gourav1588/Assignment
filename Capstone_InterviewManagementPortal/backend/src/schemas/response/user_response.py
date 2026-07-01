from pydantic import BaseModel, EmailStr, ConfigDict, Field
from beanie import PydanticObjectId
from src.enums.roles import UserRole


class UserResponse(BaseModel):
    id: PydanticObjectId = Field(..., validation_alias="_id")
    email: EmailStr
    role: UserRole
    full_name: str
    is_password_reset_pending: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)