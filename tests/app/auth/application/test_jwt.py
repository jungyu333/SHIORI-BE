import pytest

from shiori.app.auth.application import JwtService
from shiori.app.core import get_settings
from shiori.app.core.exceptions import DecodeTokenException
from shiori.app.utils.helpers import TokenHelper
from tests.support.token import INVALID_REFRESH_TOKEN

jwt_service = JwtService()

config = get_settings()


@pytest.mark.asyncio
async def test_verify_token():
    # Given, When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.verify_token(token="abc")


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token():
    # Given
    token = INVALID_REFRESH_TOKEN

    # When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.create_refresh_token(token=token, refresh_token=token)


@pytest.mark.asyncio
async def test_create_refresh_token():
    # Given
    token = TokenHelper.encode(payload={"user_id": 1, "is_admin": True})

    refresh_token = TokenHelper.encode(payload={"sub": "refresh"})

    # When
    sut = await jwt_service.create_refresh_token(
        token=token, refresh_token=refresh_token
    )

    # Then
    assert sut.token
    assert sut.refresh_token
