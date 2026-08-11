"""
Tests for the auth module endpoints.

Endpoints tested:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/otp/verify
- GET /api/v1/health
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models.user import User


class TestHealth:
    """Test the health check endpoint."""

    async def test_health_endpoint(self, client: AsyncClient):
        """GET /api/v1/health returns 200 with status ok."""
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestRegister:
    """Test the register endpoint."""

    async def test_register_success(self, client: AsyncClient):
        """POST /api/v1/auth/register creates a new user."""
        payload = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "securepassword123",
        }
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["email"] == "newuser@example.com"
        assert "user_id" in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        """POST /api/v1/auth/register with existing email returns 409."""
        payload = {
            "email": "duplicate@example.com",
            "name": "First User",
            "password": "securepassword123",
        }
        # First registration should succeed
        response1 = await client.post("/api/v1/auth/register", json=payload)
        assert response1.status_code == 200

        # Second registration with same email should fail
        payload["name"] = "Second User"
        response2 = await client.post("/api/v1/auth/register", json=payload)
        assert response2.status_code == 409
        data = response2.json()
        assert "sudah terdaftar" in data["detail"]


class TestLogin:
    """Test the login endpoint."""

    async def test_login_user_not_found(self, client: AsyncClient):
        """POST /api/v1/auth/login with non-existent email returns 401."""
        payload = {
            "email": "nonexistent@example.com",
            "password": "anypassword123",
        }
        response = await client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert "salah" in data["detail"]


class TestOTPVerify:
    """Test the OTP verify endpoint."""

    async def test_otp_verify_invalid_code(self, client: AsyncClient, test_user: User):
        """POST /api/v1/auth/otp/verify with invalid code returns 400."""
        payload = {
            "email": test_user.email,
            "code": "000000",
        }
        response = await client.post("/api/v1/auth/otp/verify", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "tidak valid" in data["detail"]

    async def test_otp_verify_user_not_found(self, client: AsyncClient):
        """POST /api/v1/auth/otp/verify with non-existent user returns 404."""
        payload = {
            "email": "nobody@example.com",
            "code": "123456",
        }
        response = await client.post("/api/v1/auth/otp/verify", json=payload)
        assert response.status_code == 404
        data = response.json()
        assert "tidak ditemukan" in data["detail"]
