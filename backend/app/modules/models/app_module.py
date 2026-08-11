from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin
import uuid


class AppModule(Base, BaseMixin):
    __tablename__ = "app_modules"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False)  # e.g. "ai-cs"
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)  # lucide icon name e.g. "MessageSquare"
    href = Column(String, nullable=False)
    color = Column(String, nullable=False)  # tailwind class e.g. "bg-blue-600"
    is_permanent = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
