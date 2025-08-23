from shiori.app.diary.infra.emotion import EmotionModel


class EmotionPipeline:
    def __init__(self, model: EmotionModel):
        self._model = model

    async def analyze(self, texts: list[str]) -> list[dict[str, str]]:
        results = []
        for text in texts:
            result = await self._model.predict(text=text)
            results.append(result)
        return results
