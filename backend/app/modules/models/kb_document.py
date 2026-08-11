from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from pgvector.sqlalchemy import Vector
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class KbDocument(Base, BaseMixin):
    __tablename__ = 'kb_documents'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    knowledge_base_id = Column(UUID(as_uuid=True))
    title = Column(String)
    content = Column(String)
    embedding = Column(Vector(1536))
    knowledge_base = relationship('KnowledgeBase', back_populates='kb_documents')