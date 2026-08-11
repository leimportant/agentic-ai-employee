from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.app_modules import service, schemas

router = APIRouter(prefix="/app-modules", tags=["app-modules"])


@router.get("", response_model=list[schemas.AppModuleOut])
async def list_app_modules(db: AsyncSession = Depends(get_db)):
    """Return all active app modules ordered by sort_order."""
    return await service.get_active_modules(db)
