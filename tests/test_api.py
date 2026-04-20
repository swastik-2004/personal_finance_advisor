import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE_URL = "http://test"

TEST_EMAIL = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "TestPass123"


@pytest.fixture(scope="session")
async def registered_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/auth/register", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "first_name": "Test",
            "last_name": "User"
        })
    return response


@pytest.mark.asyncio(loop_scope="session")
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(registered_user):
    assert registered_user.status_code == 201
    data = registered_user.json()
    assert "access_token" in data
    assert data["user"]["email"] == TEST_EMAIL


@pytest.mark.asyncio(loop_scope="session")
async def test_login_valid_credentials(registered_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_login_invalid_credentials():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
