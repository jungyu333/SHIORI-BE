from datetime import datetime

from shiori.app.diary.domain.exception import (
    NotValidDateFormat,
    NotValidTitle,
    NotValidDateRange,
)


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

    @staticmethod
    def validate_date_range(*, start: str, end: str) -> None:
        start_date = datetime.strptime(start, "%Y%m%d").date()
        end_date = datetime.strptime(end, "%Y%m%d").date()

        if start_date > end_date:
            raise NotValidDateRange
