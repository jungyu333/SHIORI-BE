from abc import ABC, abstractmethod

from ..entity.user import User as UserVO


class UserRepository(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserVO:
        pass
