from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.users import UserResponse

router = APIRouter(prefix="/classes/{class_id}/users", tags=["ClassMembers"])


@router.get("/", response_model=list[UserResponse])
async def get_members(class_id: UUID):
    return repositories.classroom_members.get_classroom_members(class_id)


@router.post("/{user_id}", response_model=UserResponse)
async def add_member(class_id, user_id):
    repositories.classroom_members.add_classroom_member(class_id, user_id)
    return repositories.users.get_user(user_id)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(class_id, user_id: UUID):
    return repositories.classroom_members.remove_classroom_member(class_id, user_id)
