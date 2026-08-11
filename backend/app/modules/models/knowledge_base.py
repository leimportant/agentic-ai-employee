from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class KnowledgeBase(Base, BaseMixin):
    __tablename__ = 'knowledge_bases'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True))
    ai_agent_id = Column(UUID(as_uuid=True))
    name = Column(String)
    tenant = relationship('Tenant', back_populates='knowledge_bases')
    ai_agent = relationship('AiAgent', back_populates='knowledge_bases')
    kb_documents = relationship('KbDocument', back_populates='knowledge_base')