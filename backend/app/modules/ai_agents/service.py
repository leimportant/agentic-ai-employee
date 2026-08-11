from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.models.ai_agent import AiAgent
from app.modules.ai_agents.schemas import AgentCreate, AgentUpdate


async def list_agents(db: AsyncSession, tenant_id: UUID):
    result = await db.execute(
        select(AiAgent).where(AiAgent.tenant_id == tenant_id).order_by(AiAgent.created_at.desc())
    )
    return result.scalars().all()


async def get_agent(db: AsyncSession, tenant_id: UUID, agent_id: UUID):
    agent = await db.get(AiAgent, agent_id)
    if not agent or agent.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


async def create_agent(db: AsyncSession, tenant_id: UUID, data: AgentCreate):
    agent = AiAgent(
        id=uuid4(),
        tenant_id=tenant_id,
        name=data.name,
        type=data.type,
        system_prompt=data.system_prompt,
        config=data.config or {},
        is_active=data.is_active,
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


async def update_agent(db: AsyncSession, tenant_id: UUID, agent_id: UUID, data: AgentUpdate):
    agent = await get_agent(db, tenant_id, agent_id)
    for key, val in data.model_dump(exclude_none=True).items():
        setattr(agent, key, val)
    await db.commit()
    await db.refresh(agent)
    return agent


async def delete_agent(db: AsyncSession, tenant_id: UUID, agent_id: UUID):
    agent = await get_agent(db, tenant_id, agent_id)
    await db.delete(agent)
    await db.commit()
