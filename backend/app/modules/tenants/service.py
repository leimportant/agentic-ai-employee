import secrets
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.models.user import User
from app.modules.models.team_invite import TeamInvite
from app.modules.models.notification import Notification


async def list_members(db: AsyncSession, tenant_id: UUID) -> list[User]:
    result = await db.execute(
        select(User).where(User.tenant_id == tenant_id, User.deleted_at.is_(None))
    )
    return result.scalars().all()


async def list_invites(db: AsyncSession, tenant_id: UUID) -> list[TeamInvite]:
    result = await db.execute(
        select(TeamInvite).where(
            TeamInvite.tenant_id == tenant_id,
            TeamInvite.accepted == False,
            TeamInvite.expires_at > datetime.utcnow(),
        )
    )
    return result.scalars().all()


async def invite_member(
    db: AsyncSession, tenant_id: UUID, email: str, role: str, invited_by: UUID
) -> TeamInvite:
    # Check if already a member
    existing = await db.execute(
        select(User).where(User.tenant_id == tenant_id, User.email == email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User sudah menjadi member")

    # Check pending invite
    pending = await db.execute(
        select(TeamInvite).where(
            TeamInvite.tenant_id == tenant_id,
            TeamInvite.email == email,
            TeamInvite.accepted == False,
            TeamInvite.expires_at > datetime.utcnow(),
        )
    )
    if pending.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Invite sudah dikirim ke email ini")

    invite = TeamInvite(
        id=uuid4(),
        tenant_id=tenant_id,
        email=email,
        role=role,
        invited_by=invited_by,
        token=secrets.token_urlsafe(32),
        accepted=False,
        expires_at=datetime.utcnow() + timedelta(days=7),
    )
    db.add(invite)

    # Create notification for inviter
    notif = Notification(
        id=uuid4(),
        tenant_id=tenant_id,
        user_id=invited_by,
        type="team_invite",
        title="Undangan terkirim",
        message=f"Undangan telah dikirim ke {email} sebagai {role}",
        action_url="/settings?tab=team",
    )
    db.add(notif)

    await db.commit()
    await db.refresh(invite)
    return invite


async def accept_invite(db: AsyncSession, token: str) -> dict:
    result = await db.execute(
        select(TeamInvite).where(TeamInvite.token == token, TeamInvite.accepted == False)
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite tidak valid atau sudah expired")
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Invite sudah expired")

    invite.accepted = True

    # Create or link user to tenant
    user_result = await db.execute(select(User).where(User.email == invite.email))
    user = user_result.scalar_one_or_none()

    if user:
        user.tenant_id = invite.tenant_id
        user.role = invite.role
    else:
        user = User(
            id=uuid4(),
            tenant_id=invite.tenant_id,
            email=invite.email,
            name=invite.email.split("@")[0],
            role=invite.role,
            is_verified=False,
            provider="invite",
        )
        db.add(user)

    await db.commit()
    return {"message": "Invite accepted", "tenant_id": str(invite.tenant_id)}


async def update_member_role(db: AsyncSession, tenant_id: UUID, user_id: UUID, role: str) -> User:
    user = await db.get(User, user_id)
    if not user or str(user.tenant_id) != str(tenant_id):
        raise HTTPException(status_code=404, detail="Member tidak ditemukan")
    if user.role == "owner":
        raise HTTPException(status_code=400, detail="Tidak bisa mengubah role owner")

    user.role = role
    await db.commit()
    await db.refresh(user)
    return user


async def remove_member(db: AsyncSession, tenant_id: UUID, user_id: UUID) -> dict:
    user = await db.get(User, user_id)
    if not user or str(user.tenant_id) != str(tenant_id):
        raise HTTPException(status_code=404, detail="Member tidak ditemukan")
    if user.role == "owner":
        raise HTTPException(status_code=400, detail="Tidak bisa menghapus owner")

    user.deleted_at = datetime.utcnow()
    await db.commit()
    return {"message": f"{user.email} telah dihapus dari tim"}


async def revoke_invite(db: AsyncSession, tenant_id: UUID, invite_id: UUID) -> dict:
    result = await db.execute(
        select(TeamInvite).where(TeamInvite.id == invite_id, TeamInvite.tenant_id == tenant_id)
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite tidak ditemukan")

    await db.delete(invite)
    await db.commit()
    return {"message": "Invite dibatalkan"}
