from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    method: str = Field(title="HTTP Method")
    url: str = Field(title="Request URL")
    client: Optional[str] = Field(default=None, title="Client IP")
    headers: dict[str, str] | None = Field(default=None, title="Request Headers")


class ResponseInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    headers: dict[str, str] | None = Field(default=None, title="Response headers")
    status_code: Optional[int] = Field(default=None, title="Status code")


class LogResult(BaseModel):
    timestamp: str
    level: str
    type: Literal["response", "request", "service"]
    trace_id: Optional[str] = None
    message: Optional[str] = None
    response: Optional[ResponseInfo] = None
    request: Optional[RequestInfo] = None
    duration_ms: Optional[float] = None
