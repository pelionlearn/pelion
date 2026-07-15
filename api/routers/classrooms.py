from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.orm import Session
from db import repositories
from db.database import get_db
from schemas.classrooms import ClassroomCreateRequest, ClassroomCreateResponse

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


@router.get("/{classroom_id}", response_model=ClassroomCreateResponse)
async def get_classroom(classroom_id: UUID, db: Session = Depends(get_db)):
    return repositories.classrooms.get_classroom(db, classroom_id)


@router.post("/", response_model=ClassroomCreateResponse)
async def create_classroom(
    class_: ClassroomCreateRequest, db: Session = Depends(get_db)
):
    return repositories.classrooms.create_classroom(db, class_.name)


@router.delete("/{classroom_id}", response_model=ClassroomCreateResponse)
async def delete_classroom(user_id: UUID, db: Session = Depends(get_db)):
    return repositories.classrooms.delete_classroom(db, user_id)
