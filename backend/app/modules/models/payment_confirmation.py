import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin


class PaymentConfirmation(Base, BaseMixin):
    __tablename__ = "payment_confirmations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), nullable=False)
    plan_id = Column(PGUUID(as_uuid=True), nullable=False)
    amount = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)        # bank pengirim
    account_name = Column(String, nullable=False)     # nama pengirim
    proof_url = Column(String, nullable=False)        # URL bukti transfer
    status = Column(String, default="pending")        # pending | approved | rejected
    notes = Column(String, nullable=True)             # catatan admin saat reject
    reviewed_by = Column(PGUUID(as_uuid=True), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
