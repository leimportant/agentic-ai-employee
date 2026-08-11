"""
WhatsApp integration service.
Supports: Fonnte (default), Meta Official (future).
Each tenant stores their own WA config in tenant.settings:
  {
    "wa_provider": "fonnte",
    "wa_api_token": "xxx",
    "wa_webhook_secret": "yyy"
  }
"""
import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models.tenant import Tenant


async def send_whatsapp_message(db: AsyncSession, tenant_id: UUID, phone: str, message: str) -> dict:
    """Send a WhatsApp message via tenant's configured provider."""
    tenant = await db.get(Tenant, tenant_id)
    if not tenant or not tenant.settings:
        return {"success": False, "error": "No WA config"}

    settings = tenant.settings
    provider = settings.get("wa_provider", "fonnte")

    if provider == "fonnte":
        return await _send_fonnte(settings, phone, message)
    else:
        return {"success": False, "error": f"Unsupported provider: {provider}"}


async def _send_fonnte(settings: dict, phone: str, message: str) -> dict:
    token = settings.get("wa_api_token", "")
    url = settings.get("wa_api_url", "https://api.fonnte.com/send")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={"Authorization": token},
            json={"target": phone, "message": message},
        )
        data = resp.json()
        return {"success": data.get("status", False), "detail": data}
