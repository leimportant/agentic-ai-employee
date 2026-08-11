from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agentic_ai"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "change-me-in-production"

    # Auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/api/auth/google/callback"

    # OTP - Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@agenticai.id"

    # OTP - Telegram
    TELEGRAM_BOT_TOKEN: str = ""

    # OTP - WhatsApp (Fonnte / WA Business API)
    WHATSAPP_API_URL: str = "https://api.fonnte.com/send"
    WHATSAPP_API_TOKEN: str = ""

    # Trial
    TRIAL_DAYS: int = 14

    # Bank Transfer
    BANK_NAME: str = "BCA"
    BANK_ACCOUNT_NUMBER: str = "1234567890"
    BANK_ACCOUNT_NAME: str = "PT Agentic AI"

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://app.agenticai.id"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
