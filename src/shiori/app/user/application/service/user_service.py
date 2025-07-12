from shiori.app.core.database import Transactional
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.domain.repository import UserRepository
from shiori.app.user.interface.exception import (
    UserNotFoundException,
    AuthenticationException,
    DuplicateUserException,
)
from shiori.app.utils.crypto import Crypto
from shiori.app.utils.helpers import TokenHelper


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
        self._crypto = Crypto()

    @Transactional()
    async def create_user(self, email: str, password: str, nickname: str) -> int:
        existed_user = await self._user_repo.get_user_by_email(email)

        if existed_user:
            raise DuplicateUserException

        userVO = UserVO(
            email=email,
            password=self._crypto.encrypt(password),
            nickname=nickname,
            is_admin=False,
        )

        user_id = await self._user_repo.save(userVO)

        return user_id

    async def login(self, email: str, password: str) -> tuple[str, str]:
        user = await self._user_repo.get_user_by_email(email)

        if not user:
            raise UserNotFoundException

        is_matched = self._crypto.verify(password, user.password)

        if not is_matched:
            raise AuthenticationException

        token = TokenHelper.encode(
            {
                "user_id": user.id,
                "is_admin": user.is_admin,
            }
        )

        refresh_token = TokenHelper.encode(
            {
                "sub": "refresh",
            }
        )

        return token, refresh_token
