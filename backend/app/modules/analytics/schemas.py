from pydantic import BaseModel
from datetime import date
from uuid import UUID


class OverviewResponse(BaseModel):
    total_conversations: int
    total_messages: int
    total_customers: int
    active_agents: int
    revenue_this_month: float


class DailyCount(BaseModel):
    date: date
    count: int


class TopAgent(BaseModel):
    agent_id: UUID
    agent_name: str
    conversations: int
