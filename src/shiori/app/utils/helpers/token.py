import uuid
from datetime import datetime, timedelta, timezone

import jwt

from shiori.app.core import get_settings
from shiori.app.core.exceptions import (DecodeTokenException,
                                        ExpiredTokenException)

config = get_settings()

class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        jti = str(uuid.uuid4())
        token = jwt.encode(
            payload = {
                **payload,
                "exp": datetime.now(timezone.utc) + timedelta(seconds=expire_period),
                "jti": jti,
            },
            key= config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException