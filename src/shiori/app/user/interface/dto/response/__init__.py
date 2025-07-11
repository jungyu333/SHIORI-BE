from pydantic import BaseModel, Field


class SignUpResponse(BaseModel):
    user_id: int


class LogInResponse(BaseModel):
    token: str = Field(..., description="Access Token")
