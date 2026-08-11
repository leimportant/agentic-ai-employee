from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.modules.auth.deps import get_current_active_user
from app.modules.models.user import User
from app.modules.models.user_module_access import UserModuleAccess
from app.modules.tenants import service, schemas
from app.middleware.usage_gate import usage_gate

router = APIRouter(prefix="/team", tags=["team"])


def _require_owner_or_admin(user: User):
    if user.role not in ("owner", "admin"):
        raise HTTPException(status_code=403, detail="Only owner/admin can manage team")


@router.get("/members", response_model=list[schemas.TeamMemberOut])
async def list_members(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await service.list_members(db, user.tenant_id)


@router.get("/invites", response_model=list[schemas.InviteOut])
async def list_invites(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    _require_owner_or_admin(user)
    return await service.list_invites(db, user.tenant_id)


@router.post("/invite", response_model=schemas.InviteOut, dependencies=[Depends(usage_gate)])
async def invite_member(req: schemas.InviteMemberRequest, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    _require_owner_or_admin(user)
    # Admin can only invite members, not other admins
    if user.role == "admin" and req.role != "member":
        raise HTTPException(status_code=403, detail="Admin can only invite members")
    return await service.invite_member(db, user.tenant_id, req.email, req.role, user.id)


@router.post("/invite/accept")
async def accept_invite(token: str, db: AsyncSession = Depends(get_db)):
    return await service.accept_invite(db, token)


@router.patch("/members/{user_id}/role", response_model=schemas.TeamMemberOut)
async def update_role(user_id: UUID, req: schemas.UpdateRoleRequest, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    # Only owner can change roles
    if user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can change roles")
    return await service.update_member_role(db, user.tenant_id, user_id, req.role)


@router.delete("/members/{user_id}")
async def remove_member(user_id: UUID, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    _require_owner_or_admin(user)
    return await service.remove_member(db, user.tenant_id, user_id)


# --- Module Access ---

class ModuleAccessItem(BaseModel):
    module_key: str
    sub_menus: list[str] | None = None  # None = all sub-menus


class AssignModulesRequest(BaseModel):
    modules: list[ModuleAccessItem]


@router.get("/members/{user_id}/modules")
async def get_member_modules(user_id: UUID, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserModuleAccess).where(UserModuleAccess.user_id == user_id)
    )
    rows = result.scalars().all()
    # Group by module_key
    access: dict[str, list[str]] = {}
    for row in rows:
        if row.module_key not in access:
            access[row.module_key] = []
        if row.sub_menu:
            access[row.module_key].append(row.sub_menu)
    # Convert: if sub_menus is empty list → means all (was stored as NULL)
    modules = [
        {"module_key": k, "sub_menus": v if v else None}
        for k, v in access.items()
    ]
    return {"modules": modules}


@router.put("/members/{user_id}/modules")
async def assign_modules(user_id: UUID, req: AssignModulesRequest, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    _require_owner_or_admin(user)
    # Remove existing
    await db.execute(delete(UserModuleAccess).where(UserModuleAccess.user_id == user_id))
    # Insert new
    for item in req.modules:
        if item.sub_menus:
            for sub in item.sub_menus:
                db.add(UserModuleAccess(user_id=user_id, module_key=item.module_key, sub_menu=sub))
        else:
            # NULL sub_menu = access all sub-menus
            db.add(UserModuleAccess(user_id=user_id, module_key=item.module_key, sub_menu=None))
    await db.commit()
    return {"status": "ok"}


@router.get("/me/modules")
async def my_modules(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    """Return current user's accessible modules + sub-menus (for sidebar filtering)."""
    if user.role in ("owner", "admin"):
        return {"role": user.role, "modules": "__all__"}
    result = await db.execute(
        select(UserModuleAccess).where(UserModuleAccess.user_id == user.id)
    )
    rows = result.scalars().all()
    access: dict[str, list[str]] = {}
    for row in rows:
        if row.module_key not in access:
            access[row.module_key] = []
        if row.sub_menu:
            access[row.module_key].append(row.sub_menu)
    modules = [
        {"module_key": k, "sub_menus": v if v else None}
        for k, v in access.items()
    ]
    return {"role": user.role, "modules": modules}
