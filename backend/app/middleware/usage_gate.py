"""
Usage Gating Middleware
Enforces plan limits on specific endpoints.
Returns 429 when tenant exceeds their plan quota.
"""

from uuid import UUID
from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.billing import service

# Map: route pattern → metric to check
GATED_ROUTES: dict[str, str] = {
    "/api/v1/conversations/send": "messages",
    "/api/v1/ai-agents": "agents",       # POST only
    "/api/v1/apps/activate": "apps",      # POST only
    "/api/v1/team/invite": "users",       # POST only
}


async def usage_gate(request: Request, db: AsyncSession = Depends(get_db)):
    """
    FastAPI dependency that checks usage limits before allowing the request.
    Add to routes that consume quota.

    Usage:
        @router.post("/send", dependencies=[Depends(usage_gate)])
        async def send_message(...):
    """
    # Only gate mutating requests
    if request.method not in ("POST", "PUT"):
        return

    # Extract tenant_id from request state (set by auth middleware)
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        return  # No tenant = skip gating (will fail on auth anyway)

    # Find which metric to check
    path = request.url.path
    metric = None
    for route_pattern, route_metric in GATED_ROUTES.items():
        if path.startswith(route_pattern):
            metric = route_metric
            break

    if not metric:
        return  # Route not gated

    # Check limit
    within_limit = await service.check_limit(db, UUID(str(tenant_id)), metric)
    if not within_limit:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "quota_exceeded",
                "metric": metric,
                "message": f"Kuota {metric} sudah habis. Upgrade plan untuk melanjutkan.",
            },
        )


async def track_usage_after(request: Request, metric: str, db: AsyncSession):
    """
    Call after successful operation to increment usage counter.

    Usage:
        await track_usage_after(request, "messages", db)
    """
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id:
        await service.increment_usage(db, UUID(str(tenant_id)), metric)
