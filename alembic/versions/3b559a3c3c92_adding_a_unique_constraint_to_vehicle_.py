"""adding a unique constraint to vehicle names

Revision ID: 3b559a3c3c92
Revises: 4e6830f5903d
Create Date: 2022-11-11 10:01:52.349460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b559a3c3c92'
down_revision = '4e6830f5903d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('vehicles','name',sa.UniqueConstraint(),existing_type=sa.String(),existing_nullable=False)
    

def downgrade() -> None:
    op.alter_column('vehicles','name',existing_type=sa.String(),existing_nullable=False)
