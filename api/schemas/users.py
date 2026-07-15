from pydantic import BaseModel
from uuid import UUID
from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = None
