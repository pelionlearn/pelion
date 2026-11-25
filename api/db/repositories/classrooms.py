from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Classroom
from uuid import UUID
from db.repositories.classroom_members import add_classroom_member
from exceptions import errors


async def create_classroom(db: AsyncSession, name: str, color: str, user_id: UUID):
    class_obj = Classroom(name=name, color=color, owner=user_id)
    db.add(class_obj)

    await db.flush()
    await db.refresh(class_obj)

    return class_obj


async def delete_classroom(db: AsyncSession, id: UUID):
    obj = await db.get(Classroom, id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")
    await db.delete(obj)
    await db.flush()
    return obj


async def get_classroom(db: AsyncSession, id: UUID):
    obj = await db.get(Classroom, id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")
    return obj


async def rename_classroom(db: AsyncSession, id: UUID, name: str):
    class_obj = await db.get(Classroom, id)

    if class_obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")

    class_obj.name = name

    return class_obj

async def set_classroom_owner(db: AsyncSession, classroom_id: UUID, user_id: UUID):
    obj = await db.get(Classroom, classroom_id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")

    obj.owner = user_id

    await db.flush()

    return obj

async def is_classroom_owner(db: AsyncSession, classroom_id: UUID, user_id: UUID):
    obj = await db.get(Classroom, classroom_id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")

    return obj.owner == user_id