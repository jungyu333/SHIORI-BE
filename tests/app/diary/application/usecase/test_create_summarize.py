from unittest.mock import AsyncMock, MagicMock

import pytest
from shiori.app.celery import celery_app
from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import CreateSummarize


@pytest.fixture
def diary_service():
    return AsyncMock(spec=DiaryService)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_execute_success(diary_service):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    original_send_task = celery_app.send_task
    mock_send_task = MagicMock()
    celery_app.send_task = mock_send_task

    diary_service.can_summarize_diary.return_value = ["dummy_diary"]
    diary_service.prepare_summarize_diary.return_value = (
        [["dummy_input"]],
        ["meta_1"],
        ["20250810"],
    )

    use_case = CreateSummarize(diary_service=diary_service)

    # When
    result = await use_case.execute(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    # Then
    assert result is True
    diary_service.can_summarize_diary.assert_awaited_once_with(
        user_id=user_id, start=start_date, end=end_date
    )
    diary_service.prepare_summarize_diary.assert_awaited_once_with(
        week_diary=["dummy_diary"]
    )

    mock_send_task.assert_called_once_with(
        "summary_task",
        args=[
            {
                "user_id": user_id,
                "start": start_date,
                "end": end_date,
                "week_inputs": [["dummy_input"]],
                "diary_meta_ids": ["meta_1"],
                "dates": ["20250810"],
            }
        ],
        queue="summary-queue",
    )

    celery_app.send_task = original_send_task
