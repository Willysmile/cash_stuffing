"""remove_envelope_id_from_transactions

Revision ID: b64ff962d40b
Revises: 537e51ceed15
Create Date: 2025-12-28 23:32:25.377956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b64ff962d40b'
down_revision: Union[str, Sequence[str], None] = '537e51ceed15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Retirer la colonne envelope_id de la table transactions
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_column('envelope_id')


def downgrade() -> None:
    """Downgrade schema."""
    # Réajouter la colonne envelope_id
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('envelope_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_transactions_envelope_id', 'envelopes', ['envelope_id'], ['id'], ondelete='SET NULL')
        batch_op.create_index('ix_transactions_envelope_id', ['envelope_id'])
