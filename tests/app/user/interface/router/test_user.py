import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shiori.app.core.helpers import redis_client
from shiori.app.server import app
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.infra.repository.user import UserRepositoryImpl
from shiori.app.utils.crypto import Crypto
from shiori.app.utils.helpers import TokenHelper

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_signup(session: AsyncSession):
    # Given
    email = "jungyu@naver.com"
    password = "ralwnsrb1!"
    nickname = "dummy_name"

    body = {
        "email": email,
        "password": password,
        "nickname": nickname,
    }

    # When
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/user/signup", json=body)

    # Then
    assert response.json() == {
        "code": 201,
        "message": "환영합니다!",
        "data": {"user_id": 1},
    }

    user_repo = UserRepositoryImpl()
    sut = await user_repo.get_user_by_email(email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given

    email = "jungyu@naver.com"
    password = "ralwnsrb1!"
    nickname = "dummy_name"

    user = UserVO(
        id=1,
        email=email,
        password=Crypto().encrypt(password),
        nickname=nickname,
        is_admin=False,
    )

    session.add(user.to_model())
    await session.commit()

    body = {
        "email": email,
        "password": password,
    }

    # When
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/user/login", json=body)

    # Then
    assert response.status_code == 200
    sut = response.json()

    assert sut["code"] == 200
    assert sut["message"] == "환영합니다!"
    assert "data" in sut
    assert "token" in sut["data"]

    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None
    assert "refresh_token=" in set_cookie


@pytest.mark.asyncio
async def test_logout_registers_token_in_blacklist(session: AsyncSession):
    # Given
    email = "test@example.com"
    password = "rlawnsrb1!"
    nickname = "tester"

    user = UserVO(
        id=1,
        email=email,
        password=Crypto().encrypt(password),
        nickname=nickname,
        is_admin=False,
    )
    session.add(user.to_model())
    await session.commit()

    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        login_response = await client.post(
            "/api/user/login", json={"email": email, "password": password}
        )

    sut = login_response.json()
    access_token = sut["data"]["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.delete("/api/user/logout")

    payload = TokenHelper.decode(access_token)
    jti = payload["jti"]

    stored = await redis_client.get(f"blacklist:{jti}")
    assert stored == "1"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_blacklisted_token_is_rejected(session: AsyncSession):
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
    jti = TokenHelper.decode(access_token)["jti"]
    ttl = 3600

    await redis_client.set(f"blacklist:{jti}", "1", ex=ttl)

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.delete("/api/user/logout")

    # Then
    assert response.status_code == 401
