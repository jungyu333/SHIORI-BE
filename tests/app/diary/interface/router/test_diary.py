import pytest
from httpx import AsyncClient

from shiori.app.server import app
from shiori.app.utils.helpers import TokenHelper

BASE_URL = "http://test"


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
    assert response.json().get("data") == None
