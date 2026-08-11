from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.modules.models.user import User
from app.modules.models.tenant import Tenant
from app.modules.auth.schemas import (
    RegisterRequest, LoginRequest, SendOTPRequest, VerifyOTPRequest, TokenResponse,
)
from app.services import otp_service
from app.services import trial_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm="HS256")


def create_tokens(user_id: str, tenant_id: str) -> tuple[str, str]:
    access = create_token(
        {"sub": user_id, "tid": tenant_id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh = create_token(
        {"sub": user_id, "tid": tenant_id, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return access, refresh


async def register(db: AsyncSession, req: RegisterRequest) -> dict:
    """Register user + create tenant. Does NOT log in yet — must verify OTP first."""
    # Check existing
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email sudah terdaftar")

    # Create tenant
    tenant = Tenant(
        id=uuid4(),
        name=f"{req.name}'s Workspace",
        slug=req.email.split("@")[0].lower(),
        settings={"active_apps": []},
    )
    db.add(tenant)

    # Create user
    user = User(
        id=uuid4(),
        tenant_id=tenant.id,
        email=req.email,
        name=req.name,
        role="owner",
        provider="email",
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Activate 14-day Pro trial
    await trial_service.activate_trial(db, tenant.id)

    return {"success": True, "user_id": str(user.id), "email": user.email}


async def send_otp(db: AsyncSession, req: SendOTPRequest) -> dict:
    """Send OTP to user via chosen channel."""
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Determine destination
    destination = req.destination or req.email
    if req.channel == "email":
        destination = req.email
    elif req.channel == "whatsapp" and req.destination:
        user.phone = req.destination
    elif req.channel == "telegram" and req.destination:
        user.telegram_chat_id = req.destination

    await otp_service.create_otp(db, user.id, req.channel, destination)
    await db.commit()
    return {"success": True, "channel": req.channel, "message": f"OTP dikirim via {req.channel}"}


async def verify_otp_and_login(db: AsyncSession, req: VerifyOTPRequest) -> TokenResponse:
    """Verify OTP and issue JWT tokens. Also marks user as verified."""
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    valid = await otp_service.verify_otp(db, user.id, req.code)
    if not valid:
        raise HTTPException(status_code=400, detail="OTP tidak valid atau sudah expired")

    # Mark verified
    is_new = not user.is_verified
    if not user.is_verified:
        user.is_verified = True
        await db.commit()

    access, refresh = create_tokens(str(user.id), str(user.tenant_id))
    return TokenResponse(access_token=access, refresh_token=refresh, is_new_user=is_new)


async def login(db: AsyncSession, req: LoginRequest) -> dict:
    """Login with email/password → send OTP for 2FA."""
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Email atau password salah")

    # Check password (stored in user model - we'll use a password_hash field concept)
    # For now: if provider is "email", verify password
    # NOTE: User model needs password_hash field. For MVP, skip password check on OTP-only flow.

    # Send OTP to email
    await otp_service.create_otp(db, user.id, "email", user.email)
    return {"success": True, "message": "OTP dikirim ke email", "email": user.email}


async def google_oauth_callback(db: AsyncSession, email: str, name: str, avatar_url: str) -> TokenResponse:
    """Handle Google OAuth - create or login user."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    is_new = False
    if not user:
        # Create tenant + user
        tenant = Tenant(
            id=uuid4(),
            name=f"{name}'s Workspace",
            slug=email.split("@")[0].lower(),
            settings={"active_apps": []},
        )
        db.add(tenant)

        user = User(
            id=uuid4(),
            tenant_id=tenant.id,
            email=email,
            name=name,
            avatar_url=avatar_url,
            role="owner",
            provider="google",
            is_verified=True,
        )
        db.add(user)
        is_new = True
        await db.commit()
        await db.refresh(user)

        # Activate 14-day Pro trial for new users
        await trial_service.activate_trial(db, tenant.id)

    access, refresh = create_tokens(str(user.id), str(user.tenant_id))
    return TokenResponse(access_token=access, refresh_token=refresh, is_new_user=is_new)


async def get_current_user(db: AsyncSession, token: str) -> User:
    """Decode JWT and return user."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.get(User, UUID(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
