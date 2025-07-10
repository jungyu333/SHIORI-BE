from shiori.app.auth.domain.jwt import Jwt
from shiori.app.auth.interface.dto import RefreshTokenResponse
from shiori.app.core.exceptions.base import DecodeTokenException
from shiori.app.core.exceptions.base import \
    DecodeTokenException as JwtDecodeTokenException
from shiori.app.core.exceptions.base import \
    ExpiredTokenException as JwtExpiredTokenException
from shiori.app.utils.helpers import TokenHelper


class JwtService(Jwt):
    async def create_refresh_token(
        self, token: str, refresh_token: str
    ) -> RefreshTokenResponse:
        decoded_created_token = TokenHelper.decode(token=token)
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)
        if decoded_refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenResponse(
            token=TokenHelper.encode(
                payload={
                    "user_id": decoded_created_token.get("user_id"),
                    "is_admin": decoded_created_token.get("is_admin")
                }
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )

    async def verify_token(self, token: str) -> None:
        try:
            TokenHelper.decode(token=token)
        except (JwtDecodeTokenException, JwtExpiredTokenException):
            raise DecodeTokenException
