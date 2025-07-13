from abc import ABC, abstractmethod
from typing import Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from shiori.app.core.exceptions import BaseCustomException, UnauthorizedException


class BasePermission(ABC):
    exception = BaseCustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsNotAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.is_admin is not None


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: list[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()

            if not await cls.has_permission(request=request):
                raise cls.exception
