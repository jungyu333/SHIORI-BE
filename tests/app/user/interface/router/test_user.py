import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shiori.app.server import app
from shiori.app.user.infra.repository.user import UserRepositoryImpl

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
        response = await client.post('/api/user/signup', json=body)

    # Then
    assert response.json() == {"code": 201, "message" : '환영합니다!' , "data": { "user_id": 1} }

    user_repo = UserRepositoryImpl()
    sut = await user_repo.get_user_by_email(email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.nickname == nickname