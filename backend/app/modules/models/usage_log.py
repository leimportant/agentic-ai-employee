from sqlalchemy import Column, String, UUID, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class UsageLog(Base, BaseMixin):
    __tablename__ = 'usage_logs'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True))
    metric = Column(String)
    count = Column(String)
    period_start = Column(Date)
    tenant = relationship('Tenant', back_populates='usage_logs')