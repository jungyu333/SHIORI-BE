from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Response

from shiori.app.container import Container
from shiori.app.core import get_settings
from shiori.app.core.response import StandardResponse
from shiori.app.user.application.usecase import CreateUserUseCase, LoginUserUseCase
from shiori.app.user.interface.dto import SignUpRequest, SignUpResponse, LogInRequest
from shiori.app.user.interface.dto.response import LogInResponse

router = APIRouter()

config = get_settings()


@router.post("/signup", response_model=StandardResponse[SignUpResponse])
@inject
async def signup(
    request: SignUpRequest = Body(...),
    create_user_use_case: CreateUserUseCase = Depends(Provide[Container.create_user]),
):
    email = request.email
    password = request.password
    nickname = request.nickname

    user_id = await create_user_use_case.execute(email, password, nickname)

    response = SignUpResponse(user_id=user_id)

    return {"code": 201, "message": "환영합니다!", "data": response}


@router.post("/login", response_model=StandardResponse[LogInResponse])
@inject
async def login(
    request: LogInRequest,
    response: Response,
    use_case: LoginUserUseCase = Depends(Provide[Container.login_user]),
):
    email = request.email
    password = request.password

    access_token, refresh_token = await use_case.execute(email, password)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=config.ENV == "production",
        samesite="strict",
        path="/api/auth/refresh",
    )

    return {
        "code": 200,
        "message": "환영합니다!",
        "data": LogInResponse(
            token=access_token,
        ),
    }
