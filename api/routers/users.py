from fastapi import APIRouter
from uuid import UUID
from db import repositories
from schemas.users import UserCreateResponse, UserCreateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserCreateResponse)
async def get_user(user_id: UUID):
    return repositories.users.get_user(user_id)


@router.post("/", response_model=UserCreateResponse)
async def create_user(user: UserCreateRequest):
    return repositories.users.create_user(user.name, user.email)


@router.delete("/{user_id}", response_model=UserCreateResponse)
async def delete_user(user_id: UUID):
    return repositories.users.delete_user(user_id)
