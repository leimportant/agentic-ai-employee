from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AgentCreate(BaseModel):
    name: str
    type: str = "customer_service"
    system_prompt: str = "Kamu adalah AI Customer Service yang ramah dan membantu."
    config: Optional[dict] = None
    is_active: bool = True


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    system_prompt: Optional[str] = None
    config: Optional[dict] = None
    is_active: Optional[bool] = None


class AgentOut(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    type: str
    system_prompt: str
    config: Optional[dict] = None
    is_active: bool

    class Config:
        from_attributes = True
