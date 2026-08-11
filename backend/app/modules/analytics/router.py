from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import get_current_active_user
from app.modules.models.user import User
from app.modules.analytics import service, schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=schemas.OverviewResponse)
async def get_overview(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Dashboard overview: conversations, messages, customers, agents, revenue this month."""
    data = await service.get_overview(db, user.tenant_id)
    return data


@router.get("/conversations/daily", response_model=list[schemas.DailyCount])
async def get_daily_conversations(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Conversation count per day for the last 30 days."""
    data = await service.get_daily_conversations(db, user.tenant_id)
    return data


@router.get("/messages/daily", response_model=list[schemas.DailyCount])
async def get_daily_messages(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Message count per day for the last 30 days."""
    data = await service.get_daily_messages(db, user.tenant_id)
    return data


@router.get("/top-agents", response_model=list[schemas.TopAgent])
async def get_top_agents(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Top 5 agents by conversation count this month."""
    data = await service.get_top_agents(db, user.tenant_id)
    return data
