"""empty message

Revision ID: c7ad6b90e3f1
Revises: 
Create Date: 2021-01-29 17:07:51.686541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ad6b90e3f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('LOG_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('PROJECT_NAME', sa.String(length=255), nullable=False),
    sa.Column('MODULE_NAME', sa.String(length=255), nullable=False),
    sa.Column('ORDER_DATE', sa.Date(), nullable=False),
    sa.Column('DATASET_NAME', sa.String(length=255), nullable=True),
    sa.Column('LOG_MESSAGE', sa.String(length=1024), nullable=True),
    sa.Column('LOG_TYPE', sa.String(length=255), nullable=True),
    sa.Column('INS_COUNT', sa.Integer(), nullable=True),
    sa.Column('UPD_COUNT', sa.Integer(), nullable=True),
    sa.Column('DEL_COUNT', sa.Integer(), nullable=True),
    sa.Column('MERGE_COUNT', sa.Integer(), nullable=True),
    sa.Column('IT_INS_DATE', sa.DateTime(), nullable=True),
    sa.Column('IT_INS_USER', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('LOG_ID')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('confirmations',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('expire_at', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('confirmations')
    op.drop_table('users')
    op.drop_table('logs')
    # ### end Alembic commands ###
