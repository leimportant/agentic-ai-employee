from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin


class Notification(Base, BaseMixin):
    __tablename__ = "notifications"
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), nullable=True)  # null = broadcast to tenant
    type = Column(String, nullable=False)  # team_invite | usage_warning | payment | system
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    action_url = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
