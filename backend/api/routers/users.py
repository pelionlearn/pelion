from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.users import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    return repositories.users.get_user(user_id)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return repositories.users.create_user(user.name, user.email)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: UUID):
    return repositories.users.delete_user(user_id)
