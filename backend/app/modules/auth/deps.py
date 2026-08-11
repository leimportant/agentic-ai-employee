from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.auth.service import get_current_user
from app.modules.models.user import User
from app.modules.models.user_module_access import UserModuleAccess

security = HTTPBearer()


async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await get_current_user(db, credentials.credentials)


async def require_admin(user: User = Depends(get_current_active_user)) -> User:
    if user.role not in ("admin", "owner"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def require_module(module_key: str):
    """Dependency factory: check if user has access to a specific module."""
    async def checker(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
        if user.role in ("owner", "admin"):
            return user
        result = await db.execute(
            select(UserModuleAccess).where(
                UserModuleAccess.user_id == user.id,
                UserModuleAccess.module_key == module_key,
            )
        )
        if not result.scalars().first():
            raise HTTPException(status_code=403, detail=f"No access to module: {module_key}")
        return user
    return checker


def require_sub_menu(module_key: str, sub_menu: str):
    """Dependency factory: check if user has access to a specific sub-menu."""
    async def checker(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
        if user.role in ("owner", "admin"):
            return user
        result = await db.execute(
            select(UserModuleAccess).where(
                UserModuleAccess.user_id == user.id,
                UserModuleAccess.module_key == module_key,
            )
        )
        rows = result.scalars().all()
        if not rows:
            raise HTTPException(status_code=403, detail=f"No access to module: {module_key}")
        # If any row has sub_menu=NULL → full access to module
        if any(r.sub_menu is None for r in rows):
            return user
        # Check specific sub_menu
        if not any(r.sub_menu == sub_menu for r in rows):
            raise HTTPException(status_code=403, detail=f"No access to {module_key}/{sub_menu}")
        return user
    return checker
