import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Chat, ChatMessage
from uuid import UUID
from exceptions import errors


async def get_messages(db: AsyncSession, chat_id: UUID):
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(50)
    )

    result = await db.execute(stmt)

    return result.scalars().all()


async def get_all_messages(db: AsyncSession, chat_id: UUID):
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.asc())
    )

    result = await db.execute(stmt)

    return result.scalars().all()


async def create_chat(db: AsyncSession, classroom_id: UUID, user_id: UUID, name: str):
    obj = Chat(name=name, classroom_id=classroom_id, user_id=user_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


async def get_chats(db: AsyncSession, classroom_id, user_id):
    stmt = select(Chat).where(
        Chat.classroom_id == classroom_id, Chat.user_id == user_id
    )

    return (await db.scalars(stmt)).all()


async def get_chat(db: AsyncSession, chat_id):
    chat = await db.get(Chat, chat_id)

    return chat


async def create_message(db: AsyncSession, chat_id: UUID, role: str, content: str):
    message = ChatMessage(
        chat_id=chat_id,
        role=role,
        content=content,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message
