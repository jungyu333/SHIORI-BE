from datetime import timedelta, datetime
from unittest.mock import AsyncMock

import pytest
from pymongo.errors import PyMongoError

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.domain.entity import (
    DiaryVO,
    DiaryBlockVO,
    DiaryMetaVO,
    ReflectionVO,
)
from shiori.app.diary.domain.exception import (
    NotValidDateFormat,
    NotValidTitle,
    NotValidDateRange,
    SummarizeFailed,
)
from shiori.app.diary.domain.repository import (
    DiaryRepository,
    DiaryMetaRepository,
    TagRepository,
    ReflectionRepository,
)
from shiori.app.diary.domain.schema import EmotionResult
from shiori.app.diary.infra.model import ProseMirror


@pytest.fixture
def diary_repository_mock():
    return AsyncMock(spec=DiaryRepository)


@pytest.fixture
def diary_meta_repository_mock():
    return AsyncMock(spec=DiaryMetaRepository)


@pytest.fixture
def tag_repository_mock():
    return AsyncMock(spec=TagRepository)


@pytest.fixture
def reflection_repository_mock():
    return AsyncMock(spec=ReflectionRepository)


@pytest.fixture
def diary_service(
    diary_repository_mock,
    diary_meta_repository_mock,
    tag_repository_mock,
    reflection_repository_mock,
):
    return DiaryService(
        diary_repo=diary_repository_mock,
        diary_meta_repo=diary_meta_repository_mock,
        tag_repo=tag_repository_mock,
        reflection_repo=reflection_repository_mock,
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


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_diary_content_none(diary_repository_mock, diary_service):
    # Given
    user_id = 1
    date = "20250728"

    diary_repository_mock.get_diary_by_date.return_value = None

    # When

    result = await diary_service.get_diary_content(
        user_id=user_id,
        date=date,
    )

    # Then
    assert result is None


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_diary_content_invalid_date(diary_repository_mock, diary_service):
    # Given
    user_id = 1
    date = "2025-07-28"

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

    # When, Then

    with pytest.raises(NotValidDateFormat) as e:
        result = await diary_service.get_diary_content(
            user_id=user_id,
            date=date,
        )

    assert str(e.value.message) == "잘못된 날짜 형식이에요."
    assert e.value.code == 422


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary_meta(diary_meta_repository_mock, diary_service):
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

    diary_meta_repository_mock.get_diary_meta_by_date_range.return_value = diary_metas

    # When
    result = await diary_service.get_week_diary_meta(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )

    # Then
    assert len(result) == len(diary_metas)
    for i, vo in enumerate(result):
        assert vo.date == date_list[i]
        assert vo.user_id == user_id


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary_meta_invalid_date_format(
    diary_repository_mock, diary_service
):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    invalid_start_date = "2025-08-10"
    invalid_end_date = "2025-08-16"

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

    # When, Then

    with pytest.raises(NotValidDateFormat) as e:
        result = await diary_service.get_week_diary_meta(
            user_id=user_id,
            start=invalid_start_date,
            end=invalid_end_date,
        )

    assert e.value.message == "잘못된 날짜 형식이에요."
    assert e.value.code == 422


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary_meta_invalid_date_range(
    diary_repository_mock, diary_service
):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    invalid_start_date = "20250816"
    invalid_end_date = "20250810"

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

    # When, Then
    with pytest.raises(NotValidDateRange) as e:
        result = await diary_service.get_week_diary_meta(
            user_id=user_id,
            start=invalid_start_date,
            end=invalid_end_date,
        )

    assert e.value.message == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert e.value.code == 400


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary(diary_repository_mock, diary_service):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

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

    expected = [diary_vo_mock] * 7

    diary_repository_mock.get_diary_by_date_range.return_value = expected

    # When

    result = await diary_service.get_week_diary(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )

    # Then
    assert result == expected
    assert len(result) == len(expected)
    assert diary_repository_mock.get_diary_by_date_range.call_count == 1


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary_invalid_date_format(diary_repository_mock, diary_service):
    # Given
    user_id = 1
    start_date = "2025-08-10"
    end_date = "2025-08-16"

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

    expected = [diary_vo_mock] * 7

    diary_repository_mock.get_diary_by_date_range.return_value = expected

    # When, Then
    with pytest.raises(NotValidDateFormat) as e:
        result = await diary_service.get_week_diary_meta(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

    assert e.value.message == "잘못된 날짜 형식이에요."
    assert e.value.code == 422
    assert diary_repository_mock.get_diary_by_date_range.call_count == 0


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_get_week_diary_invalid_date_range(diary_repository_mock, diary_service):
    # Given
    user_id = 1
    start_date = "20250816"
    end_date = "20250810"

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

    expected = [diary_vo_mock] * 7

    diary_repository_mock.get_diary_by_date_range.return_value = expected

    # When, Then
    with pytest.raises(NotValidDateRange) as e:
        result = await diary_service.get_week_diary_meta(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

    assert e.value.message == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert e.value.code == 400
    assert diary_repository_mock.get_diary_by_date_range.call_count == 0


@pytest.mark.asyncio
@pytest.mark.mongo
async def test_summarize_diary(
    diary_repository_mock, tag_repository_mock, diary_service
):
    # Given

    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

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
    diary_vo_mock.diary_meta_id = "dummy_diary_meta_id"

    diary_vo_mock.diary_blocks = [
        DiaryBlockVO(
            order=0,
            type="paragraph",
            content="hello",
            textAlign="left",
            marks=["bold"],
        )
    ]

    expected = [diary_vo_mock] * 7

    diary_repository_mock.get_diary_by_date_range.return_value = expected

    tag_repository_mock.upsert.return_value = None

    diary_service._emotion_pipeline.analyze = AsyncMock()
    diary_service._emotion_pipeline.analyze.return_value = [
        EmotionResult(predicted="행복", probabilities={"행복": 0.9, "슬픔": 0.1})
    ] * 7

    diary_service._adaptor.convert_week = AsyncMock(return_value=["dummy"] * 7)
    diary_service._summarize_pipeline.run = AsyncMock()
    diary_service._summarize_pipeline.return_value = "dummy_value"

    # When

    result = await diary_service.summarize_diary(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )

    # Then
    assert result == True


@pytest.mark.asyncio
async def test_summarize_diary_llm_failure(
    diary_repository_mock,
    tag_repository_mock,
    reflection_repository_mock,
    diary_service,
):
    # Given
    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    diary_vo_mock = AsyncMock(spec=DiaryVO)
    diary_vo_mock.diary_meta_id = "dummy_diary_meta_id"
    diary_vo_mock.diary_blocks = [
        DiaryBlockVO(
            order=0,
            type="paragraph",
            content="hello",
            textAlign="left",
            marks=["bold"],
        )
    ]

    diary_repository_mock.get_diary_by_date_range.return_value = [diary_vo_mock] * 7
    tag_repository_mock.upsert.return_value = None

    diary_service._adaptor.convert_week = AsyncMock(return_value=["dummy"] * 7)
    diary_service._emotion_pipeline.analyze = AsyncMock(
        return_value=[
            EmotionResult(predicted="행복", probabilities={"행복": 0.9, "슬픔": 0.1})
        ]
        * 7
    )

    diary_service._summarize_pipeline.run = AsyncMock(
        side_effect=Exception("LLM error")
    )

    # When, Then
    with pytest.raises(SummarizeFailed) as e:
        await diary_service.summarize_diary(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

    assert e.value.code == 503
    assert e.value.message == "요약 처리에 실패했습니다. 잠시 후 다시 시도해주세요."


async def test_summarize_diary_return_none_diary(diary_repository_mock, diary_service):

    # Given

    user_id = 1
    start_date = "20250810"
    end_date = "20250816"

    diary_repository_mock.get_diary_by_date_range.return_value = []

    # When

    result = await diary_service.summarize_diary(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )

    # Then

    assert result == False


@pytest.mark.asyncio
async def test_upsert_diary_tag(tag_repository_mock, diary_service):
    # Given

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
    diary_vo_mock.diary_meta_id = "dummy_diary_meta_id"

    diary_vo_mock.diary_blocks = [
        DiaryBlockVO(
            order=0,
            type="paragraph",
            content="hello",
            textAlign="left",
            marks=["bold"],
        )
    ]

    diary_vo_list = [diary_vo_mock] * 7

    tag_repository_mock.upsert.return_value = None

    emotion_props = [
        EmotionResult(
            predicted="행복",
            probabilities={
                "공포": 0.0,
                "놀람": 0.0,
                "분노": 0.0,
                "슬픔": 0.0,
                "중립": 0.0,
                "행복": 1.0,
                "혐오": 0.0,
            },
        )
    ] * 7

    # When

    result = await diary_service.upsert_diary_tag(
        diary=diary_vo_list, emotion_probs=emotion_props
    )

    # Then

    assert result is None
    assert tag_repository_mock.upsert.call_count == len(diary_vo_list)


@pytest.mark.asyncio
async def test_get_reflection(diary_service, reflection_repository_mock):
    # Given

    user_id = 1
    start_date = "20250811"
    end_date = "20250817"
    summary_text = "summary_text"

    reflection_mock = ReflectionVO(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        summary_text=summary_text,
    )

    reflection_repository_mock.get.return_value = reflection_mock

    # When

    result = await diary_service.get_reflection(
        user_id=user_id,
        start=start_date,
        end=end_date,
    )

    # Then
    assert result is not None
    assert result.user_id == user_id
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.summary_text == summary_text

    reflection_repository_mock.get.assert_awaited_once_with(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )


@pytest.mark.asyncio
async def test_get_reflection_invalid_date_format(
    diary_service, reflection_repository_mock
):
    # Given
    user_id = 1
    invalid_start_date = "2025-08-11"
    end_date = "20250817"

    # When, Then
    with pytest.raises(NotValidDateFormat) as e:
        await diary_service.get_reflection(
            user_id=user_id,
            start=invalid_start_date,
            end=end_date,
        )

    assert e.value.message == "잘못된 날짜 형식이에요."
    assert e.value.code == 422
    assert reflection_repository_mock.get.call_count == 0


@pytest.mark.asyncio
async def test_get_reflection_invalid_date_range(
    diary_service, reflection_repository_mock
):
    # Given
    user_id = 1
    start_date = "20250817"
    end_date = "20250811"

    # When, Then
    with pytest.raises(NotValidDateRange) as e:
        await diary_service.get_reflection(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

    assert e.value.message == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert e.value.code == 400
    assert reflection_repository_mock.get.call_count == 0
