"""empty message

Revision ID: c84b6cdc4e99
Revises: a503c0d125e7
Create Date: 2017-09-05 12:27:01.433861

"""

# revision identifiers, used by Alembic.
revision = 'c84b6cdc4e99'
down_revision = 'a503c0d125e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('derivations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['processes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('derivations')
    # ### end Alembic commands ###
