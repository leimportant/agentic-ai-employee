"""
Auth models — re-exported from centralized models package.
Actual model definitions live in app.modules.models.user
"""
from app.modules.models.user import User
from app.modules.models.otp_code import OtpCode

__all__ = ["User", "OtpCode"]
