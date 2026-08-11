import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin


class UserModuleAccess(Base, BaseMixin):
    __tablename__ = "user_module_access"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    module_key = Column(String, nullable=False)  # e.g. "konveksi", "ai-cs"
    sub_menu = Column(String, nullable=True)     # e.g. "cutting", "sewing", NULL = all
