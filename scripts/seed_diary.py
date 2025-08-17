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

    blocks.append(
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": title}],
        }
    )

    paragraph_templates = [
        "오늘은 기분이 {adj1} 하루였다.",
        "출근길에 {event} 일이 있었다.",
        "점심으로는 {food}를 먹었고, 생각보다 {adj2} 맛이었다.",
        "오후엔 {activity} 하며 시간을 보냈다.",
        "하루를 마무리하며 {emotion} 감정을 느꼈다.",
    ]
    options = {
        "adj1": ["좋은", "이상한", "답답한", "신나는", "무기력한"],
        "event": ["황당한", "행복한", "짜증나는", "뜻밖의", "감동적인"],
        "food": ["김치찌개", "햄버거", "연어덮밥", "샐러드", "짜장면"],
        "adj2": ["괜찮은", "별로인", "좋은", "맛없는", "인상적인"],
        "activity": ["산책을", "책을 읽기를", "일기를 쓰기를", "멍하니 보내기를"],
        "emotion": ["고마운", "쓸쓸한", "뿌듯한", "우울한", "기쁜"],
    }

    for _ in range(random.randint(2, 4)):
        sentence = random.choice(paragraph_templates).format(
            **{k: random.choice(v) for k, v in options.items()}
        )
        blocks.append(
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [{"type": "text", "text": sentence}],
            }
        )

    if random.random() < 0.5:
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

    if random.random() < 0.4:
        quote = random.choice(
            [
                "오늘은 나를 더 사랑하기로 했다.",
                "가끔은 쉬어가는 것도 중요하다.",
                "작은 성취도 나를 웃게 만든다.",
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

    if random.random() < 0.3:
        blocks.append({"type": "horizontalRule"})

    return {"type": "doc", "content": blocks}


async def seed(user_id: int, start: datetime, end: datetime) -> None:
    await init_mongo()

    if start > end:
        raise ValueError("start date must be <= end date")

    diary_service = DiaryService(
        diary_repo=DiaryRepositoryImpl(),
        diary_meta_repo=DiaryMetaRepositoryImpl(),
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
