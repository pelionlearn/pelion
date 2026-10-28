from pydantic import BaseModel, Field
from uuid import UUID


class ClassroomCreateRequest(BaseModel):
    name: str
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$", default="#FFFFFF")


class ClassroomResponse(BaseModel):
    id: UUID
    name: str
    color: str
