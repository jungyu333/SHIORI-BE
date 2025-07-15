from pydantic import BaseModel, Field


class RefreshRequest(BaseModel):
    access_token: str = Field(..., description="Access token")


class VerifyRequest(RefreshRequest):
    pass
