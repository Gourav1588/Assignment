"""
Integration test suite for authentication API endpoints.

Contains:
- test_login_success                → Valid credentials return user profile with 200
- test_login_wrong_password         → Wrong password returns 401
- test_login_unknown_email          → Unknown email returns 401
- test_login_no_credentials         → Missing header returns 401
- test_reset_password_success       → Valid new password clears pending flag
- test_reset_password_weak_password → Weak password returns 422
- test_reset_password_requires_auth → Unauthenticated reset attempt returns 401
- test_change_password_success         → Valid old password allows changing to new
- test_change_password_wrong_old_password → Wrong old password returns 401
- test_change_password_requires_auth   → Unauthenticated change attempt returns 401
"""

import base64
from src.models.users import User
from src.core.security import hash_password


def make_auth_header(email: str, password: str) -> dict:
    """Helper — builds Basic Auth header from email and password."""
    token = base64.b64encode(f"{email}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


async def create_test_user(
    email="test@nucleusteq.com",
    password="Valid@1234",
    role="Admin",
    full_name="Test User",
    is_password_reset_pending=False,
) -> User:
    """Helper — inserts a user into the mock DB and returns it."""
    user = User(
        email=email,
        password=hash_password(password),
        role=role,
        full_name=full_name,
        is_password_reset_pending=is_password_reset_pending,
    )
    await user.insert()
    return user


# ── Login ──────────────────────────────────────────────────────────────────

async def test_login_success(client):
    """Valid credentials return 200 and the user profile payload."""
    await create_test_user()
    response = await client.post(
        "/api/v1/auth/login",
        headers=make_auth_header("test@nucleusteq.com", "Valid@1234"),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "test@nucleusteq.com"
    assert body["role"] == "Admin"
    assert "password" not in body


async def test_login_wrong_password(client):
    """Incorrect password returns 401 Unauthorized."""
    await create_test_user()
    response = await client.post(
        "/api/v1/auth/login",
        headers=make_auth_header("test@nucleusteq.com", "Wrong@1234"),
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "UNAUTHORIZED_ACCESS"


async def test_login_unknown_email(client):
    """Unknown email returns 401 — not 404, to avoid user enumeration."""
    response = await client.post(
        "/api/v1/auth/login",
        headers=make_auth_header("nobody@nucleusteq.com", "Valid@1234"),
    )
    assert response.status_code == 401


async def test_login_no_credentials(client):
    """Request with no Authorization header returns 401."""
    response = await client.post("/api/v1/auth/login")
    assert response.status_code == 401

    
# ── change  Password ─────────────────────────────────────────────────────────
    
async def test_change_password_success(client):
    """Valid old password allows changing to new password."""
    await create_test_user(is_password_reset_pending=False)
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "Valid@1234", "new_password": "Changed@9876"},
        headers=make_auth_header("test@nucleusteq.com", "Valid@1234"),
    )
    assert response.status_code == 200


async def test_change_password_wrong_old_password(client):
    """Wrong old password returns 401."""
    await create_test_user(is_password_reset_pending=False)
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "Wrong@1234", "new_password": "Changed@9876"},
        headers=make_auth_header("test@nucleusteq.com", "Valid@1234"),
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "UNAUTHORIZED_ACCESS"


async def test_change_password_requires_auth(client):
    """Change password without credentials returns 401."""
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "Valid@1234", "new_password": "Changed@9876"},
    )
    assert response.status_code == 401