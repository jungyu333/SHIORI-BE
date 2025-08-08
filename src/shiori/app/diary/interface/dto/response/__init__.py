from pydantic import BaseModel, Field

from shiori.app.diary.infra.model import ProseMirror


class UpsertDiaryResponse(BaseModel):
    id: str = Field(..., description="Diary Id")


class GetDiaryResponse(BaseModel):
    content: ProseMirror = Field(..., description="Diary Content")
