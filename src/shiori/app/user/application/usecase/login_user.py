from shiori.app.core.helpers import redis_client
from shiori.app.user.application.service import UserService


class LoginUserUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def execute(self, email, password) -> tuple[str, str]:
        access_token, refresh_token, user_id = await self._user_service.login(
            email=email, password=password
        )

        key = f"refresh:{user_id}"
        ttl = 60 * 60 * 24 * 7  # 7days

        await redis_client.set(key, refresh_token, ex=ttl)

        return access_token, refresh_token
