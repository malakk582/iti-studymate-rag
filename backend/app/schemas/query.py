from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    top_k: int | None = Field(default=None, ge=1, le=10)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value

class Source(BaseModel):
    source: str
    chunk_id: str
    page: int | None = None
    score: float
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
