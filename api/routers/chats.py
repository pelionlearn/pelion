from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from auth.authorization import require_chat_member, require_classroom_member
from auth.authentication import current_active_user
from db import repositories
from db.database import get_db
from db.models import User
from schemas.chats import ChatCreate, ChatMessageCreate, ChatMessageRead, ChatRead
from services.llm import get_llm_response

router = APIRouter(prefix="/classrooms/{classroom_id}/chats", tags=["Chats"])


@router.post("/", response_model=ChatRead)
async def create_chat(
    chat: ChatCreate,
    classroom_id: UUID,
    user: User = Depends(current_active_user),
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.chats.create_chat(db, classroom_id, user.id, chat.name)


@router.get("/", response_model=list[ChatRead])
async def get_chats(
    classroom_id: UUID,
    user: User = Depends(current_active_user),
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.chats.get_chats(db, classroom_id, user.id)


@router.get("/{chat_id}", response_model=ChatRead)
async def get_chat(
    classroom_id: UUID,
    chat_id: UUID,
    _classroom_member: None = Depends(require_classroom_member),
    _chat_member: None = Depends(require_chat_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.chats.get_chat(db, chat_id)


@router.get("/{chat_id}/messages", response_model=list[ChatMessageRead])
async def get_messages(
    classroom_id: UUID,
    chat_id: UUID,
    _classroom_member: None = Depends(require_classroom_member),
    _chat_member: None = Depends(require_chat_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.chats.get_messages(db, chat_id)


@router.post("/{chat_id}/messages", response_model=ChatMessageRead)
async def post_message(
    message: ChatMessageCreate,
    classroom_id: UUID,
    chat_id: UUID,
    _classroom_member: None = Depends(require_classroom_member),
    _chat_member: None = Depends(require_chat_member),
    db: AsyncSession = Depends(get_db),
):
    prev_messages = await repositories.chats.get_all_messages(db, chat_id)
    prev_messages = [
        {"content": message.content, "role": message.role} for message in prev_messages
    ]

    rag_content, usr_content, llm_content = await get_llm_response(
        prev_messages, message.content, classroom_id
    )

    rag_msg = await repositories.chats.create_message(db, chat_id, "rag", rag_content)
    usr_msg = await repositories.chats.create_message(db, chat_id, "user", usr_content)
    llm_msg = await repositories.chats.create_message(
        db, chat_id, "assistant", llm_content
    )

    return llm_msg
