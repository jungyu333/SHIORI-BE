from unittest.mock import AsyncMock

import pytest

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import GetReflection
from shiori.app.diary.domain.entity import ReflectionVO


@pytest.fixture
def diary_service_mock():
    return AsyncMock(spec=DiaryService)


@pytest.mark.asyncio
async def test_execute(diary_service_mock):
    # Given
    user_id = 1
    start_date = "20250811"
    end_date = "20250818"

    summary_text = "dummy_text"

    reflection = ReflectionVO(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        summary_text=summary_text,
    )

    diary_service_mock.get_reflection.return_value = reflection

    use_case = GetReflection(diary_service=diary_service_mock)

    # When

    result = await use_case.execute(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    # Then
    assert result is not None
    assert result.user_id == user_id
    assert result.summary_text == summary_text
    assert result.start_date == start_date
    assert result.end_date == end_date

    diary_service_mock.get_reflection.assert_awaited_with(
        user_id=user_id, start=start_date, end=end_date
    )
