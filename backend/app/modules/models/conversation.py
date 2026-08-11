from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class Conversation(Base, BaseMixin):
    __tablename__ = 'conversations'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)
    ai_agent_id = Column(PGUUID(as_uuid=True), ForeignKey('ai_agents.id'), nullable=False)
    customer_id = Column(PGUUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    channel = Column(String)
    status = Column(String)
    ai_agent = relationship('AiAgent', back_populates='conversations')
    customer = relationship('Customer', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation')
