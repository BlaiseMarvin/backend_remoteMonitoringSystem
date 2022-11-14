"""fixing bugs

Revision ID: c60f8e24c928
Revises: adb1c392ff4d
Create Date: 2022-11-14 07:32:29.926085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c60f8e24c928'
down_revision = 'adb1c392ff4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('data','owner_id',nullable=False,existing_type=sa.Integer())


def downgrade() -> None:
    op.alter_column('data','owner_id',nullable=True,existing_type=sa.Integer())
