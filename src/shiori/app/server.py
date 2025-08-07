from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from shiori.app.auth.interface.router import auth_router
from shiori.app.container import Container
from shiori.app.core.database import lifespan_context
from shiori.app.core.exceptions import (
    AuthenticationException,
    BaseCustomException,
    ValidationException,
)
from shiori.app.core.helpers.cache import Cache, RedisBackend, CustomKeyMaker
from shiori.app.core.middleware import (
    AuthBackend,
    AuthenticationMiddleware,
    RequestLogMiddleware,
    ResponseLogMiddleware,
    SQLAlchemyMiddleware,
)
from shiori.app.diary.interface.router import diary_router
from shiori.app.user.interface.router import user_router


def init_router(app_: FastAPI) -> None:
    app_.include_router(user_router, prefix="/api/user", tags=["User"])
    app_.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
    app_.include_router(diary_router, prefix="/api/diary", tags=["Diary"])


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

        validation_exc = ValidationException(message=first_msg, data=None)

        return await custom_exception_handler(request, validation_exc)

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


def on_auth_error(request: Request, exc: Exception):
    if isinstance(exc, BaseCustomException):
        error = exc
    else:
        error = AuthenticationException(message=str(exc))

    return JSONResponse(
        status_code=error.code,
        content={
            "code": error.code,
            "message": error.message,
            "data": error.data,
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
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(RequestLogMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    container = Container()

    app_ = FastAPI(
        title="Shiori Be",
        description="Shiori Be",
        version="1.0.0",
        middleware=make_middleware(),
        lifespan=lifespan_context,
    )

    app_.container = container

    init_router(app_)
    init_listener(app_)
    init_cache()

    return app_


app = create_app()
