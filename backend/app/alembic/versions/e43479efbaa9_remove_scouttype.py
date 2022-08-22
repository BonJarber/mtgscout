"""Remove scouttype

Revision ID: e43479efbaa9
Revises: 3adbd1055494
Create Date: 2022-08-22 06:59:57.438337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e43479efbaa9'
down_revision = '3adbd1055494'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scout', 'scout_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scout', sa.Column('scout_type', postgresql.ENUM('common', 'uncommon', 'rare', 'mythic', name='scouttype'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
