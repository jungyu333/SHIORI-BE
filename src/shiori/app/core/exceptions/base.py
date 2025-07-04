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
