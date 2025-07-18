"""Ajout de la relation user_id dans MessageContact

Revision ID: 6ca982269d70
Revises: 167925d06aef
Create Date: 2025-07-16 16:32:47.504990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ca982269d70'
down_revision = '167925d06aef'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('messages_contact', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_message', 'utilisateurs', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('messages_contact', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_message', type_='foreignkey')
        batch_op.drop_column('user_id')
