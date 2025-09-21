from typing import Optional

from shiori.app.core.database import MongoTransactional, Transactional
from shiori.app.diary.domain.constants import REQUIRED_DAYS_FOR_SUMMARY
from shiori.app.diary.domain.entity import (
    DiaryBlockVO,
    DiaryVO,
    DiaryMetaVO,
    TagVO,
    ReflectionVO,
)
from shiori.app.diary.domain.repository import (
    DiaryRepository,
    DiaryMetaRepository,
    TagRepository,
    ReflectionRepository,
)
from shiori.app.diary.domain.schema import EmotionResult
from shiori.app.diary.domain.validator import DiaryMetaValidator
from shiori.app.diary.infra.emotion import EmotionPipeline, EmotionModel, EmotionAdaptor
from shiori.app.diary.infra.model import ProseMirror, SummaryStatus
from shiori.app.diary.infra.summarize import SummarizePipeline


class DiaryService:
    def __init__(
        self,
        diary_repo: DiaryRepository,
        diary_meta_repo: DiaryMetaRepository,
        tag_repo: TagRepository,
        reflection_repo: ReflectionRepository,
    ):
        self._diary_repo = diary_repo
        self._diary_meta_repo = diary_meta_repo
        self._tag_repo = tag_repo
        self._reflection_repo = reflection_repo
        self._adaptor = EmotionAdaptor()
        self._emotion_pipeline = EmotionPipeline(model=EmotionModel())
        self._summarize_pipeline = SummarizePipeline()

    async def save_diary(
        self,
        *,
        user_id: int,
        diary_meta_id: str,
        date: str,
        content: ProseMirror,
    ) -> tuple[str, bool]:

        diary_blocks = DiaryBlockVO.from_prosemirror(content.model_dump())

        diary = DiaryVO(
            user_id=user_id,
            diary_meta_id=diary_meta_id,
            date=date,
            diary_content=content,
            diary_blocks=diary_blocks,
        )

        diary_document_id, is_created = await self._diary_repo.save_diary(diary=diary)

        return diary_document_id, is_created

    async def save_diary_meta(
        self, *, user_id: int, date: str, title: str
    ) -> str | None:

        DiaryMetaValidator.validate_date_format(date)
        DiaryMetaValidator.validate_title(title)

        diary_meta_vo = DiaryMetaVO(
            user_id=user_id,
            date=date,
            title=title,
        )

        diary_meta_id = await self._diary_meta_repo.save_diary_meta(
            diary_meta=diary_meta_vo
        )

        return diary_meta_id

    @MongoTransactional()
    async def upsert_diary(
        self,
        *,
        user_id: int,
        date: str,
        content: ProseMirror,
        title: Optional[str] = "",
    ) -> tuple[str | None, bool | None]:

        diary_meta_id = await self.save_diary_meta(
            user_id=user_id, date=date, title=title
        )

        if diary_meta_id:
            diary_id, is_created = await self.save_diary(
                user_id=user_id,
                diary_meta_id=diary_meta_id,
                date=date,
                content=content,
            )

            return diary_id, is_created

        return None, None

    async def get_diary_content(self, *, user_id: int, date: str) -> ProseMirror | None:

        DiaryMetaValidator.validate_date_format(date)

        diary_vo = await self._diary_repo.get_diary_by_date(
            user_id=user_id,
            date=date,
        )

        if diary_vo:
            return diary_vo.diary_content

        return None

    async def get_week_diary_meta(
        self, *, user_id: int, start: str, end: str
    ) -> list[DiaryMetaVO]:

        DiaryMetaValidator.validate_date_format(start)
        DiaryMetaValidator.validate_date_format(end)

        DiaryMetaValidator.validate_date_range(start=start, end=end)

        diary_meta_list = await self._diary_meta_repo.get_diary_meta_by_date_range(
            user_id=user_id,
            start_date=start,
            end_date=end,
        )

        return diary_meta_list

    async def get_week_diary(
        self, *, user_id: int, start: str, end: str
    ) -> list[DiaryVO]:

        DiaryMetaValidator.validate_date_format(start)
        DiaryMetaValidator.validate_date_format(end)

        DiaryMetaValidator.validate_date_range(start=start, end=end)

        diary_list = await self._diary_repo.get_diary_by_date_range(
            user_id=user_id,
            start_date=start,
            end_date=end,
        )

        return diary_list

    @Transactional()
    async def upsert_diary_tag(
        self, *, diary: list[DiaryVO], emotion_probs: list[EmotionResult]
    ) -> None:

        for diary_vo, result in zip(diary, emotion_probs):
            predicted_label = result.predicted
            confidence = result.probabilities[predicted_label]

            tag_vo = TagVO(
                diary_meta_id=diary_vo.diary_meta_id,
                label=predicted_label,
                confidence=confidence,
            )

            await self._tag_repo.upsert(tag=tag_vo)

    @MongoTransactional()
    async def update_summary_status(
        self, *, diary_meta_id: list[str], status: SummaryStatus
    ):
        await self._diary_meta_repo.update_summary_status_by_meta_id(
            diary_meta_id=diary_meta_id,
            status=status,
        )

    @Transactional()
    async def upsert_reflection(
        self, *, reflection: str, user_id: int, start: str, end: str
    ) -> None:

        reflection_vo = ReflectionVO(
            user_id=user_id,
            start_date=start,
            end_date=end,
            summary_text=reflection,
        )

        await self._reflection_repo.upsert(reflection=reflection_vo)

    async def summarize_diary(self, *, user_id: int, start: str, end: str) -> bool:

        ## 7일치 diary get
        week_diary = await self.get_week_diary(
            user_id=user_id,
            start=start,
            end=end,
        )

        if len(week_diary) != REQUIRED_DAYS_FOR_SUMMARY:
            return False

        diary_meta_ids = [diary.diary_meta_id for diary in week_diary]

        try:
            ## tag inference

            await self.update_summary_status(
                diary_meta_id=diary_meta_ids, status=SummaryStatus.pending
            )

            week_inputs = self._adaptor.convert_week(diaries=week_diary)

            emotion_results = await self._emotion_pipeline.analyze(week_inputs)

            await self.upsert_diary_tag(diary=week_diary, emotion_probs=emotion_results)

            reflection = await self._summarize_pipeline.run(
                diaries=week_diary, emotions=emotion_results
            )

            await self.upsert_reflection(
                user_id=user_id, reflection=reflection, start=start, end=end
            )

            await self.update_summary_status(
                diary_meta_id=diary_meta_ids, status=SummaryStatus.completed
            )

            return True

        except Exception as e:

            await self.update_summary_status(
                diary_meta_id=diary_meta_ids, status=SummaryStatus.failed
            )
            return False
