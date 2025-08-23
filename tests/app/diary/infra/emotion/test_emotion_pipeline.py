import json
import time

import pytest

from shiori.app.diary.domain.constants import MODEL_NAME, EMOTION_LABELS
from shiori.app.diary.infra.emotion import EmotionModel, EmotionPipeline


@pytest.fixture
def emotion_model() -> EmotionModel:
    return EmotionModel(model_name=MODEL_NAME, device="cpu")


@pytest.fixture
def emotion_pipeline(emotion_model: EmotionModel) -> EmotionPipeline:
    return EmotionPipeline(model=emotion_model)


@pytest.mark.asyncio
async def test_analyze_day(
    emotion_model: EmotionModel, emotion_pipeline: EmotionPipeline
):
    # Given
    daily_texts = [
        "오늘 하루는 정말 즐거웠고, 기분이 좋았어.",
        "오랜만에 친구들과 웃고 떠들면서 스트레스를 풀었지.",
        "햇볕도 따뜻해서 산책하기 딱 좋은 날이었어.",
    ]

    pipeline = emotion_pipeline

    # When
    start = time.perf_counter()
    result = await pipeline.analyze_day(daily_texts)
    elapsed = time.perf_counter() - start
    # Then

    print(f"\n[analyze_day duration] {elapsed:.4f} seconds")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert isinstance(result, dict)
    assert "predicted" in result
    assert isinstance(result["predicted"], str)
    assert result["predicted"] in EMOTION_LABELS.values()

    assert "probabilities" in result
    assert isinstance(result["probabilities"], dict)

    total_prob = sum(result["probabilities"].values())
    assert abs(total_prob - 1.0) < 0.01

    for label, prob in result["probabilities"].items():
        assert isinstance(label, str)
        assert isinstance(prob, float)
        assert 0.0 <= prob <= 1.0


@pytest.mark.asyncio
async def test_analyze(
    emotion_model: EmotionModel, emotion_pipeline: EmotionPipeline
) -> None:
    # Given
    week_diary_texts: list[list[str]] = [
        [
            "오늘 아침에 눈을 떴는데 기분이 너무 좋았어.",
            "햇살이 따뜻하고 상쾌했거든.",
            "오랜만에 산책도 다녀왔어.",
        ],
        [
            "출근길에 지하철이 고장나서 너무 짜증났어.",
            "회사에서도 일이 꼬이고 실수도 많았어.",
            "하루종일 우울했어.",
        ],
        [
            "점심에 매운 떡볶이를 먹었는데 맛있었어.",
            "오후엔 팀원이랑 티타임도 즐겼지.",
            "오늘은 마음이 편안했어.",
        ],
        [
            "어젯밤에 악몽을 꿨어.",
            "꿈에서 귀신이 쫓아와서 너무 무서웠어.",
            "잠에서 깨고 한참을 덜덜 떨었지.",
        ],
        [
            "친구랑 오랜만에 전화통화를 했어.",
            "서로 고민도 나누고 위로도 받았지.",
            "기분이 한결 나아졌어.",
        ],
        [
            "집 근처에서 이상한 사람을 마주쳐서 찝찝했어.",
            "기분이 안 좋아서 일찍 들어왔어.",
            "뉴스도 불쾌한 것들만 가득했지.",
        ],
        [
            "오늘은 아무런 감정도 느끼기 어려운 하루였어.",
            "밥도 대충 먹고 그냥 누워만 있었어.",
            "그냥 무의미한 하루였지.",
        ],
    ]

    pipeline = emotion_pipeline

    # When
    start = time.perf_counter()
    results = await pipeline.analyze(week_diary_texts)
    elapsed = time.perf_counter() - start

    # Then

    print(f"\n[analyze (weekly) duration] {elapsed:.4f} seconds")

    assert isinstance(results, list)
    assert len(results) == 7

    for result in results:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        assert isinstance(result, dict)
        assert "predicted" in result
        assert isinstance(result["predicted"], str)
        assert "probabilities" in result
        assert isinstance(result["probabilities"], dict)

        total_prob = sum(result["probabilities"].values())
        assert abs(total_prob - 1.0) < 0.01

        for label, prob in result["probabilities"].items():
            assert isinstance(label, str)
            assert isinstance(prob, float)
            assert 0.0 <= prob <= 1.0
