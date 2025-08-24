import pytest

from shiori.app.diary.domain.constants import MODEL_NAME
from shiori.app.diary.domain.schema import EmotionResult
from shiori.app.diary.infra.emotion import EmotionModel


@pytest.fixture
def emotion_model() -> EmotionModel:
    return EmotionModel(model_name=MODEL_NAME, device="cpu")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "오늘 하루가 너무 힘들고 우울했어요.",
        "기쁘고 행복한 하루였습니다!",
        "꿈에서 처녀귀신이 칼 들고 쫓아와서 너무 무서웠어",
    ],
)
async def test_predict(emotion_model: EmotionModel, text):
    # Given

    model = emotion_model

    # When

    result = await model.predict(text=text)

    # Then

    assert isinstance(result, EmotionResult)

    assert isinstance(result.predicted, str)
    assert isinstance(result.probabilities, dict)

    total_prob = sum(result.probabilities.values())
    assert abs(total_prob - 1.0) < 0.01

    for label, score in result.probabilities.items():
        assert isinstance(label, str)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
