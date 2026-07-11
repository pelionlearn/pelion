from pydantic import BaseModel
from uuid import UUID


class UserCreateRequest(BaseModel):
    name: str
    email: str


class UserCreateResponse(BaseModel):
    id: UUID
    name: str
    email: str
