"""modify_envelopes_for_savings_goals

Revision ID: 537e51ceed15
Revises: c05c5bbee9ca
Create Date: 2025-12-28 23:28:50.001985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '537e51ceed15'
down_revision: Union[str, Sequence[str], None] = 'c05c5bbee9ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite ne supporte pas ALTER COLUMN, on utilise batch mode
    with op.batch_alter_table('envelopes', schema=None) as batch_op:
        # Renommer monthly_budget en target_amount
        batch_op.alter_column('monthly_budget',
                              new_column_name='target_amount',
                              existing_type=sa.Numeric(10, 2),
                              nullable=False)
        
        # Ajouter description si elle n'existe pas
        batch_op.add_column(sa.Column('description', sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('envelopes', schema=None) as batch_op:
        # Renommer target_amount en monthly_budget
        batch_op.alter_column('target_amount',
                              new_column_name='monthly_budget',
                              existing_type=sa.Numeric(10, 2),
                              nullable=False)
        
        # Supprimer description
        batch_op.drop_column('description')
