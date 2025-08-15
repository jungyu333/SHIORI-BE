import pytest
from httpx import AsyncClient

from shiori.app.server import app
from shiori.app.utils.helpers import TokenHelper

BASE_URL = "http://test"


@pytest.fixture
def access_token_mock():
    return TokenHelper.encode({"user_id": 1, "is_admin": False})


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_upsert_diary():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})

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
async def test_upsert_diary_update():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})

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

    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as client:
        response = await client.post(f"/api/diary/{date}", json=body)

    # Then
    assert response.json().get("code") == 200
    assert response.json().get("message") == "저장 되었어요!"
    assert response.json().get("data").get("id") is not None


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_upsert_diary_invalid_date():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})

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
async def test_get_diary_empty():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
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
async def test_get_diary_invalid_date():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
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
async def test_get_diary():
    # Given
    access_token = TokenHelper.encode({"user_id": 1, "is_admin": False})
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
async def test_get_week_diary_meta(access_token_mock):
    # Given
    access_token = access_token_mock

    start_date = "20250810"
    end_date = "20250816"

    test_dates = ["20250810", "20250812", "20250814"]
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
    assert len(response.json().get("data")) == len(test_dates)
