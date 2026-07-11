from pydantic import BaseModel
from uuid import UUID
from api.schemas.user import UserResponse


class ClassCreate(BaseModel):
    file_name: str
    file_url: str


class ClassResponse(BaseModel):
    id: UUID
    file_name: str
    file_url: str
