from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models import User
from exceptions import errors


async def get_user(db: AsyncSession, id):
    user = await db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    return user


async def delete_user(db: AsyncSession, id):
    user = db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    await db.delete(user)
    await db.commit()
    return user


async def rename_user(db: AsyncSession, id, name: str):
    user = await db.get(User, id)

    if user is None:
        raise errors.NotFoundError(f"User {id} not found")

    user.name = name

    await db.commit()
    await db.refresh(user)

    return user


async def get_user_classes(db: AsyncSession, id):
    stmt = select(User).where(User.id == id).options(selectinload(User.classrooms))
    user = (await db.scalars(stmt)).one_or_none()

    if user is None:
        return []

    return user.classrooms
