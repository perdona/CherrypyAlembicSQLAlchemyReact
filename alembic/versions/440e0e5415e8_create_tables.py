"""create tables

Revision ID: 440e0e5415e8
Revises:
Create Date: 2015-12-11 14:59:07.660256

"""

# revision identifiers, used by Alembic.
revision = '440e0e5415e8'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "customer",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('order_count', sa.Integer),
    )

def downgrade():
    op.drop_table('customer')
