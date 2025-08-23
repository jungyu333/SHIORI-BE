from asyncio import gather
from collections import Counter

from shiori.app.diary.domain.constants import EMOTION_LABELS
from shiori.app.diary.infra.emotion import EmotionModel


class EmotionPipeline:
    def __init__(self, model: EmotionModel):
        self._model = model

    async def analyze_day(
        self, daily_texts: list[str]
    ) -> dict[str, str | dict[str, float]]:

        results = await gather(*[self._model.predict(text=t) for t in daily_texts])

        predicted_labels = [r["predicted"] for r in results]
        most_common = Counter(predicted_labels).most_common(1)[0][0]

        summed = {label: 0.0 for label in EMOTION_LABELS.values()}
        for r in results:
            for label, prob in r["probabilities"].items():
                summed[label] += prob
        averaged = {
            label: round(total / len(results), 4) for label, total in summed.items()
        }

        return {
            "predicted": most_common,
            "probabilities": averaged,
        }

    async def analyze(
        self, week_diary_texts: list[list[str]]
    ) -> list[dict[str, str | dict[str, float]]]:
        tasks = [self.analyze_day(daily_texts) for daily_texts in week_diary_texts]
        results = await gather(*tasks)
        return results
