from fastapi import APIRouter

from shiori.app.core.response import StandardResponse

router = APIRouter()


@router.post(
    "/refresh",
    response_model=StandardResponse,
)
async def refresh_token():
    pass
