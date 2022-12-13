"""empty message

Revision ID: 14531698fd7f
Revises: 8eb932257659
Create Date: 2022-12-13 08:50:19.452227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14531698fd7f'
down_revision = '8eb932257659'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Integer(), nullable=True))
        batch_op.drop_column('satus')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('satus', sa.INTEGER(), nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
