from shiori.app.core.database import Transactional
from shiori.app.core.exceptions import ValidationException
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.domain.repository import UserRepository
from shiori.app.utils.crypto import Crypto


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
        self._crypto = Crypto()

    @Transactional()
    async def create_user(self, email: str, password: str, nickname: str) -> int:

        existed_user = await self._user_repo.get_user_by_email(email)

        if existed_user:
            raise ValidationException(message="이미 존재하는 회원입니다")

        userVO = UserVO(email=email, password= self._crypto.encrypt(password), nickname=nickname)

        user_id = await self._user_repo.save(userVO)

        return user_id
