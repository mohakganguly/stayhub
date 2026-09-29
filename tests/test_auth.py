from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings



def test_auth_me_requires_authentication(client):
    response = client.get(
        "/api/v1/auth/me"
    )

    assert response.status_code == 401

def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPass123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    assert "password" not in data
    assert "password_hash" not in data

def test_register_duplicate_email(client):
    payload = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "TestPass123",
    }

    # First registration
    first_response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    # Same email again
    second_response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409

def test_login_user(client):
    # Create user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "LoginPass123",
        },
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "LoginPass123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0

def test_login_wrong_password(client):
    # Create user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Wrong Password User",
            "email": "wrongpassword@example.com",
            "password": "CorrectPass123",
        },
    )

    assert register_response.status_code == 201

    # Attempt login with incorrect password
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpassword@example.com",
            "password": "WrongPass123",
        },
    )

    assert login_response.status_code == 401

    data = login_response.json()

    assert data["detail"] == "Invalid email or password"

def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "SomePass123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"

def test_auth_me_with_valid_token(client):
    # Register
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Token User",
            "email": "tokenuser@example.com",
            "password": "TokenPass123",
        },
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "tokenuser@example.com",
            "password": "TokenPass123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["name"] == "Token User"
    assert data["email"] == "tokenuser@example.com"
    assert "id" in data

    # Sensitive fields must not be returned
    assert "password" not in data
    assert "password_hash" not in data

def test_auth_me_with_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer this-is-not-a-valid-jwt",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid authentication credentials"

def test_auth_me_with_expired_token(client):
    expired_time = (
        datetime.now(timezone.utc)
        - timedelta(minutes=1)
    )

    token = jwt.encode(
        {
            "sub": "1",
            "exp": expired_time,
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid authentication credentials"

def test_register_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Invalid Email User",
            "email": "not-an-email",
            "password": "ValidPass123",
        },
    )

    assert response.status_code == 422

def test_register_short_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Short Password User",
            "email": "shortpass@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422

def test_register_missing_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Missing Password User",
            "email": "missingpass@example.com",
        },
    )

    assert response.status_code == 422