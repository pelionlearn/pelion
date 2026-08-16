from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from exceptions import errors

# MOST USER METHODS ARE UNNECESSARY BECAUSE OF FASTAPI USERS


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
