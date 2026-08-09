from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Classroom, ClassroomMember
from uuid import UUID
from exceptions import errors


async def get_classroom_members(db: AsyncSession, classroom_id: UUID):
    class_obj = await db.get(Classroom, classroom_id)
    if class_obj is None:
        raise errors.NotFoundError(f"Classroom {classroom_id} found")
    return class_obj.members


async def add_classroom_member(db: AsyncSession, classroom_id: UUID, user_id: UUID):
    class_member = ClassroomMember(classroom_id=classroom_id, user_id=user_id)
    db.add(class_member)
    await db.commit()
    await db.refresh(class_member)
    return class_member


async def remove_classroom_member(db: AsyncSession, classroom_id: UUID, user_id: UUID):
    class_member = await db.get(ClassroomMember, (classroom_id, user_id))
    if class_member is None:
        raise errors.NotFoundError(
            f"User {user_id} not found in classroom {classroom_id}"
        )
    await db.delete(class_member)
