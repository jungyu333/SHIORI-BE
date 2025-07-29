from shiori.app.core.exceptions import BaseCustomException


class NotValidDateFormat(BaseCustomException):
    def __init__(self, message: str = "잘못된 날짜 형식 입니다.", data: None = None):
        super().__init__(code=400, message=message, data=data)


class NotValidTitle(BaseCustomException):
    def __init__(
        self,
        message: str = "일지 제목은 50자 이내로 작성 해 주세요.",
        data: None = None,
    ):
        super().__init__(code=400, message=message, data=data)
