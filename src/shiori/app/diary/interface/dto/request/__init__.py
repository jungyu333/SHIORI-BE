from typing import Optional

from pydantic import BaseModel, Field

from shiori.app.diary.infra.model import ProseMirror


class UpsertDiaryRequest(BaseModel):
    content: ProseMirror = Field(
        ...,
        examples=[
            {
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "attrs": {"textAlign": "left"},
                        "content": [
                            {
                                "type": "text",
                                "text": "hello",
                                "marks": [{"type": "bold"}],
                            }
                        ],
                    }
                ],
            }
        ],
    )
    title: Optional[str] = Field(..., examples=["오늘의 일지"])
