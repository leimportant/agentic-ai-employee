"""
Trial Period Logic
- On register: auto-assign 14-day Pro trial
- On trial expire: downgrade to Starter
"""

from uuid import UUID, uuid4
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.modules.models.plan import Plan
from app.modules.models.subscription import Subscription
from app.modules.models.tenant import Tenant


async def activate_trial(db: AsyncSession, tenant_id: UUID):
    """Give tenant a 14-day Pro trial subscription."""
    # Find Pro plan
    result = await db.execute(select(Plan).where(Plan.slug == "pro", Plan.is_active == True))
    pro_plan = result.scalar_one_or_none()

    if not pro_plan:
        # Fallback: find any active plan that's not starter
        result = await db.execute(select(Plan).where(Plan.slug != "starter", Plan.is_active == True).limit(1))
        pro_plan = result.scalar_one_or_none()

    if not pro_plan:
        return  # No plan to trial, skip

    now = datetime.utcnow()
    sub = Subscription(
        id=uuid4(),
        tenant_id=tenant_id,
        plan_id=pro_plan.id,
        status="trialing",
        current_period_start=now,
        current_period_end=now + timedelta(days=settings.TRIAL_DAYS),
    )
    db.add(sub)

    # Update tenant plan
    tenant = await db.get(Tenant, tenant_id)
    if tenant:
        tenant.plan_id = pro_plan.id

    await db.commit()


async def check_trial_expired(db: AsyncSession, tenant_id: UUID) -> bool:
    """Check if tenant's trial has expired. If so, downgrade to Starter."""
    result = await db.execute(
        select(Subscription).where(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "trialing",
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return False

    if sub.current_period_end < datetime.utcnow():
        # Expired — downgrade
        sub.status = "expired"

        # Find starter plan
        starter_result = await db.execute(select(Plan).where(Plan.slug == "starter"))
        starter = starter_result.scalar_one_or_none()

        if starter:
            tenant = await db.get(Tenant, tenant_id)
            if tenant:
                tenant.plan_id = starter.id

            # Create starter subscription
            now = datetime.utcnow()
            new_sub = Subscription(
                id=uuid4(),
                tenant_id=tenant_id,
                plan_id=starter.id,
                status="active",
                current_period_start=now,
                current_period_end=now + timedelta(days=36500),  # "forever"
            )
            db.add(new_sub)

        await db.commit()
        return True

    return False


async def get_trial_info(db: AsyncSession, tenant_id: UUID) -> dict | None:
    """Get trial status for tenant. Returns None if not trialing."""
    result = await db.execute(
        select(Subscription).where(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "trialing",
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return None

    days_left = (sub.current_period_end - datetime.utcnow()).days
    return {
        "status": "trialing",
        "days_left": max(days_left, 0),
        "expires_at": sub.current_period_end.isoformat(),
    }
