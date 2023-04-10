"""Init

Revision ID: 933e871c8511
Revises: 
Create Date: 2023-04-10 02:44:06.307468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933e871c8511'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('additional_info', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contact_email'), 'contact', ['email'], unique=True)
    op.create_index(op.f('ix_contact_id'), 'contact', ['id'], unique=False)
    op.create_index(op.f('ix_contact_name'), 'contact', ['name'], unique=False)
    op.create_index(op.f('ix_contact_phone'), 'contact', ['phone'], unique=True)
    op.create_index(op.f('ix_contact_surname'), 'contact', ['surname'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contact_surname'), table_name='contact')
    op.drop_index(op.f('ix_contact_phone'), table_name='contact')
    op.drop_index(op.f('ix_contact_name'), table_name='contact')
    op.drop_index(op.f('ix_contact_id'), table_name='contact')
    op.drop_index(op.f('ix_contact_email'), table_name='contact')
    op.drop_table('contact')
    # ### end Alembic commands ###