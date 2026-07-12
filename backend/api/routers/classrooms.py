from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.classrooms import ClassroomCreateRequest, ClassroomCreateResponse

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/{class_id}", response_model=ClassroomCreateResponse)
async def get_classroom(class_id: UUID):
    return repositories.classrooms.get_classroom(class_id)


@router.post("/", response_model=ClassroomCreateResponse)
async def create_classroom(class_: ClassroomCreateRequest):
    return repositories.classrooms.create_classroom(class_.name)


@router.delete("/{class_id}", response_model=ClassroomCreateResponse)
async def delete_classroom(user_id: UUID):
    return repositories.classrooms.delete_classroom(user_id)
