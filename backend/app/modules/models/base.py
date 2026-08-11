from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from app.database import Base  # Single source of truth for Base

class BaseMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)