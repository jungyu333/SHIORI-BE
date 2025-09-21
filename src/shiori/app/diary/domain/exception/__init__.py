from shiori.app.core.exceptions import BaseCustomException


class NotValidDateFormat(BaseCustomException):
    def __init__(self, message: str = "잘못된 날짜 형식이에요.", data: None = None):
        super().__init__(code=422, message=message, data=data)


class NotValidTitle(BaseCustomException):
    def __init__(
        self,
        message: str = "일지 제목은 50자 이내로 작성 해 주세요.",
        data: None = None,
    ):
        super().__init__(code=400, message=message, data=data)


class NotValidDateRange(BaseCustomException):
    def __init__(
        self, message: str = "시작 날짜와 끝 날짜가 유효하지 않아요!", data: None = None
    ):
        super().__init__(code=400, message=message, data=data)


class SummarizeFailed(BaseCustomException):
    def __init__(
        self,
        message: str = "요약 처리에 실패했습니다. 잠시 후 다시 시도해주세요.",
        data: None = None,
    ):
        super().__init__(code=503, message=message, data=data)
