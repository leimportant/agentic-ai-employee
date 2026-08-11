from sqlalchemy import Column, String, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class AiAgent(Base, BaseMixin):
    __tablename__ = 'ai_agents'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)
    name = Column(String)
    type = Column(String)
    system_prompt = Column(String)
    config = Column(JSON)
    is_active = Column(Boolean)
    tenant = relationship('Tenant', back_populates='ai_agents')
    conversations = relationship('Conversation', back_populates='ai_agent')
    knowledge_bases = relationship('KnowledgeBase', back_populates='ai_agent')
