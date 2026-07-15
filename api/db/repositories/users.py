from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from exceptions import errors

# MOST USER METHODS ARE UNNECESSARY BECAUSE OF FASTAPI USERS


async def get_user(db: AsyncSession, id):
    user = await db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    return user


async def get_all_users(db: AsyncSession):
    return await db.query(User).all()


async def get_user_classes(db: AsyncSession, id):
    user = await db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    return user.classrooms
