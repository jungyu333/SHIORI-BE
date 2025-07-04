import uuid
from datetime import datetime

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from ...utils import get_log_level_for_request, save_log_to_file
from ..schema import LogResult, RequestInfo


class RequestLogMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        trace_id = str(uuid.uuid4())

        scope.setdefault("state", {})
        scope["state"]["trace_id"] = trace_id

        level = get_log_level_for_request(request.url.path)

        request_info = RequestInfo(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            client=request.client.host if request.client else None,
        )

        log_result = LogResult(
            timestamp=datetime.utcnow().isoformat(),
            level=level,
            type="request",
            trace_id=trace_id,
            request=request_info.model_dump(),
        )

        await save_log_to_file(log_result)

        await self.app(scope, receive, send)
