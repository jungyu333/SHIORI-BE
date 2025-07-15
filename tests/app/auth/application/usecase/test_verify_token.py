from unittest.mock import AsyncMock

import pytest

from shiori.app.auth.application.service import JwtService
from shiori.app.auth.application.usecase import VerifyTokenUseCase
from shiori.app.core.exceptions import DecodeTokenException
from shiori.app.utils.helpers import TokenHelper

jwt_service_mock = AsyncMock(spec=JwtService)


@pytest.mark.asyncio
async def test_execute():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})

    use_case = VerifyTokenUseCase(jwt_service=jwt_service_mock)

    # When

    await use_case.execute(token=access_token)

    # Then

    jwt_service_mock.verify_token.assert_awaited_once_with(token=access_token)


@pytest.mark.asyncio
async def test_execute_with_expired_token():
    # Given

    jwt_service_mock.verify_token.side_effect = DecodeTokenException("invalid token")
    use_case = VerifyTokenUseCase(jwt_service=jwt_service_mock)

    # When, Then
    with pytest.raises(DecodeTokenException) as exc_info:
        await use_case.execute(token="fake.token")

    assert str(exc_info.value) == "invalid token"
