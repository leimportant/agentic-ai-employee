from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.database import get_db
from app.config import settings
from app.modules.auth import service, schemas
from app.middleware.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, req: schemas.RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register → create user (unverified) → returns user_id for OTP step."""
    return await service.register(db, req)


@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, req: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login → sends OTP to email for verification."""
    return await service.login(db, req)


@router.post("/otp/send")
@limiter.limit("3/minute")
async def send_otp(request: Request, req: schemas.SendOTPRequest, db: AsyncSession = Depends(get_db)):
    """Send OTP via email/telegram/whatsapp."""
    return await service.send_otp(db, req)


@router.post("/otp/verify", response_model=schemas.TokenResponse)
@limiter.limit("5/minute")
async def verify_otp(request: Request, req: schemas.VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP → returns JWT tokens."""
    return await service.verify_otp_and_login(db, req)


@router.get("/google/login")
async def google_login():
    """Redirect user to Google OAuth consent screen."""
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + "&".join(f"{k}={v}" for k, v in params.items())
    return {"redirect_url": url}


@router.get("/google/callback", response_model=schemas.TokenResponse)
async def google_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Exchange Google auth code for user tokens."""
    # Exchange code for Google tokens
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        tokens = token_resp.json()

        # Get user info
        userinfo_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {tokens.get('access_token', '')}"},
        )
        userinfo = userinfo_resp.json()

    return await service.google_oauth_callback(
        db,
        email=userinfo.get("email", ""),
        name=userinfo.get("name", ""),
        avatar_url=userinfo.get("picture", ""),
    )
