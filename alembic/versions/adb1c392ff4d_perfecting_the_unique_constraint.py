"""perfecting the unique constraint

Revision ID: adb1c392ff4d
Revises: 3b559a3c3c92
Create Date: 2022-11-11 11:18:00.062599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adb1c392ff4d'
down_revision = '3b559a3c3c92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("unique_vehicles_name","vehicles",["name"])


def downgrade() -> None:
    op.drop_constraint("unique_vehicles_name","vehicles")
