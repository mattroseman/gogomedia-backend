"""add order column to media table

Revision ID: 946b8f7010a9
Revises: 75647cfb1050
Create Date: 2018-03-06 17:16:13.507513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence


# revision identifiers, used by Alembic.
revision = '946b8f7010a9'
down_revision = '75647cfb1050'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(CreateSequence(Sequence('order_seq')))
    order_seq = sa.Sequence('order_seq')
    op.add_column('media', sa.Column('order', sa.Integer, nullable=False, unique=True,
                                     server_default=order_seq.next_value()))

    # TODO handle inserting new element
    # TODO handle updating element consumed state
    # TODO handle deleting element
    # TODO handle moving element within same consumed state


def downgrade():
    op.drop_column('media', 'order')
