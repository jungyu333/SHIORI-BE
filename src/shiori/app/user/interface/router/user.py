from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from shiori.app.container import Container
from shiori.app.core.response import StandardResponse
from shiori.app.user.application.usecase import CreateUserUseCase
from shiori.app.user.interface.dto import SignUpRequest, SignUpResponse

router = APIRouter()


@router.post("/signup", response_model=StandardResponse, tags=["User"])
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
