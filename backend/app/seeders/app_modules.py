"""
Seeder for app_modules table.
Run: cd backend && .venv\\Scripts\\activate; python -m app.seeders.app_modules
"""
import asyncio
import uuid

from sqlalchemy import text
from app.database import async_session

APP_MODULES_DATA = [
    {
        "key": "home",
        "name": "Home",
        "description": "Dashboard overview",
        "icon": "LayoutDashboard",
        "href": "/home",
        "color": "bg-gray-600",
        "is_permanent": True,
        "is_active": True,
        "sort_order": 0,
    },
    {
        "key": "ai-cs",
        "name": "AI Customer Service",
        "description": "Chatbot CS otomatis 24/7 untuk WhatsApp & web",
        "icon": "MessageSquare",
        "href": "/apps/ai-cs",
        "color": "bg-blue-600",
        "is_permanent": False,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "key": "ai-sales",
        "name": "AI Sales Agent",
        "description": "Automasi follow-up lead, pipeline, dan closing",
        "icon": "TrendingUp",
        "href": "/apps/ai-sales",
        "color": "bg-emerald-600",
        "is_permanent": False,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "key": "ai-support",
        "name": "AI Support",
        "description": "Ticket management & knowledge base dengan AI",
        "icon": "Headphones",
        "href": "/apps/ai-support",
        "color": "bg-violet-600",
        "is_permanent": False,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "key": "konveksi",
        "name": "Konveksi App",
        "description": "Monitoring produksi, order tracking, bahan baku",
        "icon": "Factory",
        "href": "/apps/konveksi",
        "color": "bg-orange-600",
        "is_permanent": False,
        "is_active": True,
        "sort_order": 4,
    },
    {
        "key": "inventory",
        "name": "Inventory",
        "description": "Stock management, product catalog, alerts",
        "icon": "Package",
        "href": "/apps/inventory",
        "color": "bg-cyan-600",
        "is_permanent": False,
        "is_active": True,
        "sort_order": 5,
    },
    {
        "key": "settings",
        "name": "Settings",
        "description": "Platform settings",
        "icon": "Settings",
        "href": "/settings",
        "color": "bg-gray-600",
        "is_permanent": True,
        "is_active": True,
        "sort_order": 99,
    },
]


async def seed():
    async with async_session() as session:
        for data in APP_MODULES_DATA:
            result = await session.execute(
                text("SELECT id FROM app_modules WHERE key = :key"),
                {"key": data["key"]},
            )
            if result.scalar_one_or_none() is None:
                await session.execute(
                    text("""
                        INSERT INTO app_modules (id, key, name, description, icon, href, color, is_permanent, is_active, sort_order)
                        VALUES (:id, :key, :name, :description, :icon, :href, :color, :is_permanent, :is_active, :sort_order)
                    """),
                    {"id": str(uuid.uuid4()), **data},
                )
        await session.commit()
        print(f"[OK] Seeded {len(APP_MODULES_DATA)} app modules (skipped existing).")


if __name__ == "__main__":
    asyncio.run(seed())
