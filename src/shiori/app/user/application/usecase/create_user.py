from shiori.app.user.application.service import UserService


class CreateUserUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def execute(self, email: str, password: str, nickname: str) -> int:
        user_id = await self._user_service.create_user(email, password, nickname)

        return user_id
