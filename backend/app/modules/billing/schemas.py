from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


# --- Request ---

class SubscribeRequest(BaseModel):
    plan_id: UUID
    payment_method: Optional[str] = None  # "midtrans" | "xendit"


class CancelRequest(BaseModel):
    reason: Optional[str] = None
    immediate: bool = False  # False = end of period


class WebhookPayload(BaseModel):
    """Generic webhook from payment gateway."""
    order_id: str
    transaction_status: str  # "settlement" | "pending" | "expire" | "cancel"
    gross_amount: str
    payment_type: Optional[str] = None
    signature_key: Optional[str] = None


# --- Response ---

class PlanOut(BaseModel):
    id: UUID
    name: str
    slug: str
    price_monthly: str
    description: Optional[str] = None
    features: Optional[list[str]] = None
    is_popular: bool = False
    cta_text: Optional[str] = None
    sort_order: int = 0
    limits: dict
    is_active: bool

    class Config:
        from_attributes = True


class SubscriptionOut(BaseModel):
    id: UUID
    plan: PlanOut
    status: str  # "active" | "trialing" | "past_due" | "canceled" | "expired"
    current_period_start: datetime
    current_period_end: datetime

    class Config:
        from_attributes = True


class UsageOut(BaseModel):
    messages: int
    messages_limit: int
    agents: int
    agents_limit: int
    apps: int
    apps_limit: int
    users: int
    users_limit: int
    storage_mb: int
    storage_limit_mb: int
    period_start: datetime
    period_end: datetime


class InvoiceOut(BaseModel):
    id: UUID
    amount: str
    status: str
    paid_at: Optional[datetime]
    payment_method: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class BillingOverview(BaseModel):
    subscription: Optional[SubscriptionOut]
    usage: UsageOut
    invoices: list[InvoiceOut]
