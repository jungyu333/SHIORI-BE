from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .container import Container
from .core.exceptions import BaseCustomException
from .core.middleware import (RequestLogMiddleware, ResponseLogMiddleware,
                              SQLAlchemyMiddleware)
from .user.interface.router import user_router


def init_router(app_: FastAPI) -> None:
    container = Container()
    app_.include_router(user_router, prefix="/api/user", tags=["user"])


def init_listener(app_: FastAPI) -> None:

    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = exc.errors()

        def clean_msg(msg: str) -> str:

            if msg.lower().startswith("value error, "):
                return msg[13:].strip()
            return msg

        first_msg = (
            clean_msg(errors[0]["msg"]) if errors else "요청값이 올바르지 않습니다"
        )

        custom_exception = BaseCustomException(code=422, message=first_msg, data=None)

        return JSONResponse(
            status_code=422,
            content={
                "code": custom_exception.code,
                "message": custom_exception.message,
                "data": None,
            },
        )

    @app_.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": exc.data,
            },
        )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(RequestLogMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Shiori Be",
        description="Shiori Be",
        version="1.0.0",
        middleware=make_middleware(),
    )
    init_router(app_)
    init_listener(app_)

    return app_


app = create_app()
