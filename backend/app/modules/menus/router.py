from uuid import UUID, uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.deps import get_current_active_user, require_admin
from app.modules.models.user import User
from app.modules.models.menu import Menu

router = APIRouter(prefix="/menus", tags=["menus"])


class MenuOut(BaseModel):
    id: UUID
    module_key: Optional[str] = None
    key: str
    label: str
    icon: Optional[str] = None
    href: str
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
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


# --- Public: get module sub-menus (uses global defaults + tenant overrides) ---

@router.get("/{module_key}", response_model=list[MenuOut])
async def get_module_menus(module_key: str, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    """Get sub-menus for a module. Returns tenant-specific if exists, otherwise global defaults."""
    # Try tenant-specific first
    result = await db.execute(
        select(Menu).where(
            Menu.module_key == module_key,
            Menu.tenant_id == user.tenant_id,
            Menu.is_active == True,
        ).order_by(Menu.sort_order)
    )
    menus = result.scalars().all()
    if menus:
        return menus

    # Fallback to global defaults
    result = await db.execute(
        select(Menu).where(
            Menu.module_key == module_key,
            Menu.tenant_id.is_(None),
            Menu.is_active == True,
        ).order_by(Menu.sort_order)
    )
    return result.scalars().all()


# --- Tenant owner/admin: manage module menus for their tenant ---

@router.post("/{module_key}", response_model=MenuOut, status_code=201)
async def create_module_menu(module_key: str, data: MenuCreate, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    """Owner/admin add a sub-menu to a module for their tenant."""
    if user.role not in ("owner", "admin"):
        raise HTTPException(status_code=403, detail="Only owner/admin can manage module menus")
    menu = Menu(
        id=uuid4(), tenant_id=user.tenant_id, module_key=module_key,
        key=data.key, label=data.label, icon=data.icon,
        href=data.href, sort_order=data.sort_order, is_active=data.is_active,
    )
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


@router.put("/{module_key}/{menu_id}", response_model=MenuOut)
async def update_module_menu(module_key: str, menu_id: UUID, data: MenuUpdate, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ("owner", "admin"):
        raise HTTPException(status_code=403, detail="Only owner/admin can manage module menus")
    menu = await db.get(Menu, menu_id)
    if not menu or menu.module_key != module_key:
        raise HTTPException(status_code=404, detail="Menu not found")
    # Only allow editing own tenant's menus or global (if saas admin)
    if menu.tenant_id is not None and menu.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot edit other tenant's menus")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(menu, k, v)
    await db.commit()
    await db.refresh(menu)
    return menu


# --- SaaS Admin: manage global menus ---

@router.get("", response_model=list[MenuOut])
async def list_all_global_menus(module_key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    """Public: list global menus (for landing/public pages) or filter by module."""
    q = select(Menu).where(Menu.tenant_id.is_(None), Menu.is_active == True)
    if module_key:
        q = q.where(Menu.module_key == module_key)
    q = q.order_by(Menu.module_key, Menu.sort_order)
    result = await db.execute(q)
    return result.scalars().all()
