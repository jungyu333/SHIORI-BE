from pydantic import BaseModel


class EmotionResult(BaseModel):
    predicted: str
    probabilities: dict[str, float]
