from unittest.mock import AsyncMock

import pytest

from shiori.app.core.exceptions import ValidationException
from shiori.app.user.application.service import UserService
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.domain.repository import UserRepository

repository_mock = AsyncMock(spec=UserRepository)
user_service = UserService(user_repo=repository_mock)


@pytest.mark.asyncio
async def test_create_user():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"
    nickname = "dummy_name"

    repository_mock.get_user_by_email.return_value = None
    user_service._user_repo = repository_mock

    # When
    user_id = await user_service.create_user(
        email=email, password=password, nickname=nickname
    )

    # Then
    assert user_id is not None
    repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"
    nickname = "dummy_name"

    user = UserVO(
        email=email,
        password=password,
        nickname=nickname,
        is_admin=False,
    )

    repository_mock.get_user_by_email.return_value = user

    # When, Then
    with pytest.raises(ValidationException):
        await user_service.create_user(
            email=email, password=password, nickname=nickname
        )
