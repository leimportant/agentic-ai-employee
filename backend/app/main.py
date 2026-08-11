from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings

from app.modules.auth.router import router as auth_router
from app.modules.billing.router import router as billing_router
from app.modules.tenants.router import router as team_router
from app.modules.notifications.router import router as notifications_router
from app.modules.knowledge_base.router import router as kb_router
from app.modules.app_modules.router import router as app_modules_router
from app.modules.admin.router import router as admin_router
from app.modules.ai_agents.router import router as ai_agents_router
from app.modules.conversations.router import router as conversations_router
from app.modules.integrations.router import router as webhook_router
from app.modules.menus.router import router as menus_router
from app.modules.customers.router import router as customers_router
from app.modules.analytics.router import router as analytics_router
from app.middleware.rate_limiter import setup_rate_limiter

app = FastAPI(title="Agentic AI Employee Platform", version="0.1.0")
setup_rate_limiter(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(billing_router, prefix="/api/v1")
app.include_router(team_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(kb_router, prefix="/api/v1")
app.include_router(app_modules_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(ai_agents_router, prefix="/api/v1")
app.include_router(conversations_router, prefix="/api/v1")
app.include_router(webhook_router, prefix="/api/v1")
app.include_router(menus_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.get("/health")
def health_root():
    """Root health check for Docker/nginx."""
    return {"status": "ok"}

# Serve uploaded files
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
