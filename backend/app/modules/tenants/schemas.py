from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class InviteMemberRequest(BaseModel):
    email: EmailStr
    role: str = "member"  # admin | member | viewer


class UpdateRoleRequest(BaseModel):
    role: str  # admin | member | viewer


class TeamMemberOut(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    role: str
    is_verified: bool
    avatar_url: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class InviteOut(BaseModel):
    id: UUID
    email: str
    role: str
    accepted: bool
    expires_at: datetime
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
