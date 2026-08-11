from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class OtpCode(Base, BaseMixin):
    __tablename__ = 'otp_codes'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True))
    channel = Column(String)
    code = Column(String)
    expires_at = Column(DateTime)
    used_at = Column(DateTime)
    user = relationship('User', back_populates='otp_codes')