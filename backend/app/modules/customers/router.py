from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import get_current_active_user
from app.modules.models.user import User
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerOut,
    CustomerListResponse,
)
from app.modules.customers import service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=CustomerListResponse)
async def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    channel: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    items, total = await service.list_customers(
        db=db,
        tenant_id=current_user.tenant_id,
        page=page,
        per_page=per_page,
        search=search,
        channel=channel,
    )
    return CustomerListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = await service.get_customer(db, current_user.tenant_id, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerOut, status_code=201)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = await service.create_customer(db, current_user.tenant_id, data)
    return customer


@router.put("/{customer_id}", response_model=CustomerOut)
async def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = await service.update_customer(db, current_user.tenant_id, customer_id, data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    deleted = await service.delete_customer(db, current_user.tenant_id, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
