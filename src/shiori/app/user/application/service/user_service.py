from fastapi import HTTPException

from shiori.app.core.database import Transactional
from shiori.app.user.domain.entity import UserVO
from shiori.app.user.domain.repository import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    @Transactional()
    async def create_user(self, email: str, password: str, nickname: str) -> int:

        existed_user = await self._user_repo.get_user_by_email(email)

        if existed_user:
            raise HTTPException(status_code=422, detail="User already exists")

        userVO = UserVO(email=email, password=password, nickname=nickname)

        user_id = await self._user_repo.save(userVO)

        return user_id
