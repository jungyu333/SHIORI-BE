from shiori.app.core.helpers import redis_client
from shiori.app.user.application.service import UserService


class LogoutUserUseCase:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def execute(self, *, access_token: str) -> None:

        user_id, jti, ttl = self._user_service.parse_logout_user(
            access_token=access_token
        )

        await redis_client.set(name=f"blacklist:{jti}", value="1", ex=ttl)
