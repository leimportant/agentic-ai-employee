from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class Message(Base, BaseMixin):
    __tablename__ = 'messages'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    conversation_id = Column(PGUUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    role = Column(String)
    content = Column(String)
    meta_data = Column('metadata', JSON)
    conversation = relationship('Conversation', back_populates='messages')
