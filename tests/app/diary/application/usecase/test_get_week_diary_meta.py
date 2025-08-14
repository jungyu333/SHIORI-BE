from datetime import timedelta, datetime
from unittest.mock import AsyncMock

import pytest

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import GetWeekDiaryMeta
from shiori.app.diary.domain.entity import DiaryMetaVO


@pytest.fixture
def diary_service():
    return AsyncMock(spec=DiaryService)


@pytest.mark.asyncio
async def test_execute(diary_service):
    # Given

    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    date_list = [
        (datetime.strptime(start_date, "%Y%m%d") + timedelta(days=i)).strftime("%Y%m%d")
        for i in range(
            (
                datetime.strptime(end_date, "%Y%m%d")
                - datetime.strptime(start_date, "%Y%m%d")
            ).days
            + 1
        )
    ]

    diary_metas = []
    for date in date_list:
        mock_vo = AsyncMock(spec=DiaryMetaVO)
        mock_vo.date = date
        mock_vo.user_id = user_id
        diary_metas.append(mock_vo)

    diary_service.get_week_diary_meta.return_value = diary_metas

    use_case = GetWeekDiaryMeta(diary_service=diary_service)

    # When

    result = await use_case.execute(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    # Then
    assert result == diary_metas
    for i, vo in enumerate(diary_metas):
        assert vo.user_id == user_id
        assert vo.date == date_list[i]

    diary_service.get_week_diary_meta.assert_awaited_once_with(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )
