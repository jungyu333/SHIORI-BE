from unittest.mock import AsyncMock

import pytest

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import UpsertDiary
from shiori.app.diary.infra.model import ProseMirror


@pytest.fixture()
def diary_service_mock():
    return AsyncMock(spec=DiaryService)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_execute(diary_service_mock):
    # Given

    user_id = 1
    date = "20250728"
    title = "dummy_title"
    version = None
    diary_content_dict = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [
                    {"type": "text", "text": "hello", "marks": [{"type": "bold"}]}
                ],
            }
        ],
    }

    content = ProseMirror(**diary_content_dict)

    diary_service_mock.upsert_diary.return_value = "dummy_id", True

    use_case = UpsertDiary(diary_service=diary_service_mock)

    # When

    diary_id, is_created = await use_case.execute(
        user_id=user_id, date=date, content=content, title=title, version=version
    )

    # Then

    assert is_created
    assert diary_id is not None
    diary_service_mock.upsert_diary.assert_awaited_with(
        user_id=user_id, date=date, content=content, title=title, version=version
    )
