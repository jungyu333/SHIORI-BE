from pydantic import BaseModel


class SignUpResponse(BaseModel):
    user_id: int
