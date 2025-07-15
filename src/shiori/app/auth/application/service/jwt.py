from shiori.app.auth.domain.jwt import Jwt
from shiori.app.auth.interface.dto import RefreshTokenResponse
from shiori.app.core.exceptions.base import DecodeTokenException
from shiori.app.core.exceptions.base import (
    DecodeTokenException as JwtDecodeTokenException,
)
from shiori.app.core.exceptions.base import (
    ExpiredTokenException as JwtExpiredTokenException,
)
from shiori.app.core.helpers import redis_client
from shiori.app.utils.helpers import TokenHelper


class JwtService(Jwt):
    async def create_refresh_token(
        self, *, token: str, refresh_token: str
    ) -> RefreshTokenResponse:
        decoded_access_token = TokenHelper.decode_expired_token(token=token)
        jti = decoded_access_token.get("jti")
        user_id = decoded_access_token.get("user_id")
        is_admin = decoded_access_token.get("is_admin")

        decoded_refresh_token = TokenHelper.decode(token=refresh_token)
        if decoded_refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        is_blacklisted = await redis_client.exists(f"blacklist:{jti}")
        if is_blacklisted:
            raise JwtExpiredTokenException

        key = f"refresh:{user_id}"
        ttl = 60 * 60 * 24 * 7  # 7days

        await redis_client.set(key, refresh_token, ex=ttl)

        return RefreshTokenResponse(
            token=TokenHelper.encode(
                payload={
                    "user_id": user_id,
                    "is_admin": is_admin,
                }
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )

    async def verify_token(self, *, token: str) -> None:
        try:
            decoded_token = TokenHelper.decode(token=token)
            jti = decoded_token.get("jti")

            if await redis_client.exists(f"blacklist:{jti}"):
                raise JwtExpiredTokenException

        except (JwtDecodeTokenException, JwtExpiredTokenException):
            raise DecodeTokenException
