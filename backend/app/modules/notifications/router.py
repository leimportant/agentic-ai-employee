from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.modules.notifications import service

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationOut(BaseModel):
    id: UUID
    type: str
    title: str
    message: str
    action_url: Optional[str]
    is_read: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[NotificationOut])
async def list_notifications(tenant_id: UUID, user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.list_notifications(db, tenant_id, user_id)


@router.get("/unread-count")
async def unread_count(tenant_id: UUID, user_id: UUID, db: AsyncSession = Depends(get_db)):
    count = await service.unread_count(db, tenant_id, user_id)
    return {"count": count}


@router.post("/{notification_id}/read")
async def mark_read(notification_id: UUID, db: AsyncSession = Depends(get_db)):
    await service.mark_read(db, notification_id)
    return {"status": "ok"}


@router.post("/read-all")
async def mark_all_read(tenant_id: UUID, user_id: UUID, db: AsyncSession = Depends(get_db)):
    await service.mark_all_read(db, tenant_id, user_id)
    return {"status": "ok"}
