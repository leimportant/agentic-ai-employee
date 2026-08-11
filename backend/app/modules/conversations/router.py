from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import get_current_active_user, require_module
from app.modules.models.user import User
from app.modules.conversations import service, schemas
from app.middleware.usage_gate import usage_gate

router = APIRouter(prefix="/conversations", tags=["conversations"], dependencies=[Depends(require_module("ai-cs"))])


@router.get("", response_model=list[schemas.ConversationOut])
async def list_conversations(
    agent_id: Optional[UUID] = None,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_conversations(db, user.tenant_id, agent_id)


@router.get("/{convo_id}", response_model=schemas.ConversationDetail)
async def get_conversation(convo_id: UUID, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.get_conversation(db, user.tenant_id, convo_id)


@router.post("", response_model=schemas.ConversationOut, status_code=201)
async def start_conversation(data: schemas.StartConversationRequest, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.start_conversation(db, user.tenant_id, data)


@router.post("/{convo_id}/send", dependencies=[Depends(usage_gate)])
async def send_message(convo_id: UUID, data: schemas.SendMessageRequest, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.send_message(db, user.tenant_id, convo_id, data.content)
