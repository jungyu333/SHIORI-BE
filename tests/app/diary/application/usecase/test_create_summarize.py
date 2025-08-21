from unittest.mock import AsyncMock

import pytest

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import CreateSummarize


@pytest.fixture
def diary_service():
    return AsyncMock(spec=DiaryService)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_execute(diary_service):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    diary_service.summarize_diary.return_value = True

    use_case = CreateSummarize(diary_service=diary_service)

    # When

    result = await use_case.execute(
        user_id=user_id, start_date=start_date, end_date=end_date
    )

    # Then

    assert result is True
    diary_service.summarize_diary.assert_awaited_once_with(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )
