"""empty message

Revision ID: f4b84bcf493c
Revises: 81e14ea96bf3
Create Date: 2017-03-14 17:20:28.827296

"""

# revision identifiers, used by Alembic.
revision = 'f4b84bcf493c'
down_revision = '81e14ea96bf3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #Step 1" Create Table Permissions
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('dataset_id', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('can_read', sa.Boolean(), nullable=True),
    sa.Column('can_interact', sa.Boolean(), nullable=True),
    sa.Column('can_fork', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    #Step 2: Migrate data (collection id and user id) from collections to permissions
    permissions = sa.sql.table('permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('dataset_id', sa.Integer(), nullable=True),
        sa.Column('collection_id', sa.Integer(), nullable=True),
        sa.Column('can_read', sa.Boolean(), nullable=True),
        sa.Column('can_interact', sa.Boolean(), nullable=True),
        sa.Column('can_fork', sa.Boolean(), nullable=True),
    )
    conn = op.get_bind()
    res = conn.execute("SELECT id, user_id FROM collections")
    results = res.fetchall()
    collection_permissions = [{'collection_id':r[0], 'owner_id':r[1], 'can_read':True, 'can_interact':True, 'can_fork':False} for r in results]
    op.bulk_insert(permissions, collection_permissions)
    
    # Step 3 : Drop column user_id
    naming_convention = {
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    with op.batch_alter_table('collections', naming_convention=naming_convention, schema=None) as batch_op:
        batch_op.drop_constraint("fk_collections_user_id_users", type_='foreignkey')
        batch_op.drop_column('user_id')


    res = conn.execute("SELECT user_id, dataset_id, owner FROM accesses")
    results = res.fetchall()
    dataset_permissions = []
    for r in results:
        if r[2]:
            perm = {'dataset_id': r[1], 'owner_id':r[0], 'can_read':True, 'can_interact':True, 'can_fork':False}
            dataset_permissions.append(perm)
    op.bulk_insert(permissions, dataset_permissions)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Step 1 : Create Column user_id in collections
    naming_convention = {
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    with op.batch_alter_table('collections', naming_convention=naming_convention, schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key("fk_collections_user_id_users", 'users', ['user_id'], ['id'])
    #Step 2 Migrate Data back to collections
    conn = op.get_bind()
    res = conn.execute("SELECT collection_id, owner_id FROM permissions WHERE collection_id IS NOT NULL")
    results = res.fetchall()
    for r in results:
        conn.execute("UPDATE collections SET user_id={} WHERE id={}".format(r[1], r[0]))
    # Step 3 : Drop table Permissions
    op.drop_table('permissions')
    # ### end Alembic commands ###