from pydantic import BaseModel
from uuid import UUID


class ClassroomCreateRequest(BaseModel):
    name: str


class ClassroomResponse(BaseModel):
    id: UUID
    name: str
