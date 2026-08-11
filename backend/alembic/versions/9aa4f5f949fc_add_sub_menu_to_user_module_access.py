"""add sub_menu to user_module_access

Revision ID: 9aa4f5f949fc
Revises: 963326961d1a
Create Date: 2026-06-19 13:28:18.494031
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aa4f5f949fc'
down_revision: Union[str, None] = '963326961d1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_module_access', sa.Column('sub_menu', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('user_module_access', 'sub_menu')
