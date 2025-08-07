from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Request

from shiori.app.container import Container
from shiori.app.core.dependencies import IsAuthenticated, PermissionDependency
from shiori.app.core.response import StandardResponse
from shiori.app.diary.application.usecase import UpsertDiary
from shiori.app.diary.interface.dto import UpsertDiaryRequest

router = APIRouter()


@router.post(
    "/{date}",
    response_model=StandardResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def upsert_diary(
    body: UpsertDiaryRequest,
    request: Request,
    date: str = Path(..., description="일기 작성 날짜 (예: 20250805)"),
    use_case: UpsertDiary = Depends(Provide[Container.upsert_diary]),
):

    content = body.content
    title = body.title

    user_id = request.user.id

    diary_id, is_created = await use_case.execute(
        date=date,
        user_id=user_id,
        content=content,
        title=title,
    )

    return {"code": 201 if is_created else 200, "message": "저장 되었어요!"}
