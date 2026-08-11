from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class KBCreateRequest(BaseModel):
    name: str
    ai_agent_id: UUID


class KBUpdateRequest(BaseModel):
    name: Optional[str] = None


class KBOut(BaseModel):
    id: UUID
    tenant_id: UUID
    ai_agent_id: UUID
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KBDocumentCreateRequest(BaseModel):
    title: str
    content: str


class KBDocumentOut(BaseModel):
    id: UUID
    knowledge_base_id: UUID
    title: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
