import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shiori.app.server import app
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.infra.repository.user import UserRepositoryImpl
from shiori.app.utils.crypto import Crypto

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
