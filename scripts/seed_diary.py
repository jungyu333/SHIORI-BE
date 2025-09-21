import argparse
import asyncio
import random
from datetime import datetime, timedelta

from shiori.app.core.database.mongo_session import init_mongo
from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.infra.model import ProseMirror
from shiori.app.diary.infra.repository import (
    DiaryRepositoryImpl,
    DiaryMetaRepositoryImpl,
    TagRepositoryImpl,
)


def yyyymmdd(date: datetime):
    return date.strftime("%Y%m%d")


def parse_yyyymmdd(s: str) -> datetime:
    try:
        return datetime.strptime(s, "%Y%m%d")
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{s}', expected YYYYMMDD"
        ) from e


def generate_random_prosemirror_doc(title: str, date_str: str) -> dict:
    blocks = []

    # 제목
    blocks.append(
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": title}],
        }
    )

    # 요일에 따른 주제 흐름 (일관성 유지)
    day_offset = int(date_str[-2:]) % 7
    weekly_flow = [
        "새로운 한 주가 시작되어 긴장과 설렘을 느꼈다.",
        "업무에 몰입하며 바쁜 하루를 보냈다.",
        "작은 피로가 쌓였지만 성취감도 있었다.",
        "팀과 협력하며 중요한 결정을 내렸다.",
        "주중의 마무리를 준비하며 차분한 하루였다.",
        "휴식을 취하며 여유로움을 만끽했다.",
        "한 주를 돌아보며 감사한 마음을 느꼈다.",
    ]
    blocks.append(
        {
            "type": "paragraph",
            "attrs": {"textAlign": "left"},
            "content": [{"type": "text", "text": weekly_flow[day_offset]}],
        }
    )

    # 추가적인 디테일 문장
    paragraph_templates = [
        "점심에는 {food}를 먹었는데 생각보다 {adj} 맛이었다.",
        "오후에는 {activity} 하며 시간을 보냈다.",
        "출근길에는 {event} 일이 있었고, 기분이 {feeling}.",
        "하루를 마무리하며 {emotion} 감정을 느꼈다.",
    ]
    options = {
        "food": ["김치찌개", "햄버거", "연어덮밥", "샐러드", "짜장면"],
        "adj": ["괜찮은", "별로인", "아주 좋은", "실망스러운", "인상적인"],
        "activity": ["산책", "책 읽기", "운동", "명상", "드라마 시청"],
        "event": ["뜻밖의", "즐거운", "짜증나는", "감동적인", "어색한"],
        "feeling": ["좋아졌다", "복잡해졌다", "설렜다", "우울해졌다", "담담했다"],
        "emotion": ["뿌듯한", "쓸쓸한", "기쁜", "우울한", "고마운"],
    }

    for template in paragraph_templates:
        sentence = template.format(**{k: random.choice(v) for k, v in options.items()})
        blocks.append(
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [{"type": "text", "text": sentence}],
            }
        )

    # 체크리스트 (할 일) — 일정 확률로 추가
    if random.random() < 0.6:
        items = random.sample(
            [
                "이메일 확인",
                "운동하기",
                "책 읽기",
                "할 일 정리",
                "명상",
                "저녁 준비",
                "정리 정돈",
            ],
            k=random.randint(2, 4),
        )
        blocks.append(
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": item}],
                            }
                        ],
                    }
                    for item in items
                ],
            }
        )

    # 명언/생각 — 일정 확률로 추가
    if random.random() < 0.4:
        quote = random.choice(
            [
                "오늘은 나를 더 사랑하기로 했다.",
                "가끔은 쉬어가는 것도 중요하다.",
                "작은 성취도 나를 웃게 만든다.",
                "매일은 또 다른 시작이다.",
            ]
        )
        blocks.append(
            {
                "type": "blockquote",
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": quote}]}
                ],
            }
        )

    return {"type": "doc", "content": blocks}


async def seed(user_id: int, start: datetime, end: datetime) -> None:
    await init_mongo()

    if start > end:
        raise ValueError("start date must be <= end date")

    diary_service = DiaryService(
        diary_repo=DiaryRepositoryImpl(),
        diary_meta_repo=DiaryMetaRepositoryImpl(),
        tag_repo=TagRepositoryImpl(),
    )

    d = start
    total = created_cnt = updated_cnt = 0
    while d <= end:
        date_str = yyyymmdd(d)
        title = f"{d.year}년 {d.month}월 {d.day}일 일지"

        content_dict = generate_random_prosemirror_doc(title, date_str)
        content = ProseMirror.model_validate(content_dict)

        diary_id, created = await diary_service.upsert_diary(
            user_id=user_id,
            date=date_str,
            content=content,
            title=title,
        )

        if created:
            created_cnt += 1
        else:
            updated_cnt += 1

        print(f"[{date_str}] {'created' if created else 'updated'}: {diary_id}")
        total += 1
        d += timedelta(days=1)

    print(
        f"\n✅ Seed finished for user_id={user_id} | range={yyyymmdd(start)}~{yyyymmdd(end)}"
        f"\n   total: {total}, created: {created_cnt}, updated: {updated_cnt}"
    )


def main():
    parser = argparse.ArgumentParser(description="Seed diary data into development DB.")
    parser.add_argument("--user-id", type=int, required=True, help="Target user id")
    parser.add_argument(
        "--start", type=parse_yyyymmdd, required=True, help="Start date (YYYYMMDD)"
    )
    parser.add_argument(
        "--end",
        type=parse_yyyymmdd,
        required=True,
        help="End date (YYYYMMDD, inclusive)",
    )
    args = parser.parse_args()

    asyncio.run(seed(user_id=args.user_id, start=args.start, end=args.end))


if __name__ == "__main__":
    main()
