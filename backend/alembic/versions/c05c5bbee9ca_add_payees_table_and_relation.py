"""add_payees_table_and_relation

Revision ID: c05c5bbee9ca
Revises: 56ce580bbb76
Create Date: 2025-12-28 19:41:15.695836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c05c5bbee9ca'
down_revision: Union[str, Sequence[str], None] = '56ce580bbb76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Créer la table payees
    op.create_table('payees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payees_id'), 'payees', ['id'], unique=False)
    op.create_index(op.f('ix_payees_user_id'), 'payees', ['user_id'], unique=False)
    
    # Utiliser batch mode pour SQLite
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payee_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_transactions_payee_id'), ['payee_id'], unique=False)
        batch_op.create_foreign_key('fk_transactions_payee_id', 'payees', ['payee_id'], ['id'], ondelete='SET NULL')
        batch_op.drop_column('payee')


def downgrade() -> None:
    """Downgrade schema."""
    # Utiliser batch mode pour SQLite
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payee', sa.VARCHAR(length=100), nullable=True))
        batch_op.drop_constraint('fk_transactions_payee_id', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_transactions_payee_id'))
        batch_op.drop_column('payee_id')
    
    op.drop_index(op.f('ix_payees_user_id'), table_name='payees')
    op.drop_index(op.f('ix_payees_id'), table_name='payees')
    op.drop_table('payees')
