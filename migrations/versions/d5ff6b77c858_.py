"""empty message

Revision ID: d5ff6b77c858
Revises: 49952fde9c90
Create Date: 2020-01-27 18:24:18.963889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5ff6b77c858'
down_revision = '49952fde9c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('billing_cycles', 'end_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
    op.alter_column('billing_cycles', 'start_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
    op.alter_column('data_usages', 'from_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
    op.alter_column('data_usages', 'to_date',
               existing_type=sa.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_usages', 'to_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('data_usages', 'from_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('billing_cycles', 'start_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('billing_cycles', 'end_date',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
