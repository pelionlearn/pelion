from pydantic import BaseModel
from uuid import UUID


class ClassCreate(BaseModel):
    name: str


class ClassResponse(BaseModel):
    id: UUID
    name: str
