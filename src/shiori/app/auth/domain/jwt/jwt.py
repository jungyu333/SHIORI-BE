from abc import ABC, abstractmethod

from shiori.app.auth.interface.dto import RefreshTokenResponse


class Jwt(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> None:
        pass

    @abstractmethod
    async def create_refresh_token(
        self, token: str, refresh_token: str
    ) -> RefreshTokenResponse:
        pass
