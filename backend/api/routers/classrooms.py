from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.classrooms import ClassroomCreateRequest, ClassroomCreateResponse

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


@router.get("/{classroom_id}", response_model=ClassroomCreateResponse)
async def get_classroom(classroom_id: UUID):
    return repositories.classrooms.get_classroom(classroom_id)


@router.post("/", response_model=ClassroomCreateResponse)
async def create_classroom(class_: ClassroomCreateRequest):
    return repositories.classrooms.create_classroom(class_.name)


@router.delete("/{classroom_id}", response_model=ClassroomCreateResponse)
async def delete_classroom(user_id: UUID):
    return repositories.classrooms.delete_classroom(user_id)
