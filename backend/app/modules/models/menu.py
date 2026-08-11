import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.modules.models.base import Base, BaseMixin


class Menu(Base, BaseMixin):
    __tablename__ = "menus"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), nullable=True)  # NULL = saas global, filled = tenant-specific
    module_key = Column(String, nullable=True)   # NULL = saas top-level menu, "konveksi" = sub-menu of konveksi
    key = Column(String, nullable=False)          # unique identifier: "orders", "production", "cutting"
    label = Column(String, nullable=False)        # display name
    icon = Column(String, nullable=True)          # lucide icon name
    href = Column(String, nullable=False)         # route path
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
