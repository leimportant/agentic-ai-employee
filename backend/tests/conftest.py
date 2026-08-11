"""
Pytest configuration and fixtures for the Agentic AI backend tests.

Uses SQLite async (aiosqlite) in-memory database to avoid needing PostgreSQL.
Includes type compilation overrides for PostgreSQL-specific types (UUID, Vector).
"""
import uuid
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db

# --------------------------------------------------------------------------
# Compile PostgreSQL-specific types to SQLite-compatible types
# --------------------------------------------------------------------------
from sqlalchemy.dialects.postgresql import UUID as PGUUID


@compiles(PGUUID, "sqlite")
def compile_pguuid_sqlite(type_, compiler, **kw):
    """Compile PostgreSQL UUID type as VARCHAR(36) for SQLite."""
    return "VARCHAR(36)"


# Handle pgvector Vector type for SQLite
from pgvector.sqlalchemy import Vector


@compiles(Vector, "sqlite")
def compile_vector_sqlite(type_, compiler, **kw):
    """Compile pgvector Vector type as TEXT for SQLite."""
    return "TEXT"


# --------------------------------------------------------------------------
# Import ALL models so they register with Base.metadata
# --------------------------------------------------------------------------
from app.modules.models.user import User
from app.modules.models.tenant import Tenant
from app.modules.models.otp_code import OtpCode
from app.modules.models.ai_agent import AiAgent
from app.modules.models.conversation import Conversation
from app.modules.models.message import Message
from app.modules.models.customer import Customer
from app.modules.models.knowledge_base import KnowledgeBase
from app.modules.models.kb_document import KbDocument
from app.modules.models.plan import Plan
from app.modules.models.subscription import Subscription
from app.modules.models.invoice import Invoice
from app.modules.models.usage_log import UsageLog
from app.modules.models.notification import Notification
from app.modules.models.team_invite import TeamInvite
from app.modules.models.payment_confirmation import PaymentConfirmation
from app.modules.models.app_module import AppModule
from app.modules.models.user_module_access import UserModuleAccess
from app.modules.models.menu import Menu

# --------------------------------------------------------------------------
# SQLite async engine for testing
# --------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

async_session_test = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database for each test function."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_test() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP test client with DB dependency overridden."""
    from app.main import app

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user with tenant in the database."""
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Workspace",
        slug="testuser",
        settings={"active_apps": []},
    )
    db_session.add(tenant)
    await db_session.flush()

    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email="testuser@example.com",
        name="Test User",
        role="owner",
        provider="email",
        is_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
