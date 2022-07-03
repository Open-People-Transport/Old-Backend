"""Enable PostGIS

Revision ID: c62ab13a7632
Revises: 9ecb9160838d
Create Date: 2022-06-29 14:36:12.628799

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c62ab13a7632"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS (as of 3.0 contains just geometry/geography)
    op.execute("CREATE EXTENSION postgis;")


def downgrade() -> None:
    op.execute("DROP EXTENSION postgis;")
