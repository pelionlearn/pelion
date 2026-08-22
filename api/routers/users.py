from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from db import repositories
from db.database import get_db
from db.models import User
from schemas.users import UserRead, UserUpdate
from schemas.classrooms import ClassroomResponse
from auth.authentication import current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(
    user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db)
):
    return await repositories.users.get_user(db, user.id)


@router.patch("/me", response_model=UserRead)
async def patch_me(
    userUpdate: UserUpdate,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    if userUpdate.name:
        return await repositories.users.rename_user(db, user.id, userUpdate.name)


# TODO: add this endpoint to tests
@router.get("/me/classrooms", response_model=list[ClassroomResponse])
async def get_user_classrooms(
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.users.get_user_classes(db, user.id)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    _: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.users.get_user(db, user_id)
