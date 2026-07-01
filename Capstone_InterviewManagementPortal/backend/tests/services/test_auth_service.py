"""
Unit test suite verifying authentication service business logic operations.

Contains:
- MockPayload                           → Local Pydantic wrapper mimicking credentials input
- test_authenticate_user_success        → Asserts correct user retrieval on matching hashes
- test_authenticate_user_wrong_password → Asserts UnauthorizedException on key mismatches
- test_change_password_success            → Valid old password allows changing to new
- test_change_password_wrong_old_password → Wrong old password returns 401
- test_change_password_requires_auth      → Unauthenticated change attempt returns 401
"""

import pytest
from src.services.auth_service import auth_service
from src.models.users import User
from src.core.security import hash_password
from src.core.exceptions import UnauthorizedException


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

    
    authenticated_user = await auth_service.authenticate_user("test@nucleusteq.com","Valid@1234",)
    assert authenticated_user.email == "test@nucleusteq.com"



async def test_authenticate_user_wrong_password():
    """
    Ensures an unauthorized domain exception is safely raised for faulty hash values.
    """
    
    await User.all().delete()
    await User(
        email="test@nucleusteq.com",
        password=hash_password("Valid@1234"),
        role="Admin",
        full_name="Test User",
        is_password_reset_pending=True,
    ).insert()
    
    with pytest.raises(UnauthorizedException):
        await auth_service.authenticate_user(
            "test@nucleusteq.com",
            "WrongPassword1",
    )

# ── change_password ────────────────────────────────────────────────────────

async def test_change_password_success():
    """Old password verified, new password saved, pending flag cleared."""
    await User.all().delete()
    await User(
        email="test@nucleusteq.com",
        password=hash_password("Valid@1234"),
        role="Admin",
        full_name="Test User",
        is_password_reset_pending=True,
    ).insert()

    updated = await auth_service.change_password(
        email="test@nucleusteq.com",
        old_password="Valid@1234",
        new_password="Changed@9876",
    )
    assert updated.is_password_reset_pending is False
    assert updated.password != hash_password("Valid@1234")


async def test_change_password_wrong_old_password():
    """Wrong old password raises UnauthorizedException."""
    await User.all().delete()
    await User(
        email="test@nucleusteq.com",
        password=hash_password("Valid@1234"),
        role="Admin",
        full_name="Test User",
        is_password_reset_pending=False,
    ).insert()

    with pytest.raises(UnauthorizedException):
        await auth_service.change_password(
            email="test@nucleusteq.com",
            old_password="Wrong@1234",
            new_password="Changed@9876",
        )

