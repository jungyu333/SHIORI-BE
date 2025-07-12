import re

from pydantic import BaseModel, Field, field_validator


class LogInRequest(BaseModel):
    email: str = Field(..., examples=["jungyu3826@gmail.com"])
    password: str = Field(..., examples=["rlawnsrb1!"])

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:

        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not email_regex.match(v):
            raise ValueError("이메일 주소 형식이 올바르지 않습니다")

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("비밀번호에 최소 하나의 영문자가 포함되어야 합니다")
        if not re.search(r"\d", v):
            raise ValueError("비밀번호에 최소 하나의 숫자가 포함되어야 합니다")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("비밀번호에 최소 하나의 특수문자가 포함되어야 합니다")
        return v


class SignUpRequest(LogInRequest):
    email: str = Field(..., examples=["jungyu3826@gmail.com"])
    password: str = Field(..., examples=["rlawnsrb1!"])
    nickname: str = Field(..., examples=["jungyu"])
