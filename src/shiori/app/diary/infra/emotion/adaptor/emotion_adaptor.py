from shiori.app.diary.domain.entity import DiaryVO


class EmotionAdaptor:

    @staticmethod
    def convert_diary(diary: DiaryVO) -> list[str]:
        return [block.content for block in diary.diary_blocks if block.content]

    def convert_week(self, diaries: list[DiaryVO]) -> tuple[list[list[str]], list[str]]:
        week_inputs = [self.convert_diary(d) for d in diaries]
        dates = [d.date for d in diaries]
        return week_inputs, dates
