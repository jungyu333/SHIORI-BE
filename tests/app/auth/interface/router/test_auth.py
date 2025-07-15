import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shiori.app.core.helpers import redis_client
from shiori.app.server import app
from shiori.app.utils.helpers import TokenHelper

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_refresh_token(session: AsyncSession):
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
    refresh_token = TokenHelper.encode({"sub": "refresh"})

    cookies = {"refresh_token": refresh_token}
    body = {"access_token": access_token}

    # When

    async with AsyncClient(app=app, base_url=BASE_URL, cookies=cookies) as client:
        response = await client.post("/api/auth/refresh", json=body)

    # Then

    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "token" in json_data["data"]

    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None
    assert "refresh_token=" in set_cookie


@pytest.mark.asyncio
async def test_refresh_token_invalid_sub(session: AsyncSession):
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
    invalid_refresh_token = TokenHelper.encode({"sub": "not_refresh"})

    cookies = {"refresh_token": invalid_refresh_token}
    body = {"access_token": access_token}

    # When

    async with AsyncClient(app=app, base_url=BASE_URL, cookies=cookies) as client:
        response = await client.post("/api/auth/refresh", json=body)

    # Then

    assert response.status_code == 400
    json_data = response.json()
    assert json_data["code"] == 400
    assert json_data["message"] == "TOKEN__DECODE_ERROR"


@pytest.mark.asyncio
async def test_verify(session: AsyncSession):
    # Given

    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})

    body = {"access_token": access_token}

    # When

    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/auth/verify", json=body)

    # Then

    assert response.status_code == 200
    json_data = response.json()
    assert "message" in json_data
    assert json_data["message"] == "success"


@pytest.mark.asyncio
async def test_verify_expired_token():
    # Given
    access_token = TokenHelper.encode(
        {"user_id": 1, "is_admin": False}, expire_period=-1
    )

    body = {"access_token": access_token}

    # When

    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/auth/verify", json=body)

    # Then

    assert response.status_code == 400
    json_data = response.json()
    assert "message" in json_data
    assert json_data["message"] == "TOKEN__DECODE_ERROR"


@pytest.mark.asyncio
async def test_verify_blacklisted_token():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
    jti = TokenHelper.decode(access_token)["jti"]
    await redis_client.set(f"blacklist:{jti}", "1", ex=3600)

    body = {"access_token": access_token}

    # When
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/auth/verify", json=body)

    # Then

    assert response.status_code == 400
    json_data = response.json()
    assert "message" in json_data
    assert json_data["message"] == "TOKEN__DECODE_ERROR"
