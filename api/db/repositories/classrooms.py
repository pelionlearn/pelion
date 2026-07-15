from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Classroom
from uuid import UUID
from exceptions import errors


async def create_classroom(db: AsyncSession, name: str):
    obj = Classroom(name=name)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_classroom(db: AsyncSession, id: UUID):
    obj = await db.get(Classroom, id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")
    db.delete(obj)
    await db.commit()
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

    await db.commit()
    await db.refresh(class_obj)

    return class_obj
