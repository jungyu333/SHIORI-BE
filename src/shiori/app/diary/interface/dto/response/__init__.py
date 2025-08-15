from pydantic import BaseModel, Field


class UpsertDiaryResponse(BaseModel):
    id: str = Field(..., description="Diary Id")


class GetDiaryResponse(BaseModel):
    content: dict | None = Field(..., description="Diary Content")


class WeekDiaryMeta(BaseModel):
    date: str
    title: str
    summary_status: str
    is_archived: bool
    updated_at: str
