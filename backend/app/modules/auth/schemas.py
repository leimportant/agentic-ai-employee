from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SendOTPRequest(BaseModel):
    email: EmailStr
    channel: str = "email"  # email | telegram | whatsapp
    destination: Optional[str] = None  # chat_id for telegram, phone for whatsapp. If email, uses email field.


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    is_new_user: bool = False


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    is_verified: bool
    tenant_id: Optional[str]
