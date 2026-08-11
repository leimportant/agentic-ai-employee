from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class Customer(Base, BaseMixin):
    __tablename__ = 'customers'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    channel = Column(String)
    last_contact_at = Column(DateTime)
    tenant = relationship('Tenant', back_populates='customers')
    conversations = relationship('Conversation', back_populates='customer')
