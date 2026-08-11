from sqlalchemy import Column, String, UUID, JSON, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
from sqlalchemy.orm import relationship

class Plan(Base, BaseMixin):
    __tablename__ = 'plans'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    name = Column(String)
    slug = Column(String)
    price_monthly = Column(String)
    description = Column(String, nullable=True)
    features = Column(JSON, default=list)  # ["1 AI agent", "100 pesan/bulan", ...]
    is_popular = Column(Boolean, default=False)
    cta_text = Column(String, nullable=True)
    sort_order = Column(Integer, default=0)
    limits = Column(JSON)
    is_active = Column(Boolean)
    subscriptions = relationship('Subscription', back_populates='plan')