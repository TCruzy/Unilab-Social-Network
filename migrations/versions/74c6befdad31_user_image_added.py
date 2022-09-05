"""user_image added

Revision ID: 74c6befdad31
Revises: 2c830044b4bb
Create Date: 2022-09-01 22:19:32.952672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74c6befdad31'
down_revision = '2c830044b4bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_image', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_image')
    # ### end Alembic commands ###
