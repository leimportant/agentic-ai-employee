from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.billing import service, schemas
from app.modules.auth.deps import get_current_active_user
from app.modules.models.user import User

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/plans", response_model=list[schemas.PlanOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    return await service.get_plans(db)


@router.get("/overview", response_model=schemas.BillingOverview)
async def billing_overview(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_billing_overview(db, user.tenant_id)


@router.get("/usage", response_model=schemas.UsageOut)
async def get_usage(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_usage(db, user.tenant_id)


@router.post("/subscribe", response_model=schemas.SubscriptionOut)
async def subscribe(
    req: schemas.SubscribeRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    sub = await service.subscribe(db, user.tenant_id, req)
    return schemas.SubscriptionOut(
        id=sub.id,
        plan=schemas.PlanOut.model_validate(sub.plan),
        status=sub.status,
        current_period_start=sub.current_period_start,
        current_period_end=sub.current_period_end,
    )


@router.post("/cancel")
async def cancel(
    req: schemas.CancelRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.cancel_subscription(db, user.tenant_id, req)


@router.post("/webhook")
async def payment_webhook(payload: schemas.WebhookPayload, db: AsyncSession = Depends(get_db)):
    """Receive payment gateway webhook (Midtrans/Xendit)."""
    return await service.process_webhook(db, payload)


@router.get("/invoices", response_model=list[schemas.InvoiceOut])
async def list_invoices(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_invoices(db, user.tenant_id)



@router.get("/bank-info")
async def get_bank_info():
    """Return bank account info for manual transfer."""
    from app.config import settings
    return {
        "bank_name": settings.BANK_NAME,
        "account_number": settings.BANK_ACCOUNT_NUMBER,
        "account_name": settings.BANK_ACCOUNT_NAME,
    }


@router.post("/pay")
async def submit_payment_confirmation(
    plan_id: str = Form(...),
    amount: str = Form(...),
    bank_name: str = Form(...),
    account_name: str = Form(...),
    proof: UploadFile = File(...),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """User uploads payment proof after transferring."""
    from fastapi import HTTPException

    # Validate file type
    allowed_types = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
    if proof.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File harus JPG, PNG, WebP, atau PDF")

    # Validate file size (max 5MB)
    contents = await proof.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Ukuran file maksimal 5MB")
    await proof.seek(0)

    return await service.create_payment_confirmation(
        db, user=user, plan_id=UUID(plan_id),
        amount=amount, bank_name=bank_name,
        account_name=account_name, proof=proof,
    )
