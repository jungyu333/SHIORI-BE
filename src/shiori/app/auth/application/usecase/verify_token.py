from shiori.app.auth.application.service import JwtService


class VerifyTokenUseCase:
    def __init__(self, *, jwt_service: JwtService):
        self._jwt_service = jwt_service

    async def execute(self, *, token: str) -> None:
        await self._jwt_service.verify_token(token=token)

        return
