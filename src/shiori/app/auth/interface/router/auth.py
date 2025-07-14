from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Cookie, Response

from shiori.app.auth.application.usecase import RefreshUseCase
from shiori.app.auth.interface.dto import RefreshResponse, RefreshRequest
from shiori.app.container import Container
from shiori.app.core import get_settings
from shiori.app.core.response import StandardResponse

router = APIRouter()

config = get_settings()


@router.post(
    "/refresh",
    response_model=StandardResponse[RefreshResponse],
)
@inject
async def refresh_token(
    request: RefreshRequest,
    response: Response,
    refresh_token: str = Cookie(...),
    use_case: RefreshUseCase = Depends(Provide[Container.refresh]),
):
    access_token = request.access_token

    result = await use_case.execute(
        access_token=access_token, refresh_token=refresh_token
    )

    new_access_token = result.token
    new_refresh_token = result.refresh_token

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=config.ENV == "production",
        samesite="strict",
        path="/api/auth/refresh",
    )

    return {
        "code": 200,
        "message": "success",
        "data": RefreshResponse(
            token=new_access_token,
        ),
    }
