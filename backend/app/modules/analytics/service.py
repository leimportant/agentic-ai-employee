from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, func, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models.conversation import Conversation
from app.modules.models.message import Message
from app.modules.models.customer import Customer
from app.modules.models.invoice import Invoice
from app.modules.models.ai_agent import AiAgent


def _start_of_month() -> datetime:
    """Return the first day of the current month at midnight."""
    now = datetime.utcnow()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _thirty_days_ago() -> datetime:
    """Return datetime 30 days ago."""
    return datetime.utcnow() - timedelta(days=30)


async def get_overview(db: AsyncSession, tenant_id: UUID) -> dict:
    """Get dashboard overview stats for the current month."""
    month_start = _start_of_month()

    # Total conversations this month
    result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.tenant_id == tenant_id,
            Conversation.created_at >= month_start,
        )
    )
    total_conversations = result.scalar() or 0

    # Total messages this month (join through Conversation for tenant filtering)
    result = await db.execute(
        select(func.count(Message.id))
        .join(Conversation, Message.conversation_id == Conversation.id)
        .where(
            Conversation.tenant_id == tenant_id,
            Message.created_at >= month_start,
        )
    )
    total_messages = result.scalar() or 0

    # Total customers
    result = await db.execute(
        select(func.count(Customer.id)).where(
            Customer.tenant_id == tenant_id,
        )
    )
    total_customers = result.scalar() or 0

    # Active agents
    result = await db.execute(
        select(func.count(AiAgent.id)).where(
            AiAgent.tenant_id == tenant_id,
            AiAgent.is_active == True,  # noqa: E712
        )
    )
    active_agents = result.scalar() or 0

    # Revenue this month (sum of paid invoices, amount is String so cast to Numeric)
    result = await db.execute(
        select(func.coalesce(func.sum(cast(Invoice.amount, Numeric)), 0)).where(
            Invoice.tenant_id == tenant_id,
            Invoice.status == "paid",
            Invoice.paid_at >= month_start,
        )
    )
    revenue_this_month = float(result.scalar() or 0)

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_customers": total_customers,
        "active_agents": active_agents,
        "revenue_this_month": revenue_this_month,
    }


async def get_daily_conversations(db: AsyncSession, tenant_id: UUID) -> list[dict]:
    """Get conversation count per day for the last 30 days."""
    since = _thirty_days_ago()

    result = await db.execute(
        select(
            func.date_trunc("day", Conversation.created_at).label("day"),
            func.count(Conversation.id).label("count"),
        )
        .where(
            Conversation.tenant_id == tenant_id,
            Conversation.created_at >= since,
        )
        .group_by(func.date_trunc("day", Conversation.created_at))
        .order_by(func.date_trunc("day", Conversation.created_at))
    )

    rows = result.all()
    return [{"date": row.day.date(), "count": row.count} for row in rows]


async def get_daily_messages(db: AsyncSession, tenant_id: UUID) -> list[dict]:
    """Get message count per day for the last 30 days."""
    since = _thirty_days_ago()

    result = await db.execute(
        select(
            func.date_trunc("day", Message.created_at).label("day"),
            func.count(Message.id).label("count"),
        )
        .join(Conversation, Message.conversation_id == Conversation.id)
        .where(
            Conversation.tenant_id == tenant_id,
            Message.created_at >= since,
        )
        .group_by(func.date_trunc("day", Message.created_at))
        .order_by(func.date_trunc("day", Message.created_at))
    )

    rows = result.all()
    return [{"date": row.day.date(), "count": row.count} for row in rows]


async def get_top_agents(db: AsyncSession, tenant_id: UUID) -> list[dict]:
    """Get top 5 agents by conversation count this month."""
    month_start = _start_of_month()

    result = await db.execute(
        select(
            AiAgent.id.label("agent_id"),
            AiAgent.name.label("agent_name"),
            func.count(Conversation.id).label("conversations"),
        )
        .join(Conversation, Conversation.ai_agent_id == AiAgent.id)
        .where(
            AiAgent.tenant_id == tenant_id,
            Conversation.created_at >= month_start,
        )
        .group_by(AiAgent.id, AiAgent.name)
        .order_by(func.count(Conversation.id).desc())
        .limit(5)
    )

    rows = result.all()
    return [
        {
            "agent_id": row.agent_id,
            "agent_name": row.agent_name,
            "conversations": row.conversations,
        }
        for row in rows
    ]
