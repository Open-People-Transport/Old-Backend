"""Make RouteStop distance not a primary key

Revision ID: 9ecb9160838d
Revises: 6a20b8fdc1c7
Create Date: 2022-06-25 19:42:36.829681

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9ecb9160838d"
down_revision = "6a20b8fdc1c7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("route_stop_pkey", "route_stop")
    op.create_primary_key("route_stop_pkey", "route_stop", ["route_id", "stop_id"])


def downgrade() -> None:
    op.drop_constraint("route_stop_pkey", "route_stop")
    op.create_primary_key(
        "route_stop_pkey", "route_stop", ["route_id", "stop_id", "distance"]
    )
