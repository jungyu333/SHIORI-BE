from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .container import Container
from .core.exceptions import BaseCustomException
from .core.middleware import (RequestLogMiddleware, ResponseLogMiddleware,
                              SQLAlchemyMiddleware)


def init_router(app_: FastAPI) -> None:
    container = Container()


def init_listener(app_: FastAPI) -> None:
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
