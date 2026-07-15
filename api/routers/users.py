from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.orm import Session
from db import repositories
from db.database import get_db
from schemas.users import UserCreateResponse, UserCreateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserCreateResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return repositories.users.get_user(db, user_id)


@router.post("/", response_model=UserCreateResponse)
async def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    return repositories.users.create_user(db, user.name, user.email)


@router.delete("/{user_id}", response_model=UserCreateResponse)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return repositories.users.delete_user(db, user_id)
