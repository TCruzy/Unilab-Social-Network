"""Initial migration.

Revision ID: 7822de8d307a
Revises: 
Create Date: 2022-09-01 21:05:42.597216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7822de8d307a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('post_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'post_date')
    # ### end Alembic commands ###
