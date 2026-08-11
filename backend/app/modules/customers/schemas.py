from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    channel: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    channel: Optional[str] = None


class CustomerOut(BaseModel):
    id: UUID
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    channel: Optional[str] = None
    last_contact_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CustomerListResponse(BaseModel):
    items: list[CustomerOut]
    total: int
    page: int
    per_page: int
