"""
Unit tests for UserService business logic.

Contains:
- test_create_user_success          → user created with hashed password
- test_create_user_duplicate_email  → duplicate email raises DuplicateEmailException
- test_list_users                   → returns all users
- test_get_user_by_id_success       → returns correct user
- test_get_user_by_id_not_found     → raises ResourceNotFoundException
- test_update_user_success          → updates full_name and role
- test_update_user_not_found        → raises ResourceNotFoundException
- test_disable_user_success         → sets is_active to False
- test_disable_user_not_found       → raises ResourceNotFoundException
"""

import pytest
from src.services.user_service import UserService
from src.models.users import User, UserCreate, UserUpdate
from src.core.security import hash_password
from src.core.exceptions import DuplicateEmailException, ResourceNotFoundException
from src.enums.roles import UserRole

service = UserService()


def make_payload(**kwargs) -> UserCreate:
    defaults = {
        "email": "hr@nucleusteq.com",
        "password": "Test@123",
        "role": UserRole.HR,
        "full_name": "Test HR",
    }
    defaults.update(kwargs)
    return UserCreate(**defaults)


async def seed_user(email="hr@nucleusteq.com", role="HR") -> User:
    user = User(
        email=email,
        password=hash_password("Test@123"),
        role=role,
        full_name="Test User",
        is_password_reset_pending=True,
        is_active=True,
    )
    await user.insert()
    return user


# ── create_user ────────────────────────────────────────────────────────

async def test_create_user_success():
    """Created user has correct fields and password is not stored as plain text."""
    await User.all().delete()
    user = await service.create_user(make_payload())

    assert user.email == "hr@nucleusteq.com"
    assert user.role == UserRole.HR
    assert user.is_active is True
    assert user.is_password_reset_pending is True
    assert user.password != "Test@123"   # password must not be plain text


async def test_create_user_duplicate_email():
    """Second user with same email raises DuplicateEmailException."""
    await User.all().delete()
    await service.create_user(make_payload())

    with pytest.raises(DuplicateEmailException):
        await service.create_user(make_payload())


# ── list_users ─────────────────────────────────────────────────────────

async def test_list_users():
    """Returns all users in the system."""
    await User.all().delete()
    await seed_user("hr@nucleusteq.com")
    await seed_user("interviewer@nucleusteq.com", role="Interviewer")

    users = await service.list_users()
    assert len(users) == 2


# ── get_user_by_id ─────────────────────────────────────────────────────

async def test_get_user_by_id_success():
    """Returns the correct user for a valid ID."""
    await User.all().delete()
    created = await seed_user()

    found = await service.get_user_by_id(str(created.id))
    assert found.email == "hr@nucleusteq.com"


async def test_get_user_by_id_not_found():
    """Non-existent ID raises ResourceNotFoundException."""
    await User.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.get_user_by_id("000000000000000000000000")


# ── update_user ────────────────────────────────────────────────────────

async def test_update_user_success():
    """Updates full_name and role correctly."""
    await User.all().delete()
    created = await seed_user()

    updated = await service.update_user(
        str(created.id),
        UserUpdate(full_name="Updated Name", role=UserRole.INTERVIEWER)
    )
    assert updated.full_name == "Updated Name"
    assert updated.role == UserRole.INTERVIEWER


async def test_update_user_not_found():
    """Non-existent ID raises ResourceNotFoundException."""
    await User.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.update_user(
            "000000000000000000000000",
            UserUpdate(full_name="Updated Name")
        )


# ── disable_user ───────────────────────────────────────────────────────

async def test_disable_user_success():
    """Disable sets is_active to False without deleting the user."""
    await User.all().delete()
    created = await seed_user()

    disabled = await service.disable_user(str(created.id))
    assert disabled.is_active is False
    assert disabled.email == "hr@nucleusteq.com"  # user still exists


async def test_disable_user_not_found():
    """Non-existent ID raises ResourceNotFoundException."""
    await User.all().delete()

    with pytest.raises(ResourceNotFoundException):
        await service.disable_user("000000000000000000000000")