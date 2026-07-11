from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.classes import ClassCreate, ClassResponse

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(class_id: UUID):
    return repositories.classes.get(class_id)


@router.post("/", response_model=ClassResponse)
async def create_class(class_: ClassCreate):
    return repositories.classes.create(class_.name)


@router.delete("/{class_id}", response_model=ClassResponse)
async def delete_class(user_id: UUID):
    return repositories.classes.delete(user_id)
