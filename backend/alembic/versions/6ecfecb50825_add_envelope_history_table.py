"""Add envelope history table

Revision ID: 6ecfecb50825
Revises: c7e0719b5776
Create Date: 2025-12-29 00:26:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ecfecb50825'
down_revision: Union[str, Sequence[str], None] = 'c7e0719b5776'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('envelope_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('envelope_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('balance_after', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['envelope_id'], ['envelopes.id']),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_envelope_history_created_at'), 'envelope_history', ['created_at'], unique=False)
    op.create_index(op.f('ix_envelope_history_envelope_id'), 'envelope_history', ['envelope_id'], unique=False)
    op.create_index(op.f('ix_envelope_history_id'), 'envelope_history', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_envelope_history_id'), table_name='envelope_history')
    op.drop_index(op.f('ix_envelope_history_envelope_id'), table_name='envelope_history')
    op.drop_index(op.f('ix_envelope_history_created_at'), table_name='envelope_history')
    op.drop_table('envelope_history')
