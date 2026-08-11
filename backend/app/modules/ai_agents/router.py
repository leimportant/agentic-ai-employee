from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import get_current_active_user, require_module
from app.modules.models.user import User
from app.modules.ai_agents import service, schemas
from app.middleware.usage_gate import usage_gate

router = APIRouter(prefix="/ai-agents", tags=["ai-agents"], dependencies=[Depends(require_module("ai-cs"))])


@router.get("", response_model=list[schemas.AgentOut])
async def list_agents(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.list_agents(db, user.tenant_id)


@router.get("/{agent_id}", response_model=schemas.AgentOut)
async def get_agent(agent_id: UUID, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.get_agent(db, user.tenant_id, agent_id)


@router.post("", response_model=schemas.AgentOut, status_code=201, dependencies=[Depends(usage_gate)])
async def create_agent(data: schemas.AgentCreate, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.create_agent(db, user.tenant_id, data)


@router.put("/{agent_id}", response_model=schemas.AgentOut)
async def update_agent(agent_id: UUID, data: schemas.AgentUpdate, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.update_agent(db, user.tenant_id, agent_id, data)


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: UUID, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    await service.delete_agent(db, user.tenant_id, agent_id)
