from shiori.app.core.exceptions import BaseCustomException


class UserNotFoundException(BaseCustomException):
    def __init__(self, message: str = "존재 하지 않는 계정 입니다", data: None = None):
        super().__init__(code=404, message=message, data=data)


class AuthenticationException(BaseCustomException):
    def __init__(self, message: str = "비밀번호가 일치 하지 않습니다", data=None):
        super().__init__(code=401, message=message, data=data)
