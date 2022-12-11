"""empty message

Revision ID: ddb66513234b
Revises: f852e31c4753
Create Date: 2022-12-10 18:42:21.224730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddb66513234b'
down_revision = 'f852e31c4753'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipt', schema=None) as batch_op:
        batch_op.drop_index('ix_recipt_total')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipt', schema=None) as batch_op:
        batch_op.create_index('ix_recipt_total', ['total'], unique=False)

    # ### end Alembic commands ###