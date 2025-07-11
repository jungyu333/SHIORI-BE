from sqlalchemy import select

from shiori.app.core.database import session
from shiori.app.user.domain.entity.user import User as UserVO
from shiori.app.user.domain.repository import UserRepository
from shiori.app.user.infra.model.user import User


class UserRepositoryImpl(UserRepository):
    async def get_user_by_email(self, email: str) -> UserVO | None:
        stmt = await session.execute(select(User).where(User.email == email))

        user = stmt.scalars().first()

        if not user:
            return None
        return UserVO.from_model(user)

    async def save(self, user: UserVO) -> int:

        model = user.to_model()

        session.add(model)

        await session.flush()

        return model.id
