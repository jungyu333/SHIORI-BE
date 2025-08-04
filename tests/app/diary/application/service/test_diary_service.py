from unittest.mock import AsyncMock

import pytest
from pymongo.errors import PyMongoError

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.domain.repository import DiaryRepository, DiaryMetaRepository
from shiori.app.diary.infra.model import ProseMirror

diary_repository_mock = AsyncMock(spec=DiaryRepository)
diary_meta_repository_mock = AsyncMock(spec=DiaryMetaRepository)
diary_service = DiaryService(
    diary_repo=diary_repository_mock, diary_meta_repo=diary_meta_repository_mock
)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary():
    # Given
    user_id = 1
    diary_meta_id = 123
    date = "20250728"

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

    diary_repository_mock.save_diary.return_value = "mock_diary_id"

    # When

    diary_id = await diary_service.save_diary(
        user_id=user_id, diary_meta_id=diary_meta_id, content=content, date=date
    )

    # Then
    assert diary_id is not None
    assert isinstance(diary_id, str)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary_raises_exception():
    # Given
    user_id = 1
    diary_meta_id = 123
    date = "20250728"

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

    diary_repository_mock.save_diary.side_effect = PyMongoError("DB error")

    # When Then
    with pytest.raises(PyMongoError):
        await diary_service.save_diary(
            user_id=user_id, diary_meta_id=diary_meta_id, content=content, date=date
        )


@pytest.mark.asyncio
async def test_save_diary_meta():
    # Given
    user_id = 1
    date = "20250728"
    title = "dummy_title"

    diary_meta_repository_mock.save_diary_meta.return_value = None

    # When

    response = await diary_service.save_diary_meta(
        user_id=user_id,
        date=date,
        title=title,
    )

    # Then

    assert diary_meta_repository_mock.save_diary_meta.call_count == 1
    assert response is None
