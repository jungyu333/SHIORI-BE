from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Request, Query

from shiori.app.container import Container
from shiori.app.core.dependencies import IsAuthenticated, PermissionDependency
from shiori.app.core.response import StandardResponse
from shiori.app.diary.application.usecase import (
    UpsertDiary,
    GetDiary,
    GetWeekDiaryMeta,
    CreateSummarize,
    GetReflection,
)
from shiori.app.diary.interface.dto import (
    UpsertDiaryRequest,
    UpsertDiaryResponse,
    GetDiaryResponse,
    WeekDiaryMeta,
    SummarizeDiaryRequest,
    GetReflectionResponse,
)

router = APIRouter()


@router.get(
    "/reflections",
    response_model=StandardResponse[GetReflectionResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_reflections(
    start: Annotated[str, Query(..., description="시작 날짜 (예: 20250810)")],
    end: Annotated[str, Query(..., description="끝 날짜 (예: 20250816)")],
    request: Request,
    use_case: GetReflection = Depends(Provide[Container.get_reflection]),
):

    user_id = request.user.id
    result = await use_case.execute(
        user_id=user_id,
        start_date=start,
        end_date=end,
    )

    response = GetReflectionResponse(reflection=result.summary_text) if result else None

    return {
        "code": 200,
        "message": "",
        "data": response,
    }


@router.post(
    "/summary",
    response_model=StandardResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def summarize_diary(
    body: SummarizeDiaryRequest,
    request: Request,
    use_case: CreateSummarize = Depends(Provide[Container.create_summarize]),
):
    user_id = request.user.id
    start_date = body.start
    end_date = body.end

    is_success = await use_case.execute(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "code": 200 if is_success else 204,
        "message": (
            "요약이 완료되었어요! 잠시 후 확인해보세요."
            if is_success
            else "요약할 일지가 없어요! 일지를 작성해주세요!"
        ),
    }


@router.post(
    "/{date}",
    response_model=StandardResponse[UpsertDiaryResponse],
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

    response = UpsertDiaryResponse(
        id=diary_id,
    )

    return {
        "code": 201 if is_created else 200,
        "message": "저장 되었어요!",
        "data": response,
    }


@router.get(
    "/{date}",
    response_model=StandardResponse[GetDiaryResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_diary(
    request: Request,
    date: str = Path(..., description="일기 작성 날짜 (예: 20250805)"),
    use_case: GetDiary = Depends(Provide[Container.get_diary]),
):

    user_id = request.user.id
    content = await use_case.execute(
        date=date,
        user_id=user_id,
    )

    response = GetDiaryResponse(content=content)

    return {
        "code": 200,
        "message": "",
        "data": response,
    }


@router.get(
    "",
    response_model=StandardResponse[list[WeekDiaryMeta]],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_week_diary_meta(
    start: Annotated[str, Query(..., description="시작 날짜 (예: 20250810)")],
    end: Annotated[str, Query(..., description="끝 날짜 (예: 20250816)")],
    request: Request,
    use_case: GetWeekDiaryMeta = Depends(Provide[Container.get_week_diary_meta]),
):

    user_id = request.user.id

    result = await use_case.execute(
        user_id=user_id,
        start_date=start,
        end_date=end,
    )

    response = [
        WeekDiaryMeta(
            date=diary_meta.date,
            title=diary_meta.title,
            summary_status=diary_meta.summary_status,
            is_archived=diary_meta.is_archived,
            updated_at=str(diary_meta.updated_at),
        )
        for diary_meta in result
    ]
    return {
        "code": 200,
        "message": "",
        "data": response,
    }
