import pytest
from httpx import AsyncClient

from shiori.app.diary.domain.entity import ReflectionVO
from shiori.app.server import app
from shiori.app.user.domain.entity import UserVO
from shiori.app.utils.helpers import TokenHelper

BASE_URL = "http://test"


@pytest.fixture
def access_token_mock():
    return TokenHelper.encode({"user_id": 1, "is_admin": False})


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_upsert_diary(access_token_mock):
    # Given
    access_token = access_token_mock

    date = "20250728"
    content = {
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

    title = "test_title"

    body = {
        "content": content,
        "title": title,
    }

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post(f"/api/diary/{date}", json=body)

    # Then

    assert response.json().get("code") == 201
    assert response.json().get("message") == "저장 되었어요!"
    assert response.json().get("data").get("id") is not None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_upsert_diary_update(access_token_mock):
    # Given
    access_token = access_token_mock

    date = "20250728"
    version = 1
    content = {
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

    title = "test_title"

    body = {
        "content": content,
        "title": title,
    }
    body2 = {"content": content, "title": title, "version": version}
    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post(f"/api/diary/{date}", json=body)

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post(f"/api/diary/{date}", json=body2)

    # Then
    assert response.json().get("code") == 200
    assert response.json().get("message") == "저장 되었어요!"
    assert response.json().get("data").get("id") is not None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_upsert_diary_invalid_date(access_token_mock):
    # Given
    access_token = access_token_mock

    date = "2025-07-28"
    content = {
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

    title = "test_title"

    body = {
        "content": content,
        "title": title,
    }

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post(f"/api/diary/{date}", json=body)

    # Then
    assert response.json().get("code") == 422
    assert response.json().get("message") == "잘못된 날짜 형식이에요."
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_diary_empty(access_token_mock):
    # Given
    access_token = access_token_mock
    date = "20250728"

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(f"/api/diary/{date}")

    # Then

    assert response.json().get("code") == 200
    assert response.json().get("message") == ""
    assert response.json().get("data").get("content") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_diary_invalid_date(access_token_mock):
    # Given
    access_token = access_token_mock
    date = "2025-07-28"

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(f"/api/diary/{date}")

    # Then
    assert response.json().get("code") == 422
    assert response.json().get("message") == "잘못된 날짜 형식이에요."
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_diary(access_token_mock):
    # Given
    access_token = access_token_mock
    date = "20250728"

    content = {
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

    title = "test_title"

    body = {
        "content": content,
        "title": title,
    }

    # When
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        await client.post(f"/api/diary/{date}", json=body)

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(f"/api/diary/{date}")

    # Then
    assert response.json().get("code") == 200
    assert response.json().get("message") == ""
    assert response.json().get("data").get("content") == content


@pytest.mark.mongo
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_dates, expected_count",
    [
        (["20250810", "20250812", "20250814"], 3),
        (["20250801", "20250802", "20250803"], 0),
    ],
)
async def test_get_week_diary_meta(access_token_mock, test_dates, expected_count):
    # Given
    access_token = access_token_mock

    start_date = "20250810"
    end_date = "20250816"

    content = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [{"type": "text", "text": "test"}],
            }
        ],
    }

    body = {"content": content, "title": "test_title"}

    headers = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        for date in test_dates:
            await client.post(f"/api/diary/{date}", json=body)

        # When
        response = await client.get(f"/api/diary?start={start_date}&end={end_date}")

    # Then
    assert response.json().get("code") == 200
    assert response.json().get("message") == ""
    assert len(response.json().get("data")) == expected_count


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_week_diary_meta_omission_date(access_token_mock):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = None

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(f"/api/diary?start={invalid_start_date}")

    # Then
    assert response.json().get("code") == 422
    assert response.json().get("message") == "요청값이 올바르지 않아요!"
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_week_diary_meta_invalid_date_format(access_token_mock):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = "2025-08-10"
    invalid_end_date = "2025-08-16"

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(
            f"/api/diary?start={invalid_start_date}&end={invalid_end_date}"
        )

    # Then

    assert response.json().get("code") == 422
    assert response.json().get("message") == "잘못된 날짜 형식이에요."
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_get_week_diary_meta_invalid_date_range(access_token_mock):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = "20250816"
    invalid_end_date = "20250810"

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(
            f"/api/diary?start={invalid_start_date}&end={invalid_end_date}"
        )

    # Then
    assert response.json().get("code") == 400
    assert response.json().get("message") == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_summarize_diary_none_diary(access_token_mock):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}
    start_date = "20250810"
    end_date = "20250816"
    body = {"start": start_date, "end": end_date}

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post("/api/diary/summary", json=body)

    # Then
    assert response.json().get("code") == 204
    assert (
        response.json().get("message") == "요약할 일지가 없어요! 일지를 작성해주세요!"
    )
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_dates",
    [
        [
            "20250810",
            "20250811",
            "20250812",
            "20250813",
            "20250814",
            "20250815",
            "20250816",
        ],
    ],
)
async def test_summarize_diary(access_token_mock, test_dates):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    start_date = "20250810"
    end_date = "20250816"

    summary_body = {
        "start": start_date,
        "end": end_date,
    }

    content = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [{"type": "text", "text": "test"}],
            }
        ],
    }

    body = {"content": content, "title": "test_title"}

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        for date in test_dates:
            await client.post(f"/api/diary/{date}", json=body)

        # When
        response = await client.post(f"/api/diary/summary", json=summary_body)

    # Then
    assert response.json().get("code") == 200
    assert (
        response.json().get("message") == "요약이 시작되었어요! 잠시 후 확인해보세요."
    )
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_summarize_diary_invalid_date_format(access_token_mock):
    # Given
    access_token = access_token_mock

    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = "2025-08-10"
    invalid_end_date = "2025-08-16"

    body = {"start": invalid_start_date, "end": invalid_end_date}

    # When

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post("/api/diary/summary", json=body)

    # Then

    assert response.json().get("code") == 422
    assert response.json().get("message") == "잘못된 날짜 형식이에요."
    assert response.json().get("data") is None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_summarize_diary_invalid_date_range(access_token_mock):
    # Given
    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = "20250816"
    invalid_end_date = "20250810"

    body = {"start": invalid_start_date, "end": invalid_end_date}

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post("/api/diary/summary", json=body)

    # Then
    assert response.json().get("code") == 400
    assert response.json().get("message") == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert response.json().get("data") is None


@pytest.mark.asyncio
async def test_get_reflections(access_token_mock, session):
    # Given

    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    user_id = 1
    start_date = "20250810"
    end_date = "20250816"
    summary_text = "dummy summary"

    reflection = ReflectionVO(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        summary_text=summary_text,
    )

    user = UserVO(
        id=1,
        nickname="test_user",
        email="test@example.com",
        password="hashed_pw",
        is_admin=False,
    )

    session.add(user.to_model())

    await session.commit()

    model = reflection.to_model()

    session.add(model)

    await session.commit()

    start_date = "20250810"
    end_date = "20250816"

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(
            f"/api/diary/reflections?start={start_date}&end={end_date}"
        )

    # Then
    assert response.json().get("code") == 200
    assert response.json().get("message") == ""
    assert response.json().get("data").get("reflection") == summary_text


@pytest.mark.asyncio
async def test_get_reflections_invalid_date_format(access_token_mock):
    # Given

    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_start_date = "2025-08-10"
    end_date = "20250816"

    # When
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(
            f"/api/diary/reflections?start={invalid_start_date}&end={end_date}"
        )

    # Then
    assert response.json().get("code") == 422
    assert response.json().get("message") == "잘못된 날짜 형식이에요."
    assert response.json().get("data") is None


@pytest.mark.asyncio
async def test_get_reflections_invalid_date_range(access_token_mock):
    # Given

    access_token = access_token_mock
    headers = {"Authorization": f"Bearer {access_token}"}

    start_date = "20250816"
    end_date = "20250810"

    # When

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.get(
            f"/api/diary/reflections?start={start_date}&end={end_date}"
        )

    # Then
    assert response.json().get("code") == 400
    assert response.json().get("message") == "시작 날짜와 끝 날짜가 유효하지 않아요!"
    assert response.json().get("data") is None
