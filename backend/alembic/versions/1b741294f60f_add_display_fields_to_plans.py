"""add display fields to plans

Revision ID: 1b741294f60f
Revises: ebe5a0ea350a
Create Date: 2026-06-19 10:35:13.366896
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b741294f60f'
down_revision: Union[str, None] = 'ebe5a0ea350a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('plans', sa.Column('description', sa.String(), nullable=True))
    op.add_column('plans', sa.Column('features', sa.JSON(), nullable=True))
    op.add_column('plans', sa.Column('is_popular', sa.Boolean(), nullable=True))
    op.add_column('plans', sa.Column('cta_text', sa.String(), nullable=True))
    op.add_column('plans', sa.Column('sort_order', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('plans', 'sort_order')
    op.drop_column('plans', 'cta_text')
    op.drop_column('plans', 'is_popular')
    op.drop_column('plans', 'features')
    op.drop_column('plans', 'description')
