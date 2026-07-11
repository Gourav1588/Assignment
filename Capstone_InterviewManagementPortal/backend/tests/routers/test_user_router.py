"""
Integration tests for user management API endpoints.

Contains:
- test_create_user_as_admin          → Admin can create users
- test_create_user_as_hr_forbidden   → HR cannot create users (403)
- test_create_user_duplicate_email   → duplicate email returns 409
- test_list_users_as_admin           → Admin gets all users
- test_get_user_by_id_success        → Admin gets single user
- test_get_user_by_id_not_found      → unknown ID returns 404
- test_update_user_success           → Admin updates user fields
- test_disable_user_success          → Admin disables a user
"""

from src.models.users import User
from tests.helpers import auth_header, seed_admin, seed_hr


def new_user_payload(email="newhr@nucleusteq.com"):
    return {
        "email": email,
        "password": "Test@123",
        "role": "HR",
        "full_name": "New HR User",
    }


async def test_create_user_as_admin(client):
    """Admin can create a new user — returns 201 with user data."""
    await User.all().delete()
    await seed_admin()

    response = await client.post(
        "/api/v1/users",
        json=new_user_payload(),
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "newhr@nucleusteq.com"
    assert body["is_active"] is True
    assert body["is_password_reset_pending"] is True
    assert "password" not in body


async def test_create_user_as_hr_forbidden(client):
    """HR cannot create users — returns 403."""
    await User.all().delete()
    await seed_admin()
    await seed_hr()

    response = await client.post(
        "/api/v1/users",
        json=new_user_payload(),
        headers=auth_header("hr@nucleusteq.com", "Hr@12345"),
    )
    assert response.status_code == 403
    assert response.json()["error_code"] == "INSUFFICIENT_PERMISSIONS"


async def test_create_user_duplicate_email(client):
    """Creating two users with same email returns 409."""
    await User.all().delete()
    await seed_admin()

    await client.post(
        "/api/v1/users",
        json=new_user_payload(),
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    response = await client.post(
        "/api/v1/users",
        json=new_user_payload(),
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "DUPLICATE_EMAIL"


async def test_list_users_as_admin(client):
    """Admin gets all users in the system."""
    await User.all().delete()
    await seed_admin()
    await seed_hr()

    response = await client.get(
        "/api/v1/users?page=1&page_size=10",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


async def test_get_user_by_id_success(client):
    """Admin retrieves a specific user by ID."""
    await User.all().delete()
    await seed_admin()
    hr = await seed_hr()

    response = await client.get(
        f"/api/v1/users/{hr.id}",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 200
    assert response.json()["email"] == "hr@nucleusteq.com"


async def test_get_user_by_id_not_found(client):
    """Non-existent ID returns 404."""
    await User.all().delete()
    await seed_admin()

    response = await client.get(
        "/api/v1/users/000000000000000000000000",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 404
    assert response.json()["error_code"] == "RESOURCE_NOT_FOUND"


# ── update user ────────────────────────────────────────────────────────

async def test_update_user_success(client):
    """Admin updates a user's full_name."""
    await User.all().delete()
    await seed_admin()
    hr = await seed_hr()

    response = await client.put(
        f"/api/v1/users/{hr.id}",
        json={"full_name": "Updated HR Name"},
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated HR Name"


# ── disable user ───────────────────────────────────────────────────────

async def test_disable_user_success(client):
    """Admin disables a user — is_active becomes False."""
    await User.all().delete()
    await seed_admin()
    hr = await seed_hr()

    response = await client.patch(
        f"/api/v1/users/{hr.id}/disable",
        headers=auth_header("admin@nucleusteq.com", "Admin@123"),
    )
    assert response.status_code == 200
    assert response.json()["is_active"] is False
    assert response.json()["email"] == "hr@nucleusteq.com"