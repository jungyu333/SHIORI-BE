from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import DiaryMetaVO
from shiori.app.diary.infra.model import SummaryStatus


class DiaryMetaRepository(ABC):

    @abstractmethod
    async def save_diary_meta(self, diary_meta: DiaryMetaVO) -> str:
        pass

    @abstractmethod
    async def get_diary_meta_by_date_range(
        self, user_id: int, start_date: str, end_date: str
    ) -> list[DiaryMetaVO]:
        pass

    @abstractmethod
    async def update_summary_status_by_meta_id(
        self, diary_meta_id: list[str], status: SummaryStatus
    ) -> None:
        pass
