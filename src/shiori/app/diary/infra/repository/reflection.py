from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError

from shiori.app.core.database import session
from shiori.app.diary.domain.entity import ReflectionVO
from shiori.app.diary.domain.repository import ReflectionRepository
from shiori.app.diary.infra.model import Reflection


class ReflectionRepositoryImpl(ReflectionRepository):

    async def upsert(self, *, reflection: ReflectionVO) -> None:

        model = reflection.to_model()

        session.add(model)

        try:
            await session.flush()
        except IntegrityError:

            await session.rollback()
            await session.execute(
                update(Reflection)
                .where(
                    Reflection.user_id == model.user_id,
                    Reflection.start_date == model.start_date,
                    Reflection.end_date == model.end_date,
                )
                .values(summary_text=model.summary_text)
            )
            await session.flush()

    async def get(
        self, *, user_id: int, start_date: str, end_date: str
    ) -> ReflectionVO | None:

        stmt = select(Reflection).where(
            Reflection.user_id == user_id,
            Reflection.start_date == start_date,
            Reflection.end_date == end_date,
        )

        result = await session.execute(stmt)

        reflection = result.scalar_one_or_none()

        return ReflectionVO.from_model(reflection) if reflection else None
