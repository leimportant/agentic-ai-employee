from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin


class TeamInvite(Base, BaseMixin):
    __tablename__ = "team_invites"
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, default="member")  # owner | admin | member | viewer
    invited_by = Column(PGUUID(as_uuid=True), nullable=False)
    token = Column(String, unique=True, nullable=False)
    accepted = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
