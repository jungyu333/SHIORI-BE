import jwt
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from shiori.app.core import get_settings
from shiori.app.core.helpers import redis_client

config = get_settings()


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    is_admin: bool = Field(False, description="Is admin")


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )

            jti = payload.get("jti")

            if jti:
                is_blacklisted = await redis_client.get(f"blacklist:{jti}")
                if is_blacklisted:
                    return False, current_user

            user_id = payload.get("user_id")
            is_admin = payload.get("is_admin")

        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.id = user_id
        current_user.is_admin = is_admin
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
