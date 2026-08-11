from sqlalchemy import Column, String, UUID, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class Tenant(Base, BaseMixin):
    __tablename__ = 'tenants'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    name = Column(String)
    slug = Column(String)
    plan_id = Column(UUID(as_uuid=True))
    settings = Column(JSON)
    users = relationship('User', back_populates='tenant')
    ai_agents = relationship('AiAgent', back_populates='tenant')
    customers = relationship('Customer', back_populates='tenant')
    subscriptions = relationship('Subscription', back_populates='tenant')
    invoices = relationship('Invoice', back_populates='tenant')
    usage_logs = relationship('UsageLog', back_populates='tenant')
    knowledge_bases = relationship('KnowledgeBase', back_populates='tenant')