"""empty message

Revision ID: cad8d96e718a
Revises: f6a76200c12a
Create Date: 2022-12-10 15:02:57.544699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cad8d96e718a'
down_revision = 'f6a76200c12a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.String(length=60), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipt', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
