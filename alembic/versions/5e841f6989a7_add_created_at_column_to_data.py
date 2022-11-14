"""add created_at column to data

Revision ID: 5e841f6989a7
Revises: c60f8e24c928
Create Date: 2022-11-14 07:39:17.348320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e841f6989a7'
down_revision = 'c60f8e24c928'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('data',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')
    ))


def downgrade() -> None:
    op.drop_column('data','created_at')
