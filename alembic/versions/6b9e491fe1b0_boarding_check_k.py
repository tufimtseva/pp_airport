"""boarding_check_k

Revision ID: 6b9e491fe1b0
Revises: e20f92587890
Create Date: 2022-11-14 19:26:04.630707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b9e491fe1b0'
down_revision = 'e20f92587890'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('boarding_check_manager_id_fkey', 'boarding_check', type_='foreignkey')
    op.create_foreign_key(None, 'boarding_check', 'client', ['manager_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'boarding_check', type_='foreignkey')
    op.create_foreign_key('boarding_check_manager_id_fkey', 'boarding_check', 'manager', ['manager_id'], ['id'])
    # ### end Alembic commands ###
