from unittest.mock import AsyncMock

import pytest

from shiori.app.user.application.service import UserService
from shiori.app.user.application.usecase import CreateUserUseCase

user_service_mock = AsyncMock(spec=UserService)


@pytest.mark.asyncio
async def test_execute():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"
    nickname = "dummy_name"

    user_service_mock.create_user.return_value = 1

    use_case = CreateUserUseCase(user_service=user_service_mock)

    # When
    user_id = await use_case.execute(email=email, password=password, nickname=nickname)

    # Then
    assert user_id == 1
    user_service_mock.create_user.assert_awaited_once_with(email, password, nickname)
