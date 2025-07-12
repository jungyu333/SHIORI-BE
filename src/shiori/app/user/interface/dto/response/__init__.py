from pydantic import BaseModel, Field


class SignUpResponse(BaseModel):
    user_id: int = Field(..., description="User Id")


class LogInResponse(BaseModel):
    token: str = Field(..., description="Access Token")
