from unittest.mock import AsyncMock

import pytest
from pymongo.errors import PyMongoError

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.domain.entity import diary as DiaryVO
from shiori.app.diary.domain.exception import NotValidDateFormat, NotValidTitle
from shiori.app.diary.domain.repository import DiaryRepository, DiaryMetaRepository
from shiori.app.diary.infra.model import ProseMirror


@pytest.fixture
def diary_repository_mock():
    return AsyncMock(spec=DiaryRepository)


@pytest.fixture
def diary_meta_repository_mock():
    return AsyncMock(spec=DiaryMetaRepository)


@pytest.fixture
def diary_service(diary_repository_mock, diary_meta_repository_mock):
    return DiaryService(
        diary_repo=diary_repository_mock,
        diary_meta_repo=diary_meta_repository_mock,
    )


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    diary_meta_id = "123"
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

    diary_repository_mock.save_diary.return_value = "mock_diary_id", True

    # When

    diary_id, is_created = await diary_service.save_diary(
        user_id=user_id, diary_meta_id=diary_meta_id, content=content, date=date
    )

    # Then
    assert diary_id is not None
    assert isinstance(diary_id, str)


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary_raises_exception(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    diary_meta_id = "123"
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

    # When, Then
    with pytest.raises(PyMongoError):
        await diary_service.save_diary(
            user_id=user_id, diary_meta_id=diary_meta_id, content=content, date=date
        )


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary_meta(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
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


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary_meta_invalid_date_format(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    date = "2025-07-28"
    title = "dummy_title"

    diary_meta_repository_mock.save_diary_meta.return_value = None

    # When, Then

    with pytest.raises(NotValidDateFormat) as e:
        await diary_service.save_diary_meta(
            user_id=user_id,
            date=date,
            title=title,
        )

    assert str(e.value.message) == "잘못된 날짜 형식이에요."
    assert e.value.code == 422


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_save_diary_meta_invalid_title(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    date = "20250728"
    title = "a" * 51

    diary_meta_repository_mock.save_diary_meta.return_value = None

    # When, Then

    with pytest.raises(NotValidTitle) as e:
        await diary_service.save_diary_meta(
            user_id=user_id,
            date=date,
            title=title,
        )

    assert str(e.value.message) == "일지 제목은 50자 이내로 작성 해 주세요."
    assert e.value.code == 400


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_upsert_diary(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given

    user_id = 1
    date = "20250728"
    title = "dummy_title"

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

    diary_repository_mock.save_diary.return_value = "mock_diary_id", True
    diary_meta_repository_mock.save_diary_meta.return_value = "mock_diary_meta_id"

    # When

    diary_id, is_created = await diary_service.upsert_diary(
        user_id=user_id,
        date=date,
        content=content,
        title=title,
    )

    # Then

    assert diary_repository_mock.save_diary.call_count == 1
    assert diary_meta_repository_mock.save_diary_meta.call_count == 1
    assert diary_id == "mock_diary_id"
    assert is_created


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_upsert_diary_raises_save_diary_meta(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    date = "20250728"
    title = "dummy_title"

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

    diary_repository_mock.save_diary.return_value = "mock_diary_id", True
    diary_meta_repository_mock.save_diary_meta.return_value = None

    # When

    diary_id, is_created = await diary_service.upsert_diary(
        user_id=user_id,
        date=date,
        content=content,
        title=title,
    )

    # Then

    assert diary_repository_mock.save_diary.call_count == 0
    assert diary_meta_repository_mock.save_diary_meta.call_count == 1
    assert diary_id is None
    assert is_created is None


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_upsert_diary_invalid_date_format(
    diary_repository_mock, diary_meta_repository_mock, diary_service
):
    # Given
    user_id = 1
    date = "2025-07-28"
    title = "dummy_title"

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

    diary_repository_mock.save_diary.return_value = "mock_diary_id", True
    diary_meta_repository_mock.save_diary_meta.return_value = "mock_diary_meta_id"

    # When, Then

    with pytest.raises(NotValidDateFormat) as e:
        await diary_service.upsert_diary(
            user_id=user_id,
            date=date,
            content=content,
            title=title,
        )

    assert str(e.value.message) == "잘못된 날짜 형식이에요."
    assert e.value.code == 422
    assert diary_repository_mock.save_diary.call_count == 0


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_diary_content(diary_repository_mock, diary_service):
    # Given
    user_id = 1
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

    diary_vo_mock = AsyncMock(spec=DiaryVO)
    diary_vo_mock.diary_content = content

    diary_repository_mock.get_diary_by_date.return_value = diary_vo_mock

    # When

    result = await diary_service.get_diary_content(
        user_id=user_id,
        date=date,
    )

    # Then
    assert result == content
