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


class SummarizeDiaryRequest(BaseModel):
    start: str = Field(..., examples=["20250810"])
    end: str = Field(..., examples=["20250816"])
