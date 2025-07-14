from shiori.app.auth.application.service import JwtService
from shiori.app.auth.interface.dto import RefreshTokenResponse


class RefreshUseCase:
    def __init__(self, *, jwt_service: JwtService):
        self._jwt_service = jwt_service

    async def execute(
        self, *, access_token: str, refresh_token: str
    ) -> RefreshTokenResponse:

        token_result = await self._jwt_service.create_refresh_token(
            token=access_token, refresh_token=refresh_token
        )

        return token_result
