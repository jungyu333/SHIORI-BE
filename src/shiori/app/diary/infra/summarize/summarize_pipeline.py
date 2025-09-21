from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from shiori.app.core import get_settings
from shiori.app.diary.domain.entity import DiaryVO
from shiori.app.diary.domain.schema import EmotionResult

settings = get_settings()


class SummarizePipeline:

    def __init__(self, model: str = "gpt-4o-mini"):
        self._llm = ChatOpenAI(
            model=model,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7,
        )

        self._prompt = PromptTemplate(
            template="""
                    당신은 사용자의 지난 7일치 일기를 정리해주는 따뜻한 조력자입니다.

                    주어진 일기와 감정 태그를 바탕으로,
                    마치 친구에게 이야기를 들려주듯 부드럽고 자연스럽게 요약해 주세요.
                    
                    불필요한 인사말은 생략해주세요.

                    반드시 포함해야 할 요소:
                    1. 한 주 동안 있었던 주요 사건들을 편안하게 정리
                    2. 감정의 흐름을 공감하는 어조로 설명
                    3. 전체 요약 (500자 이내, 따뜻하고 진솔한 말투)

                    일기 데이터:
                    {week_diaries}
                    """,
            input_variables=["week_diaries"],
        )

    def _preprocess(self, *, diaries: list[DiaryVO], emotions: list[EmotionResult]):
        week_data = list()

        for diary, emo in zip(diaries, emotions):
            text: str = " ".join(
                block.content for block in diary.diary_blocks if block.content
            )
            week_data.append(
                {
                    "date": diary.date,
                    "text": text,
                    "emotion": emo.predicted,
                    "emotion_probs": emo.probabilities,
                }
            )

        return week_data

    def _format_for_prompt(self, week_data: list[dict[str, Any]]) -> str:

        formatted: list[str] = []

        for entry in week_data:
            probs = entry["emotion_probs"]

            probs_str = ", ".join(
                f"{emo}: {round(val * 100, 1)}%" for emo, val in probs.items()
            )

            formatted.append(
                f"날짜: {entry['date']}\n"
                f"내용: {entry['text']}\n"
                f"예상 감정: {entry['emotion']}\n"
                f"감정 분포: {probs_str}\n"
            )

        return "\n\n".join(formatted)

    async def run(self, diaries: list[DiaryVO], emotions: list[EmotionResult]) -> str:

        chain = self._prompt | self._llm
        week_data = self._preprocess(diaries=diaries, emotions=emotions)
        week_diaries_str = self._format_for_prompt(week_data)

        result = await chain.ainvoke({"week_diaries": week_diaries_str})
        return result.content
