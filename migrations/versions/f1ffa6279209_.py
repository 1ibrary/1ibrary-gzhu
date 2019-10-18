"""empty message

Revision ID: f1ffa6279209
Revises: 
Create Date: 2017-06-20 14:15:02.161113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1ffa6279209'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id_', sa.Integer(), nullable=False),
    sa.Column('xh', sa.String(length=10), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id_')
    )
    op.create_index(op.f('ix_users_xh'), 'users', ['xh'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_xh'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###