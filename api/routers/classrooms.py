from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from auth.authorization import require_classroom_member
from auth.authentication import current_active_user
from db import repositories
from db.database import get_db
from db.models import User
from schemas.classrooms import ClassroomCreateRequest, ClassroomResponse

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


@router.get("/{classroom_id}", response_model=ClassroomResponse)
async def get_classroom(
    classroom_id: UUID,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.classrooms.get_classroom(db, classroom_id)


@router.post("/", response_model=ClassroomResponse)
async def create_classroom(
    class_: ClassroomCreateRequest,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.classrooms.create_classroom(db, class_.name, user.id)


@router.delete("/{classroom_id}", response_model=ClassroomResponse)
async def delete_classroom(
    classroom_id: UUID,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.classrooms.delete_classroom(db, classroom_id)
