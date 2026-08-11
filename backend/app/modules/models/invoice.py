from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class Invoice(Base, BaseMixin):
    __tablename__ = 'invoices'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)
    subscription_id = Column(PGUUID(as_uuid=True), ForeignKey('subscriptions.id'), nullable=True)
    amount = Column(String)
    status = Column(String)
    paid_at = Column(DateTime)
    payment_method = Column(String)
    subscription = relationship('Subscription', back_populates='invoices')
