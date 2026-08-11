from uuid import UUID, uuid4
from datetime import datetime, timedelta, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.modules.models.plan import Plan
from app.modules.models.subscription import Subscription
from app.modules.models.invoice import Invoice
from app.modules.models.usage_log import UsageLog
from app.modules.models.tenant import Tenant
from app.modules.models.ai_agent import AiAgent
from app.modules.models.user import User
from app.modules.billing.schemas import (
    SubscribeRequest, CancelRequest, WebhookPayload,
    UsageOut, BillingOverview, SubscriptionOut, PlanOut, InvoiceOut,
)


async def get_plans(db: AsyncSession) -> list[Plan]:
    result = await db.execute(select(Plan).where(Plan.is_active == True))
    return result.scalars().all()


async def get_subscription(db: AsyncSession, tenant_id: UUID) -> Subscription | None:
    result = await db.execute(
        select(Subscription)
        .options(selectinload(Subscription.plan))
        .where(Subscription.tenant_id == tenant_id, Subscription.status.in_(["active", "trialing"]))
        .order_by(Subscription.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def subscribe(db: AsyncSession, tenant_id: UUID, req: SubscribeRequest) -> Subscription:
    # Check plan exists
    plan = await db.get(Plan, req.plan_id)
    if not plan or not plan.is_active:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Cancel existing active subscription
    existing = await get_subscription(db, tenant_id)
    if existing:
        existing.status = "canceled"
        existing.updated_at = datetime.utcnow()

    # Create new subscription
    now = datetime.utcnow()
    sub = Subscription(
        id=uuid4(),
        tenant_id=tenant_id,
        plan_id=plan.id,
        status="active" if plan.slug == "starter" else "pending",
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
    )
    db.add(sub)

    # Update tenant plan_id
    tenant = await db.get(Tenant, tenant_id)
    if tenant:
        tenant.plan_id = plan.id

    # Create invoice for paid plans
    if plan.slug != "starter":
        invoice = Invoice(
            id=uuid4(),
            tenant_id=tenant_id,
            subscription_id=sub.id,
            amount=plan.price_monthly,
            status="pending",
            paid_at=None,
            payment_method=req.payment_method,
        )
        db.add(invoice)

    await db.commit()
    await db.refresh(sub, ["plan"])
    return sub


async def cancel_subscription(db: AsyncSession, tenant_id: UUID, req: CancelRequest) -> dict:
    sub = await get_subscription(db, tenant_id)
    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription")

    if req.immediate:
        sub.status = "canceled"
        sub.current_period_end = datetime.utcnow()
    else:
        # Cancel at end of period
        sub.status = "canceled"
        # period_end stays the same — access until then

    await db.commit()
    return {"message": "Subscription canceled", "effective_date": str(sub.current_period_end)}


async def process_webhook(db: AsyncSession, payload: WebhookPayload) -> dict:
    """Process payment gateway webhook (Midtrans format)."""
    # order_id format: "sub_{subscription_id}"
    if not payload.order_id.startswith("sub_"):
        return {"status": "ignored"}

    sub_id = UUID(payload.order_id.replace("sub_", ""))
    sub = await db.get(Subscription, sub_id)
    if not sub:
        return {"status": "not_found"}

    if payload.transaction_status == "settlement":
        sub.status = "active"
        # Mark invoice paid
        result = await db.execute(
            select(Invoice).where(
                Invoice.subscription_id == sub_id,
                Invoice.status == "pending"
            ).limit(1)
        )
        invoice = result.scalar_one_or_none()
        if invoice:
            invoice.status = "paid"
            invoice.paid_at = datetime.utcnow()

    elif payload.transaction_status in ("expire", "cancel"):
        sub.status = "expired"

    await db.commit()
    return {"status": "processed", "subscription_status": sub.status}


async def get_usage(db: AsyncSession, tenant_id: UUID) -> UsageOut:
    """Get current period usage for a tenant."""
    sub = await get_subscription(db, tenant_id)

    # Defaults for free/no subscription
    limits = {"messages": 1000, "agents": 1, "apps": 2, "storage_mb": 100}
    period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    period_end = period_start + timedelta(days=30)

    if sub and sub.plan:
        limits = sub.plan.limits or limits
        period_start = sub.current_period_start
        period_end = sub.current_period_end

    # Count messages this period
    msg_result = await db.execute(
        select(func.coalesce(func.sum(func.cast(UsageLog.count, int)), 0))
        .where(
            UsageLog.tenant_id == tenant_id,
            UsageLog.metric == "messages",
            UsageLog.period_start >= period_start.date(),
        )
    )
    messages_used = msg_result.scalar() or 0

    # Count active agents
    agents_result = await db.execute(
        select(func.count()).where(AiAgent.tenant_id == tenant_id)
    )
    agents_count = agents_result.scalar() or 0

    # Count active apps (from tenant settings)
    tenant = await db.get(Tenant, tenant_id)
    apps_count = len((tenant.settings or {}).get("active_apps", []))

    # Count users in tenant
    users_result = await db.execute(
        select(func.count()).where(User.tenant_id == tenant_id)
    )
    users_count = users_result.scalar() or 0

    # Storage (sum of storage usage logs)
    storage_result = await db.execute(
        select(func.coalesce(func.sum(func.cast(UsageLog.count, int)), 0))
        .where(UsageLog.tenant_id == tenant_id, UsageLog.metric == "storage_mb")
    )
    storage_used = storage_result.scalar() or 0

    return UsageOut(
        messages=messages_used,
        messages_limit=limits.get("messages", 1000),
        agents=agents_count,
        agents_limit=limits.get("agents", 1),
        apps=apps_count,
        apps_limit=limits.get("apps", 2),
        users=users_count,
        users_limit=limits.get("users", 1),
        storage_mb=storage_used,
        storage_limit_mb=limits.get("storage_mb", 100),
        period_start=period_start,
        period_end=period_end,
    )


async def get_invoices(db: AsyncSession, tenant_id: UUID) -> list[Invoice]:
    result = await db.execute(
        select(Invoice)
        .where(Invoice.tenant_id == tenant_id)
        .order_by(Invoice.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


async def get_billing_overview(db: AsyncSession, tenant_id: UUID) -> BillingOverview:
    sub = await get_subscription(db, tenant_id)
    usage = await get_usage(db, tenant_id)
    invoices = await get_invoices(db, tenant_id)

    sub_out = None
    if sub:
        sub_out = SubscriptionOut(
            id=sub.id,
            plan=PlanOut.model_validate(sub.plan),
            status=sub.status,
            current_period_start=sub.current_period_start,
            current_period_end=sub.current_period_end,
        )

    return BillingOverview(
        subscription=sub_out,
        usage=usage,
        invoices=[InvoiceOut.model_validate(i) for i in invoices],
    )


async def increment_usage(db: AsyncSession, tenant_id: UUID, metric: str, count: int = 1):
    """Increment a usage metric for current period."""
    today = date.today()
    period_start = today.replace(day=1)

    # Upsert usage log
    result = await db.execute(
        select(UsageLog).where(
            UsageLog.tenant_id == tenant_id,
            UsageLog.metric == metric,
            UsageLog.period_start == period_start,
        )
    )
    log = result.scalar_one_or_none()

    if log:
        log.count = str(int(log.count or "0") + count)
    else:
        log = UsageLog(
            id=uuid4(),
            tenant_id=tenant_id,
            metric=metric,
            count=str(count),
            period_start=period_start,
        )
        db.add(log)

    await db.commit()


async def check_limit(db: AsyncSession, tenant_id: UUID, metric: str) -> bool:
    """Returns True if tenant is within limits, False if exceeded."""
    usage = await get_usage(db, tenant_id)
    limits_map = {
        "messages": (usage.messages, usage.messages_limit),
        "agents": (usage.agents, usage.agents_limit),
        "apps": (usage.apps, usage.apps_limit),
        "users": (usage.users, usage.users_limit),
        "storage_mb": (usage.storage_mb, usage.storage_limit_mb),
    }
    current, limit = limits_map.get(metric, (0, 999999))
    if limit == -1:  # unlimited
        return True
    return current < limit



async def create_payment_confirmation(
    db: AsyncSession, user, plan_id: UUID,
    amount: str, bank_name: str, account_name: str, proof,
):
    """Save payment confirmation (proof upload)."""
    import os
    from app.modules.models.payment_confirmation import PaymentConfirmation

    # Save file
    upload_dir = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "payments")
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{uuid4()}_{proof.filename}"
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, "wb") as f:
        f.write(await proof.read())

    pc = PaymentConfirmation(
        id=uuid4(),
        tenant_id=user.tenant_id,
        user_id=user.id,
        plan_id=plan_id,
        amount=amount,
        bank_name=bank_name,
        account_name=account_name,
        proof_url=f"/uploads/payments/{filename}",
        status="pending",
    )
    db.add(pc)
    await db.commit()
    return {"id": str(pc.id), "status": "pending", "message": "Bukti transfer diterima, menunggu verifikasi admin."}


async def activate_subscription_after_payment(db: AsyncSession, tenant_id, plan_id):
    """Activate subscription after admin approves payment."""
    plan = await db.get(Plan, plan_id)
    if not plan:
        return

    # Cancel existing
    existing = await get_subscription(db, tenant_id)
    if existing:
        existing.status = "canceled"

    now = datetime.utcnow()
    sub = Subscription(
        id=uuid4(),
        tenant_id=tenant_id,
        plan_id=plan.id,
        status="active",
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
    )
    db.add(sub)

    # Update tenant plan
    tenant = await db.get(Tenant, tenant_id)
    if tenant:
        tenant.plan_id = plan.id

    await db.commit()
