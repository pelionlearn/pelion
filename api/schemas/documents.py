from pydantic import BaseModel
from uuid import UUID


class DocumentCreateRequest(BaseModel):
    file_name: str
    file_url: str


class DocumentResponse(BaseModel):
    id: UUID
    file_name: str
    file_url: str
