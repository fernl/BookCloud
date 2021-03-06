"""empty message

Revision ID: fea7f317c6a9
Revises: None
Create Date: 2016-10-13 21:23:49.743680

"""

# revision identifiers, used by Alembic.
revision = 'fea7f317c6a9'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('branch', sa.Column('expiration', sa.DateTime(), nullable=True))
    op.add_column('branch', sa.Column('expires', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('branch', 'expires')
    op.drop_column('branch', 'expiration')
    ### end Alembic commands ###
