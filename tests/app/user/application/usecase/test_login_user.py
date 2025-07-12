from unittest.mock import AsyncMock

import pytest

from shiori.app.user.application.service import UserService
from shiori.app.user.application.usecase import LoginUserUseCase

user_service_mock = AsyncMock(spec=UserService)


@pytest.mark.asyncio
async def test_execute():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"

    user_service_mock.login.return_value = "token", "refresh_token"

    use_case = LoginUserUseCase(user_service=user_service_mock)

    # When
    access_token, refresh_token = await use_case.execute(email=email, password=password)

    # Then
    assert access_token == "token"
    assert refresh_token == "refresh_token"

    user_service_mock.login.assert_awaited_once_with(email=email, password=password)
