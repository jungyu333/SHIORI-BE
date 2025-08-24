from asyncio import gather
from collections import Counter

from shiori.app.diary.domain.constants import EMOTION_LABELS
from shiori.app.diary.domain.schema import EmotionResult
from shiori.app.diary.infra.emotion import EmotionModel


class EmotionPipeline:
    def __init__(self, model: EmotionModel):
        self._model = model

    async def analyze_day(self, daily_texts: list[str]) -> EmotionResult:

        results: list[EmotionResult] = await gather(
            *[self._model.predict(text=t) for t in daily_texts]
        )

        predicted_labels = [result.predicted for result in results]
        most_common = Counter(predicted_labels).most_common(1)[0][0]

        summed = {label: 0.0 for label in EMOTION_LABELS.values()}
        for result in results:
            for label, prob in result.probabilities.items():
                summed[label] += prob
        averaged = {
            label: round(total / len(results), 4) for label, total in summed.items()
        }

        return EmotionResult(
            predicted=most_common,
            probabilities=averaged,
        )

    async def analyze(self, week_diary_texts: list[list[str]]) -> list[EmotionResult]:
        tasks = [self.analyze_day(daily_texts) for daily_texts in week_diary_texts]
        results = await gather(*tasks)
        return results
