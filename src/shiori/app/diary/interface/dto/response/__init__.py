from pydantic import BaseModel, Field


class UpsertDiaryResponse(BaseModel):
    id: str = Field(..., description="Diary Id")


class GetDiaryResponse(BaseModel):
    content: dict | None = Field(..., description="Diary Content")
