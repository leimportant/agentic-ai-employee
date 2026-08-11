from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.models.app_module import AppModule


async def get_active_modules(db: AsyncSession):
    result = await db.execute(
        select(AppModule)
        .where(AppModule.is_active == True)
        .order_by(AppModule.sort_order)
    )
    return result.scalars().all()
