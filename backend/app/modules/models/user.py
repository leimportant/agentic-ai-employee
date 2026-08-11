from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship


class User(Base, BaseMixin):
    __tablename__ = 'users'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey('tenants.id'), nullable=True)
    email = Column(String)
    name = Column(String)
    avatar_url = Column(String)
    provider = Column(String)
    role = Column(String)
    is_verified = Column(Boolean)
    phone = Column(String, nullable=True)
    telegram_chat_id = Column(String, nullable=True)
    tenant = relationship('Tenant', back_populates='users')
    otp_codes = relationship('OtpCode', back_populates='user')
