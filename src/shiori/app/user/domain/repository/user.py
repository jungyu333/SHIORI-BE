from abc import ABC, abstractmethod

from shiori.app.user.domain.entity import UserVO


class UserRepository(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserVO | None:
        pass

    @abstractmethod
    async def save(self, user: UserVO) -> int:
        pass

    @abstractmethod
    async def get_user_by_email_and_password(
        self, email: str, password: str
    ) -> UserVO | None:
        pass
