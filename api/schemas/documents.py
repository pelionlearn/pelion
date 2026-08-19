from pydantic import BaseModel
from uuid import UUID


class DocumentCreateRequest(BaseModel):
    file_name: str
    file_url: str


class DocumentResponse(BaseModel):
    id: UUID
    content_type: str | None
    size: int
    file_name: str
    file_url: str | None
