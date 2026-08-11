from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class MessageOut(BaseModel):
    id: UUID
    role: str  # "user" | "assistant" | "system"
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    id: UUID
    ai_agent_id: UUID
    customer_id: UUID
    channel: str
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConversationDetail(ConversationOut):
    messages: list[MessageOut] = []


class SendMessageRequest(BaseModel):
    content: str


class StartConversationRequest(BaseModel):
    ai_agent_id: UUID
    customer_id: UUID
    channel: str = "web"
