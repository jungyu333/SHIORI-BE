from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from shiori.app.core.database import session
from shiori.app.diary.domain.entity import ReflectionVO
from shiori.app.diary.domain.repository import ReflectionRepository
from shiori.app.diary.infra.model import Reflection


class ReflectionRepositoryImpl(ReflectionRepository):

    async def upsert(self, *, reflection: ReflectionVO) -> int | None:

        model = reflection.to_model()

        session.add(model)

        try:
            await session.flush()
        except IntegrityError:

            await session.rollback()
            result = await session.execute(
                update(Reflection)
                .where(
                    Reflection.user_id == model.user_id,
                    Reflection.start_date == model.start_date,
                    Reflection.end_date == model.end_date,
                )
                .values(summary_text=model.summary_text)
                .returning(Reflection.id)
            )
            reflection_id = result.scalar_one()

            return reflection_id
