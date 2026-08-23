from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ChatCreate(BaseModel):
    name: str


class ChatRead(BaseModel):
    id: UUID
    classroom_id: UUID
    user_id: UUID
    name: str


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageRead(BaseModel):
    id: UUID
    chat_id: UUID
    role: str
    content: str
    created_at: datetime
