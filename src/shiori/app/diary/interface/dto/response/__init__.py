from pydantic import BaseModel, Field


class UpsertDiaryResponse(BaseModel):
    id: str = Field(..., description="Diary Id")
