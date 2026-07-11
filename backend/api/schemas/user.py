from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
