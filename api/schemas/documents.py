from pydantic import BaseModel
from uuid import UUID


class DocumentCreateRequest(BaseModel):
    file_name: str
    file_url: str


class DocumentCreateResponse(BaseModel):
    id: UUID
    file_name: str
    file_url: str
