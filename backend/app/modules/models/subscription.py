from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class Subscription(Base, BaseMixin):
    __tablename__ = 'subscriptions'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)
    plan_id = Column(PGUUID(as_uuid=True), ForeignKey('plans.id'), nullable=False)
    status = Column(String)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    tenant = relationship('Tenant', back_populates='subscriptions')
    plan = relationship('Plan', back_populates='subscriptions')
    invoices = relationship('Invoice', back_populates='subscription')
