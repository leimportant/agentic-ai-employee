from uuid import UUID, uuid4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models.notification import Notification


async def list_notifications(db: AsyncSession, tenant_id: UUID, user_id: UUID, limit: int = 20):
    result = await db.execute(
        select(Notification)
        .where(
            Notification.tenant_id == tenant_id,
            (Notification.user_id == user_id) | (Notification.user_id.is_(None)),
        )
        .order_by(Notification.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def unread_count(db: AsyncSession, tenant_id: UUID, user_id: UUID) -> int:
    from sqlalchemy import func
    result = await db.execute(
        select(func.count())
        .where(
            Notification.tenant_id == tenant_id,
            (Notification.user_id == user_id) | (Notification.user_id.is_(None)),
            Notification.is_read == False,
        )
    )
    return result.scalar() or 0


async def mark_read(db: AsyncSession, notification_id: UUID):
    await db.execute(
        update(Notification).where(Notification.id == notification_id).values(is_read=True)
    )
    await db.commit()


async def mark_all_read(db: AsyncSession, tenant_id: UUID, user_id: UUID):
    await db.execute(
        update(Notification)
        .where(
            Notification.tenant_id == tenant_id,
            (Notification.user_id == user_id) | (Notification.user_id.is_(None)),
            Notification.is_read == False,
        )
        .values(is_read=True)
    )
    await db.commit()


async def create_notification(
    db: AsyncSession,
    tenant_id: UUID,
    type: str,
    title: str,
    message: str,
    user_id: UUID | None = None,
    action_url: str | None = None,
) -> Notification:
    notif = Notification(
        id=uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        action_url=action_url,
    )
    db.add(notif)
    await db.commit()
    await db.refresh(notif)
    return notif


# --- Trigger helpers (call from other services) ---

async def notify_usage_warning(db: AsyncSession, tenant_id: UUID, metric: str, pct: int):
    await create_notification(
        db, tenant_id,
        type="usage_warning",
        title=f"Kuota {metric} hampir habis",
        message=f"Penggunaan {metric} sudah mencapai {pct}%. Upgrade plan untuk menghindari limitasi.",
        action_url="/billing",
    )


async def notify_payment_success(db: AsyncSession, tenant_id: UUID, plan_name: str):
    await create_notification(
        db, tenant_id,
        type="payment",
        title="Pembayaran berhasil",
        message=f"Subscription plan {plan_name} telah aktif.",
        action_url="/billing",
    )


async def notify_payment_failed(db: AsyncSession, tenant_id: UUID):
    await create_notification(
        db, tenant_id,
        type="payment",
        title="Pembayaran gagal",
        message="Pembayaran gagal diproses. Silakan update metode pembayaran.",
        action_url="/billing",
    )


async def notify_member_joined(db: AsyncSession, tenant_id: UUID, member_name: str):
    await create_notification(
        db, tenant_id,
        type="team_invite",
        title="Anggota baru bergabung",
        message=f"{member_name} telah menerima undangan dan bergabung ke tim.",
        action_url="/settings?tab=team",
    )
