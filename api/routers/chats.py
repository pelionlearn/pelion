from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from auth.authorization import require_chat_member, require_classroom_member
from auth.authentication import current_active_user
from db import repositories
from db.database import get_db
from db.models import User
from schemas.chats import ChatCreate, ChatMessageCreate, ChatMessageRead, ChatRead

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


@router.get("/{chat_id}", response_model=list[ChatMessageRead])
async def get_messages(
    classroom_id: UUID,
    chat_id: UUID,
    _classroom_member: None = Depends(require_classroom_member),
    _chat_member: None = Depends(require_chat_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.chats.get_messages(db, chat_id)


@router.post("/{chat_id}", response_model=ChatMessageRead)
async def post_message(
    message: ChatMessageCreate,
    classroom_id: UUID,
    chat_id: UUID,
    _classroom_member: None = Depends(require_classroom_member),
    _chat_member: None = Depends(require_chat_member),
    db: AsyncSession = Depends(get_db),
):
    # create user message in db
    user_msg = await repositories.chats.create_message(
        db, chat_id, "user", message.content
    )

    # TODO: call to llm for a response
    # add role="ai" or smth
    # save response to db
    # return llm message instead of user's message

    return user_msg
