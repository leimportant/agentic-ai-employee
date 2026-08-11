from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import require_admin

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


# --- Schemas ---

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    price_monthly: Optional[str] = None
    description: Optional[str] = None
    features: Optional[list[str]] = None
    is_popular: Optional[bool] = None
    cta_text: Optional[str] = None
    sort_order: Optional[int] = None
    limits: Optional[dict] = None
    is_active: Optional[bool] = None


class AppModuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    href: Optional[str] = None
    color: Optional[str] = None
    is_permanent: Optional[bool] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


# --- Plans CRUD ---

@router.get("/plans")
async def list_plans(db: AsyncSession = Depends(get_db)):
    from app.modules.models.plan import Plan
    result = await db.execute(select(Plan).order_by(Plan.sort_order))
    plans = result.scalars().all()
    return [_plan_dict(p) for p in plans]


@router.put("/plans/{plan_id}")
async def update_plan(plan_id: UUID, body: PlanUpdate, db: AsyncSession = Depends(get_db)):
    from app.modules.models.plan import Plan
    plan = await db.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    for key, val in body.model_dump(exclude_none=True).items():
        setattr(plan, key, val)
    await db.commit()
    await db.refresh(plan)
    return _plan_dict(plan)


def _plan_dict(p):
    return {
        "id": str(p.id), "name": p.name, "slug": p.slug,
        "price_monthly": p.price_monthly, "description": p.description,
        "features": p.features, "is_popular": p.is_popular,
        "cta_text": p.cta_text, "sort_order": p.sort_order,
        "limits": p.limits, "is_active": p.is_active,
    }


# --- App Modules CRUD ---

@router.get("/app-modules")
async def list_app_modules(db: AsyncSession = Depends(get_db)):
    from app.modules.models.app_module import AppModule
    result = await db.execute(select(AppModule).order_by(AppModule.sort_order))
    modules = result.scalars().all()
    return [_module_dict(m) for m in modules]


@router.put("/app-modules/{module_id}")
async def update_app_module(module_id: UUID, body: AppModuleUpdate, db: AsyncSession = Depends(get_db)):
    from app.modules.models.app_module import AppModule
    mod = await db.get(AppModule, module_id)
    if not mod:
        raise HTTPException(status_code=404, detail="App module not found")
    for key, val in body.model_dump(exclude_none=True).items():
        setattr(mod, key, val)
    await db.commit()
    await db.refresh(mod)
    return _module_dict(mod)


def _module_dict(m):
    return {
        "id": str(m.id), "key": m.key, "name": m.name,
        "description": m.description, "icon": m.icon,
        "href": m.href, "color": m.color,
        "is_permanent": m.is_permanent, "is_active": m.is_active,
        "sort_order": m.sort_order,
    }



# --- Payment Confirmations ---

class PaymentReviewRequest(BaseModel):
    notes: Optional[str] = None


@router.get("/payments")
async def list_payments(status: str = "pending", db: AsyncSession = Depends(get_db)):
    from app.modules.models.payment_confirmation import PaymentConfirmation
    result = await db.execute(
        select(PaymentConfirmation)
        .where(PaymentConfirmation.status == status)
        .order_by(PaymentConfirmation.created_at.desc())
    )
    payments = result.scalars().all()
    return [_payment_dict(p) for p in payments]


@router.post("/payments/{payment_id}/approve")
async def approve_payment(payment_id: UUID, db: AsyncSession = Depends(get_db)):
    from app.modules.models.payment_confirmation import PaymentConfirmation
    from app.modules.billing.service import activate_subscription_after_payment
    from datetime import datetime

    pc = await db.get(PaymentConfirmation, payment_id)
    if not pc:
        raise HTTPException(status_code=404, detail="Payment not found")
    if pc.status != "pending":
        raise HTTPException(status_code=400, detail="Already reviewed")

    pc.status = "approved"
    pc.reviewed_at = datetime.now()
    await db.commit()

    # Activate subscription
    await activate_subscription_after_payment(db, pc.tenant_id, pc.plan_id)
    return {"status": "approved"}


@router.post("/payments/{payment_id}/reject")
async def reject_payment(payment_id: UUID, body: PaymentReviewRequest, db: AsyncSession = Depends(get_db)):
    from app.modules.models.payment_confirmation import PaymentConfirmation
    from datetime import datetime

    pc = await db.get(PaymentConfirmation, payment_id)
    if not pc:
        raise HTTPException(status_code=404, detail="Payment not found")
    if pc.status != "pending":
        raise HTTPException(status_code=400, detail="Already reviewed")

    pc.status = "rejected"
    pc.notes = body.notes
    pc.reviewed_at = datetime.now()
    await db.commit()
    return {"status": "rejected"}


def _payment_dict(p):
    return {
        "id": str(p.id), "tenant_id": str(p.tenant_id),
        "user_id": str(p.user_id), "plan_id": str(p.plan_id),
        "amount": p.amount, "bank_name": p.bank_name,
        "account_name": p.account_name, "proof_url": p.proof_url,
        "status": p.status, "notes": p.notes,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


# --- Menus CRUD (SaaS admin — global menus) ---

class MenuCreate(BaseModel):
    module_key: Optional[str] = None
    key: str
    label: str
    icon: Optional[str] = None
    href: str
    sort_order: int = 0
    is_active: bool = True


class MenuUpdate(BaseModel):
    label: Optional[str] = None
    icon: Optional[str] = None
    href: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


@router.get("/menus")
async def list_global_menus(db: AsyncSession = Depends(get_db)):
    from app.modules.models.menu import Menu
    result = await db.execute(
        select(Menu).where(Menu.tenant_id.is_(None)).order_by(Menu.module_key, Menu.sort_order)
    )
    menus = result.scalars().all()
    return [_menu_dict(m) for m in menus]


@router.post("/menus")
async def create_global_menu(body: MenuCreate, db: AsyncSession = Depends(get_db)):
    from app.modules.models.menu import Menu
    from uuid import uuid4
    menu = Menu(
        id=uuid4(), tenant_id=None, module_key=body.module_key,
        key=body.key, label=body.label, icon=body.icon,
        href=body.href, sort_order=body.sort_order, is_active=body.is_active,
    )
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return _menu_dict(menu)


@router.put("/menus/{menu_id}")
async def update_global_menu(menu_id: UUID, body: MenuUpdate, db: AsyncSession = Depends(get_db)):
    from app.modules.models.menu import Menu
    menu = await db.get(Menu, menu_id)
    if not menu or menu.tenant_id is not None:
        raise HTTPException(status_code=404, detail="Global menu not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(menu, k, v)
    await db.commit()
    await db.refresh(menu)
    return _menu_dict(menu)


def _menu_dict(m):
    return {
        "id": str(m.id), "module_key": m.module_key, "key": m.key,
        "label": m.label, "icon": m.icon, "href": m.href,
        "sort_order": m.sort_order, "is_active": m.is_active,
    }
