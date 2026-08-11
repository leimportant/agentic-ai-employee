import asyncio
import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.config import settings
from app.modules.models.base import Base

# Import ALL models so they register with Base.metadata
from app.modules.models.user import User
from app.modules.models.tenant import Tenant
from app.modules.models.plan import Plan
from app.modules.models.subscription import Subscription
from app.modules.models.invoice import Invoice
from app.modules.models.usage_log import UsageLog
from app.modules.models.otp_code import OtpCode
from app.modules.models.ai_agent import AiAgent
from app.modules.models.customer import Customer
from app.modules.models.conversation import Conversation
from app.modules.models.message import Message
from app.modules.models.knowledge_base import KnowledgeBase
from app.modules.models.kb_document import KbDocument
from app.modules.models.team_invite import TeamInvite
from app.modules.models.notification import Notification
from app.modules.models.app_module import AppModule
from app.modules.models.payment_confirmation import PaymentConfirmation
from app.modules.models.user_module_access import UserModuleAccess
from app.modules.models.menu import Menu

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generate SQL without DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
