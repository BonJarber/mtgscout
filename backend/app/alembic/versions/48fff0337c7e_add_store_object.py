"""Add store object

Revision ID: 48fff0337c7e
Revises: 03f6719045b7
Create Date: 2022-08-20 18:01:13.606173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48fff0337c7e'
down_revision = '03f6719045b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('affiliate_code', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_store_affiliate_code'), 'store', ['affiliate_code'], unique=False)
    op.create_index(op.f('ix_store_id'), 'store', ['id'], unique=False)
    op.create_index(op.f('ix_store_name'), 'store', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_store_name'), table_name='store')
    op.drop_index(op.f('ix_store_id'), table_name='store')
    op.drop_index(op.f('ix_store_affiliate_code'), table_name='store')
    op.drop_table('store')
    # ### end Alembic commands ###
