from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from shiori.app.container import Container
from shiori.app.core.response import StandardResponse
from shiori.app.internal.application.usecase import SummarizeResult

router = APIRouter()


class SummarizeResultRequest(BaseModel):
    user_id: int
    start: str
    end: str
    reflection: str
    emotion_results: list[dict]
    diary_meta_ids: list[str]


@router.post("/summarize/result", response_model=StandardResponse)
@inject
async def summarize_call_back(
    request: SummarizeResultRequest,
    use_case: SummarizeResult = Depends(Provide[Container.summarize_result]),
):
    await use_case.execute(
        user_id=request.user_id,
        start=request.start,
        end=request.end,
        reflection=request.reflection,
        emotion_results=request.emotion_results,
        diary_meta_ids=request.diary_meta_ids,
    )

    return {
        "code": 200,
    }
