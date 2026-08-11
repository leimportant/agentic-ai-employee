"""
Seeder for menus table (global defaults).
Run: cd backend && .venv\\Scripts\\activate; python -m app.seeders.menus
"""
import asyncio
import uuid
import json

from sqlalchemy import text
from app.database import async_session

# tenant_id=NULL, module_key=NULL → SaaS top-level (already handled by app_modules, skip)
# tenant_id=NULL, module_key="ai-cs" → default sub-menus for AI CS module
# tenant_id=NULL, module_key="konveksi" → default sub-menus for Konveksi module

MENUS_DATA = [
    # --- AI CS sub-menus ---
    {"module_key": "ai-cs", "key": "dashboard", "label": "Dashboard", "icon": "BarChart3", "href": "/apps/ai-cs", "sort_order": 0},
    {"module_key": "ai-cs", "key": "agents", "label": "Agents", "icon": "Bot", "href": "/apps/ai-cs/agents", "sort_order": 1},
    {"module_key": "ai-cs", "key": "conversations", "label": "Conversations", "icon": "MessageSquare", "href": "/apps/ai-cs/conversations", "sort_order": 2},
    {"module_key": "ai-cs", "key": "settings", "label": "Settings", "icon": "Settings", "href": "/apps/ai-cs/settings", "sort_order": 3},

    # --- Konveksi sub-menus ---
    {"module_key": "konveksi", "key": "overview", "label": "Overview", "icon": "Factory", "href": "/apps/konveksi", "sort_order": 0},
    {"module_key": "konveksi", "key": "orders", "label": "Orders", "icon": "ClipboardList", "href": "/apps/konveksi/orders", "sort_order": 1},
    {"module_key": "konveksi", "key": "production", "label": "Produksi", "icon": "Layers", "href": "/apps/konveksi/production", "sort_order": 2},
    {"module_key": "konveksi", "key": "materials", "label": "Bahan", "icon": "Package", "href": "/apps/konveksi/materials", "sort_order": 3},
    {"module_key": "konveksi", "key": "workers", "label": "Pekerja", "icon": "Users", "href": "/apps/konveksi/workers", "sort_order": 4},

    # --- AI Sales sub-menus ---
    {"module_key": "ai-sales", "key": "dashboard", "label": "Dashboard", "icon": "BarChart3", "href": "/apps/ai-sales", "sort_order": 0},
    {"module_key": "ai-sales", "key": "leads", "label": "Leads", "icon": "UserPlus", "href": "/apps/ai-sales/leads", "sort_order": 1},
    {"module_key": "ai-sales", "key": "pipeline", "label": "Pipeline", "icon": "GitBranch", "href": "/apps/ai-sales/pipeline", "sort_order": 2},
    {"module_key": "ai-sales", "key": "settings", "label": "Settings", "icon": "Settings", "href": "/apps/ai-sales/settings", "sort_order": 3},

    # --- Inventory sub-menus ---
    {"module_key": "inventory", "key": "dashboard", "label": "Dashboard", "icon": "BarChart3", "href": "/apps/inventory", "sort_order": 0},
    {"module_key": "inventory", "key": "products", "label": "Products", "icon": "Package", "href": "/apps/inventory/products", "sort_order": 1},
    {"module_key": "inventory", "key": "stock", "label": "Stock", "icon": "Boxes", "href": "/apps/inventory/stock", "sort_order": 2},
    {"module_key": "inventory", "key": "alerts", "label": "Alerts", "icon": "AlertTriangle", "href": "/apps/inventory/alerts", "sort_order": 3},
]


async def seed():
    async with async_session() as session:
        for data in MENUS_DATA:
            result = await session.execute(
                text("SELECT id FROM menus WHERE module_key = :mk AND key = :key AND tenant_id IS NULL"),
                {"mk": data["module_key"], "key": data["key"]},
            )
            if result.scalar_one_or_none() is None:
                await session.execute(
                    text("""
                        INSERT INTO menus (id, tenant_id, module_key, key, label, icon, href, sort_order, is_active)
                        VALUES (:id, NULL, :module_key, :key, :label, :icon, :href, :sort_order, true)
                    """),
                    {"id": str(uuid.uuid4()), **data},
                )
        await session.commit()
        print(f"[OK] Seeded {len(MENUS_DATA)} menus (skipped existing).")


if __name__ == "__main__":
    asyncio.run(seed())
