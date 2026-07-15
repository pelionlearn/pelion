from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.orm import Session
from db import repositories
from db.database import get_db
from schemas.users import UserCreateResponse

router = APIRouter(prefix="/classrooms/{classroom_id}/users", tags=["ClassMembers"])


@router.get("/", response_model=list[UserCreateResponse])
async def get_members(classroom_id: UUID, db: Session = Depends(get_db)):
    return repositories.classroom_members.get_classroom_members(db, classroom_id)


@router.post("/{user_id}", response_model=UserCreateResponse)
async def add_member(classroom_id, user_id, db: Session = Depends(get_db)):
    repositories.classroom_members.add_classroom_member(db, classroom_id, user_id)
    return repositories.users.get_user(db, user_id)


@router.delete("/{user_id}", response_model=UserCreateResponse)
async def delete_user(classroom_id, user_id: UUID, db: Session = Depends(get_db)):
    return repositories.classroom_members.remove_classroom_member(
        db, classroom_id, user_id
    )
