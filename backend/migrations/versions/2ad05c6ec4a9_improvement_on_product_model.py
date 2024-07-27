"""improvement on product model

Revision ID: 2ad05c6ec4a9
Revises: c1b4561cc60a
Create Date: 2024-07-06 18:36:01.244600

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2ad05c6ec4a9'
down_revision = 'c1b4561cc60a'
branch_labels = None
depends_on = None


# def upgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('locations',
#     sa.Column('name', sa.String(length=100), nullable=False),
#     sa.Column('address', sa.String(length=100), nullable=True),
#     sa.Column('id', sa.String(length=60), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=True),
#     sa.Column('updated_at', sa.DateTime(), nullable=True),
#     sa.PrimaryKeyConstraint('id')
#     )
def upgrade():
    op.create_table('stocks',
    sa.Column('product_id', sa.String(length=60), nullable=False),
    sa.Column('location_id', sa.String(length=60), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('movement_type', sa.String(length=10), nullable=False),
    sa.Column('quantity_change', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('description', sa.String(length=2048), nullable=True))
        batch_op.add_column(sa.Column('quantity_available', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('sku', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('barcode', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint(None, ['barcode'])
        batch_op.create_unique_constraint(None, ['sku'])
        batch_op.drop_column('unit_price')
        batch_op.drop_column('total_cost')
        batch_op.drop_column('product_name')
        batch_op.drop_column('total_price')
        batch_op.drop_column('product_description')
        batch_op.drop_column('quantity')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_verified')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('product_description', mysql.VARCHAR(length=2048), nullable=True))
        batch_op.add_column(sa.Column('total_price', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('product_name', mysql.VARCHAR(length=120), nullable=False))
        batch_op.add_column(sa.Column('total_cost', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('unit_price', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('barcode')
        batch_op.drop_column('sku')
        batch_op.drop_column('quantity_available')
        batch_op.drop_column('description')
        batch_op.drop_column('name')

    op.drop_table('stocks')
    op.drop_table('locations')
    # ### end Alembic commands ###