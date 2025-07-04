from datetime import datetime

from fastapi import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from ...utils import get_log_level_for_response, save_log_to_file
from ..schema import LogResult, ResponseInfo


class ResponseLogMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        start = datetime.utcnow()
        send_buffer = []

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                send_buffer.append(message)
            elif message["type"] == "http.response.body":
                send_buffer.append(message)

        await self.app(scope, receive, send_wrapper)

        status_code = send_buffer[0]["status"]
        headers = dict(send_buffer[0].get("headers", []))
        body = b""
        for msg in send_buffer[1:]:
            body += msg.get("body", b"")

        trace_id = scope.get("state", {}).get("trace_id", "unknown")
        level = get_log_level_for_response(status_code)

        response_info = ResponseInfo(
            headers=headers,
            status_code=status_code,
        )

        log_result = LogResult(
            timestamp=datetime.utcnow().isoformat(),
            level=level,
            type="response",
            trace_id=trace_id,
            response=response_info.model_dump(),
            duration_ms=round((datetime.utcnow() - start).total_seconds() * 1000, 2),
        )

        await save_log_to_file(log_result)

        response = Response(
            content=body, status_code=status_code, headers=dict(response_info.headers)
        )
        response.headers["X-Trace_Id"] = trace_id
        await response(scope, receive, send)
