"""create menus table

Revision ID: 3fb4f940cf78
Revises: 9aa4f5f949fc
Create Date: 2026-06-19 13:57:43.956299
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fb4f940cf78'
down_revision: Union[str, None] = '9aa4f5f949fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('menus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tenant_id', sa.UUID(), nullable=True),
    sa.Column('module_key', sa.String(), nullable=True),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('href', sa.String(), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('menus')
