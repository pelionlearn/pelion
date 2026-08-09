from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from db import repositories
from db.database import get_db
from schemas.users import UserRead

router = APIRouter(prefix="/classrooms/{classroom_id}/users", tags=["ClassMembers"])


@router.get("/", response_model=list[UserRead])
async def get_members(classroom_id: UUID, db: AsyncSession = Depends(get_db)):
    return await repositories.classroom_members.get_classroom_members(db, classroom_id)


@router.post("/{user_id}", response_model=UserRead)
async def add_member(classroom_id, user_id, db: AsyncSession = Depends(get_db)):
    await repositories.classroom_members.add_classroom_member(db, classroom_id, user_id)
    return await repositories.users.get_user(db, user_id)


@router.delete("/{user_id}")
async def delete_user(classroom_id, user_id: UUID, db: AsyncSession = Depends(get_db)):
    await repositories.classroom_members.remove_classroom_member(
        db, classroom_id, user_id
    )
