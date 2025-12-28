"""make_envelope_bank_account_nullable

Revision ID: c7e0719b5776
Revises: b64ff962d40b
Create Date: 2025-12-28 23:40:53.507012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7e0719b5776'
down_revision: Union[str, Sequence[str], None] = 'b64ff962d40b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rendre bank_account_id nullable pour permettre les enveloppes en espèces
    with op.batch_alter_table('envelopes', schema=None) as batch_op:
        batch_op.alter_column('bank_account_id',
                              existing_type=sa.Integer(),
                              nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Remettre bank_account_id non-nullable
    with op.batch_alter_table('envelopes', schema=None) as batch_op:
        batch_op.alter_column('bank_account_id',
                              existing_type=sa.Integer(),
                              nullable=False)
