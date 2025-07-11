from shiori.app.user.application.service import UserService


class LoginUserUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def execute(self, email, password) -> tuple[str, str]:
        access_token, refresh_token = await self._user_service.login(
            email=email, password=password
        )

        return access_token, refresh_token
