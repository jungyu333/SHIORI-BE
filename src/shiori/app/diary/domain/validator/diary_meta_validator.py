from datetime import datetime

from shiori.app.diary.domain.exception import NotValidDateFormat, NotValidTitle


class DiaryMetaValidator:

    @staticmethod
    def validate_date_format(date: str) -> None:
        try:
            datetime.strptime(date, "%Y%m%d")
        except ValueError:
            raise NotValidDateFormat

    @staticmethod
    def validate_title(title: str) -> None:
        if len(title) > 50:
            raise NotValidTitle
