import re

from pydantic import BaseModel, EmailStr, field_validator


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def validate_password(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("비밀번호에 최소 하나의 영문자가 포함되어야 합니다.")
        if not re.search(r"\d", v):
            raise ValueError("비밀번호에 최소 하나의 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("비밀번호에 최소 하나의 특수문자가 포함되어야 합니다.")
        return v
