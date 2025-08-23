from shiori.app.diary.domain.entity import DiaryVO


class EmotionAdaptor:

    @staticmethod
    def convert_diary(diary: DiaryVO) -> list[str]:
        return [block.content for block in diary.diary_blocks if block.content]

    def convert_week(self, diaries: list[DiaryVO]) -> list[list[str]]:

        return [self.convert_diary(diary) for diary in diaries]
