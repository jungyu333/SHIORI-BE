from unittest.mock import AsyncMock, MagicMock

import pytest

from shiori.app.user.application.service import UserService
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.domain.repository import UserRepository
from shiori.app.user.interface.exception import (
    DuplicateUserException,
    UserNotFoundException,
    AuthenticationException,
)
from shiori.app.utils.crypto import Crypto

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
    user_service._user_repo = repository_mock

    # When, Then
    with pytest.raises(DuplicateUserException):
        await user_service.create_user(
            email=email, password=password, nickname=nickname
        )


@pytest.mark.asyncio
async def test_login():
    # Given
    user = UserVO(
        id=1,
        email="dummy@naver.com",
        password="rlawnsrb1!",
        is_admin=False,
        nickname="dummy_name",
    )

    repository_mock.get_user_by_email.return_value = user
    user_service._user_repo = repository_mock

    mock_crypto = MagicMock(spec=Crypto)
    mock_crypto.verify.return_value = True
    user_service._crypto = mock_crypto

    # When

    access_token, refresh_token = await user_service.login(
        email="dummy@naver.com", password="rlawnsrb1!"
    )

    # Then
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)


@pytest.mark.asyncio
async def test_login_user_not_found():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"

    repository_mock.get_user_by_email.return_value = None
    user_service._user_repo = repository_mock

    mock_crypto = MagicMock(spec=Crypto)
    mock_crypto.verify.return_value = True
    user_service._crypto = mock_crypto

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.login(email=email, password=password)


@pytest.mark.asyncio
async def test_login_wrong_password():
    # Given
    email = "dummy@naver.com"
    password = "rlawnsrb1!"

    user = UserVO(
        id=1,
        email=email,
        password="rlawnsrb11!",
        is_admin=False,
        nickname="dummy_name",
    )

    repository_mock.get_user_by_email.return_value = user
    user_service._user_repo = repository_mock

    mock_crypto = MagicMock(spec=Crypto)
    mock_crypto.verify.return_value = False
    user_service._crypto = mock_crypto

    # When, Then
    with pytest.raises(AuthenticationException):
        await user_service.login(email=email, password=password)
