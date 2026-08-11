"""
Multi-channel OTP Service
Supports: email (SMTP), telegram, whatsapp
"""

import random
import smtplib
from email.mime.text import MIMEText
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.config import settings
from app.modules.models.otp_code import OtpCode

OTP_EXPIRY_MINUTES = 5
OTP_LENGTH = 6


def generate_otp() -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(OTP_LENGTH)])


async def create_otp(db: AsyncSession, user_id: UUID, channel: str, destination: str) -> str:
    """Create OTP record and send via chosen channel."""
    code = generate_otp()

    # Invalidate previous unused OTPs for this user
    result = await db.execute(
        select(OtpCode).where(
            OtpCode.user_id == user_id,
            OtpCode.used_at.is_(None),
        )
    )
    for old in result.scalars().all():
        old.used_at = datetime.utcnow()  # mark as expired

    otp = OtpCode(
        id=uuid4(),
        user_id=user_id,
        channel=channel,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
    )
    db.add(otp)
    await db.commit()

    # Send OTP via channel
    await _send_otp(channel, destination, code)
    return code


async def verify_otp(db: AsyncSession, user_id: UUID, code: str) -> bool:
    """Verify OTP code. Returns True if valid."""
    result = await db.execute(
        select(OtpCode).where(
            OtpCode.user_id == user_id,
            OtpCode.code == code,
            OtpCode.used_at.is_(None),
            OtpCode.expires_at > datetime.utcnow(),
        ).order_by(OtpCode.created_at.desc()).limit(1)
    )
    otp = result.scalar_one_or_none()
    if not otp:
        return False

    otp.used_at = datetime.utcnow()
    await db.commit()
    return True


# --- Channel Adapters ---

async def _send_otp(channel: str, destination: str, code: str):
    """Route OTP to correct channel adapter."""
    message = f"Kode OTP Anda: {code}\nBerlaku {OTP_EXPIRY_MINUTES} menit. Jangan berikan ke siapapun."

    if channel == "email":
        await _send_email(destination, code)
    elif channel == "telegram":
        await _send_telegram(destination, message)
    elif channel == "whatsapp":
        await _send_whatsapp(destination, message)
    else:
        raise ValueError(f"Unsupported OTP channel: {channel}")


async def _send_email(to_email: str, code: str):
    """Send OTP via SMTP email."""
    if not settings.SMTP_USER:
        # Dev mode: just log
        print(f"[DEV] OTP Email to {to_email}: {code}")
        return

    msg = MIMEText(
        f"<h2>Kode Verifikasi Anda</h2>"
        f"<p style='font-size:32px;font-weight:bold;letter-spacing:8px'>{code}</p>"
        f"<p>Kode berlaku {OTP_EXPIRY_MINUTES} menit.</p>"
        f"<p>Jika Anda tidak meminta kode ini, abaikan email ini.</p>",
        "html",
    )
    msg["Subject"] = f"Kode OTP: {code}"
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[ERROR] Email OTP failed: {e}")
        raise


async def _send_telegram(chat_id: str, message: str):
    """Send OTP via Telegram Bot API."""
    if not settings.TELEGRAM_BOT_TOKEN:
        print(f"[DEV] OTP Telegram to {chat_id}: {message}")
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"chat_id": chat_id, "text": message})
        if resp.status_code != 200:
            print(f"[ERROR] Telegram OTP failed: {resp.text}")
            raise Exception("Telegram send failed")


async def _send_whatsapp(phone: str, message: str):
    """Send OTP via WhatsApp API (Fonnte or WA Business)."""
    if not settings.WHATSAPP_API_TOKEN:
        print(f"[DEV] OTP WhatsApp to {phone}: {message}")
        return

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            settings.WHATSAPP_API_URL,
            headers={"Authorization": settings.WHATSAPP_API_TOKEN},
            json={"target": phone, "message": message},
        )
        if resp.status_code != 200:
            print(f"[ERROR] WhatsApp OTP failed: {resp.text}")
            raise Exception("WhatsApp send failed")
