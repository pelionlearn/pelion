from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import repositories
from db.database import get_db
from db.models import Chat, User
from auth.authentication import current_active_user
from exceptions import errors


async def require_classroom_member(
    classroom_id: UUID,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    if not await repositories.classroom_members.is_classroom_member(
        db, classroom_id, current_user.id
    ):
        raise errors.NotFoundError("Classroom not found")


async def require_document_in_class(
    classroom_id: UUID,
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    document = await repositories.documents.get_document(db, document_id, classroom_id)

    if document.classroom_id != classroom_id:
        raise errors.NotFoundError("Document not found")

    return document


async def require_chat_member(
    chat_id: UUID,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user.id)

    chat = await db.scalars(stmt)

    if chat is None:
        raise errors.NotFoundError("Chat not found")
