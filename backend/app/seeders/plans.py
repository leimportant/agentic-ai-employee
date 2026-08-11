"""
Seeder for plans table.
Run: cd backend && .venv\\Scripts\\activate; python -m app.seeders.plans
"""
import asyncio
import uuid

from sqlalchemy import text
from app.database import async_session

PLANS_DATA = [
    {
        "name": "Free",
        "slug": "free",
        "price_monthly": "Rp 0",
        "description": "Untuk coba-coba dan project kecil",
        "features": ["1 AI agent", "100 pesan/bulan", "1 user", "Web chat only"],
        "is_popular": False,
        "cta_text": "Mulai Gratis",
        "sort_order": 0,
        "limits": {"messages": 100, "agents": 1, "apps": 1, "storage_mb": 50, "users": 1},
        "is_active": True,
    },
    {
        "name": "Starter",
        "slug": "starter",
        "price_monthly": "Rp 99.000",
        "description": "Untuk UMKM yang mulai scale",
        "features": ["3 AI agents", "5.000 pesan/bulan", "5 users", "WhatsApp + Telegram", "Dashboard analytics"],
        "is_popular": True,
        "cta_text": "Pilih Starter",
        "sort_order": 1,
        "limits": {"messages": 5000, "agents": 3, "apps": 3, "storage_mb": 500, "users": 5},
        "is_active": True,
    },
    {
        "name": "Pro",
        "slug": "pro",
        "price_monthly": "Rp 299.000",
        "description": "Untuk bisnis serius yang butuh lebih",
        "features": ["Unlimited agents", "Unlimited pesan", "Unlimited users", "Priority support", "Custom AI training", "API access"],
        "is_popular": False,
        "cta_text": "Pilih Pro",
        "sort_order": 2,
        "limits": {"messages": -1, "agents": -1, "apps": -1, "storage_mb": 5000, "users": -1},
        "is_active": True,
    },
]


async def seed():
    import json

    async with async_session() as session:
        for data in PLANS_DATA:
            result = await session.execute(
                text("SELECT id FROM plans WHERE slug = :slug"),
                {"slug": data["slug"]},
            )
            if result.scalar_one_or_none() is None:
                await session.execute(
                    text("""
                        INSERT INTO plans (id, name, slug, price_monthly, description, features, is_popular, cta_text, sort_order, limits, is_active)
                        VALUES (:id, :name, :slug, :price_monthly, :description, :features, :is_popular, :cta_text, :sort_order, :limits, :is_active)
                    """),
                    {
                        "id": str(uuid.uuid4()),
                        "name": data["name"],
                        "slug": data["slug"],
                        "price_monthly": data["price_monthly"],
                        "description": data["description"],
                        "features": json.dumps(data["features"]),
                        "is_popular": data["is_popular"],
                        "cta_text": data["cta_text"],
                        "sort_order": data["sort_order"],
                        "limits": json.dumps(data["limits"]),
                        "is_active": data["is_active"],
                    },
                )
        await session.commit()
        print(f"[OK] Seeded {len(PLANS_DATA)} plans (skipped existing).")


if __name__ == "__main__":
    asyncio.run(seed())
