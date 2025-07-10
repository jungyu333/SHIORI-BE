from typing import Any

import jwt
import pytest

from shiori.app.core import get_settings
from shiori.app.utils.helpers import TokenHelper

config = get_settings()


@pytest.mark.asyncio
def test_encode():
    # Given
    payload = {
        "user_id": 1,
        "is_admin": True,
    }

    # When
    sut = TokenHelper.encode(payload=payload)

    # Then
    decoded_token: dict[str, Any] = jwt.decode(
        sut,
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM,
    )
    assert decoded_token["user_id"] == 1
    assert decoded_token["is_admin"] == True
