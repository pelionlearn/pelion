from fastapi import APIRouter
from uuid import UUID
from db import repositories
from schemas.users import UserCreateResponse

router = APIRouter(prefix="/classrooms/{classroom_id}/users", tags=["ClassMembers"])


@router.get("/", response_model=list[UserCreateResponse])
async def get_members(classroom_id: UUID):
    return repositories.classroom_members.get_classroom_members(classroom_id)


@router.post("/{user_id}", response_model=UserCreateResponse)
async def add_member(classroom_id, user_id):
    repositories.classroom_members.add_classroom_member(classroom_id, user_id)
    return repositories.users.get_user(user_id)


@router.delete("/{user_id}", response_model=UserCreateResponse)
async def delete_user(classroom_id, user_id: UUID):
    return repositories.classroom_members.remove_classroom_member(classroom_id, user_id)
