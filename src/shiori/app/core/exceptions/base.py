class BaseCustomException(Exception):
    def __init__(self, code: int = 400, message: str = "", data=None):
        if data is None:
            data = {}

        self.code = code
        self.message = message
        self.data = data


class NotFoundException(BaseCustomException):
    def __init__(self, message: str = "Not Found", data: None = None):
        super().__init__(code=404, message=message, data=data)


class ForbiddenException(BaseCustomException):
    def __init__(self, message: str = "Forbidden", data: None = None):
        super().__init__(code=401, message=message, data=data)


class ServerErrorException(BaseCustomException):
    def __init__(self, message: str = "Internal Server Error", data: None = None):
        super().__init__(code=500, message=message, data=data)


class ValidationException(BaseCustomException):
    def __init__(self, message: str = "요청값이 올바르지 않습니다", data=None):
        super().__init__(code=422, message=message, data=data)


class DecodeTokenException(BaseCustomException):
    def __init__(self, message: str = "TOKEN__DECODE_ERROR", data=None):
        super().__init__(code=400, message=message, data=data)


class ExpiredTokenException(BaseCustomException):
    def __init__(self, message: str = "TOKEN__EXPIRE_TOKEN", data=None):
        super().__init__(code=401, message=message, data=data)
