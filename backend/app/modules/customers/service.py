from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models.customer import Customer
from app.modules.customers.schemas import CustomerCreate, CustomerUpdate


async def list_customers(
    db: AsyncSession,
    tenant_id: UUID,
    page: int = 1,
    per_page: int = 20,
    search: Optional[str] = None,
    channel: Optional[str] = None,
):
    base_query = select(Customer).where(
        Customer.tenant_id == tenant_id,
        Customer.deleted_at.is_(None),
    )

    if search:
        search_filter = f"%{search}%"
        base_query = base_query.where(
            or_(
                Customer.name.ilike(search_filter),
                Customer.phone.ilike(search_filter),
                Customer.email.ilike(search_filter),
            )
        )

    if channel:
        base_query = base_query.where(Customer.channel == channel)

    # Count total
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * per_page
    items_query = base_query.order_by(Customer.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(items_query)
    items = result.scalars().all()

    return items, total


async def get_customer(
    db: AsyncSession,
    tenant_id: UUID,
    customer_id: UUID,
) -> Optional[Customer]:
    query = select(Customer).where(
        Customer.id == customer_id,
        Customer.tenant_id == tenant_id,
        Customer.deleted_at.is_(None),
    )
    result = await db.execute(query)
    return result.scalars().first()


async def create_customer(
    db: AsyncSession,
    tenant_id: UUID,
    data: CustomerCreate,
) -> Customer:
    customer = Customer(
        id=uuid4(),
        tenant_id=tenant_id,
        name=data.name,
        phone=data.phone,
        email=data.email,
        channel=data.channel,
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


async def update_customer(
    db: AsyncSession,
    tenant_id: UUID,
    customer_id: UUID,
    data: CustomerUpdate,
) -> Optional[Customer]:
    customer = await get_customer(db, tenant_id, customer_id)
    if not customer:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return customer


async def delete_customer(
    db: AsyncSession,
    tenant_id: UUID,
    customer_id: UUID,
) -> bool:
    customer = await get_customer(db, tenant_id, customer_id)
    if not customer:
        return False

    customer.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    return True
