"""
Unit test suite verifying authentication service business logic operations.

Contains:
- MockPayload                           → Local Pydantic wrapper mimicking credentials input
- test_authenticate_user_success        → Asserts correct user retrieval on matching hashes
- test_authenticate_user_wrong_password → Asserts UnauthorizedException on key mismatches
- test_update_user_password_success    → Asserts database state updates cleanly on resets
"""

import pytest
from pydantic import BaseModel
from src.services.auth_service import auth_service
from src.models.users import User
from src.core.security import hash_password
from src.core.exceptions import UnauthorizedException


class MockPayload(BaseModel):
    """
    Simulates inbound basic auth payloads expected by the authentication engine.
    """
    email: str
    password: str


@pytest.mark.asyncio
async def test_authenticate_user_success():
    """
    Confirms successful verification and user record extraction for exact credential pairs.
    """
    await User.all().delete()
    user = User(
        email="test@nucleusteq.com",
        password=hash_password("Valid@1234"),
        role="Admin",
        full_name="Test User",
        is_password_reset_pending=True
    )
    await user.insert()

    payload = MockPayload(email="test@nucleusteq.com", password="Valid@1234")
    authenticated_user = await auth_service.authenticate_user(payload)
    assert authenticated_user.email == "test@nucleusteq.com"


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    """
    Ensures an unauthorized domain exception is safely raised for faulty hash values.
    """
    payload = MockPayload(email="test@nucleusteq.com", password="WrongPassword1")
    with pytest.raises(UnauthorizedException):
        await auth_service.authenticate_user(payload)


@pytest.mark.asyncio
async def test_update_user_password_success():
    """
    Validates password hash alteration and state cleanup for active user resets.
    """
    await User.all().delete()
    await User(
        email="test@nucleusteq.com",
        password=hash_password("Valid@1234"),
        role="Admin",
        full_name="Test User",
        is_password_reset_pending=True
    ).insert()

    updated_user = await auth_service.update_user_password(
        email="test@nucleusteq.com", 
        new_password="Changed@9876"
    )
    assert updated_user.is_password_reset_pending is False  # Confirms setup flag is disabled
    assert updated_user.password != hash_password("Valid@1234")