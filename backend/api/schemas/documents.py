from pydantic import BaseModel
from uuid import UUID


class DocumentCreate(BaseModel):
    file_name: str
    file_url: str


class DocumentResponse(BaseModel):
    id: str
    file_name: str
    file_url: str
