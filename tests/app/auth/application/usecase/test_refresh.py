from unittest.mock import AsyncMock

import pytest

from shiori.app.auth.application.service import JwtService
from shiori.app.auth.application.usecase import RefreshUseCase
from shiori.app.auth.interface.dto import RefreshTokenResponse

jwt_service_mock = AsyncMock(spec=JwtService)


@pytest.mark.asyncio
async def test_execute():
    # Given
    access_token = "expired.access.token"
    refresh_token = "valid.refresh.token"

    expected_result = RefreshTokenResponse(
        token="new.access.token", refresh_token="new.refresh.token"
    )

    jwt_service_mock.create_refresh_token.return_value = expected_result

    use_case = RefreshUseCase(jwt_service=jwt_service_mock)

    # When
    result = await use_case.execute(
        access_token=access_token, refresh_token=refresh_token
    )

    # Then
    jwt_service_mock.create_refresh_token.assert_awaited_once_with(
        token=access_token,
        refresh_token=refresh_token,
    )

    assert isinstance(result, RefreshTokenResponse)
    assert result.token == "new.access.token"
    assert result.refresh_token == "new.refresh.token"
