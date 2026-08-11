from pydantic import BaseModel
from uuid import UUID


class AppModuleOut(BaseModel):
    id: UUID
    key: str
    name: str
    description: str
    icon: str
    href: str
    color: str
    is_permanent: bool
    is_active: bool
    sort_order: int

    class Config:
        from_attributes = True
