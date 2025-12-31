"""merge_migration_branches

Revision ID: 86625607d7cf
Revises: 6ecfecb50825, b64ff962d40b
Create Date: 2025-12-30 23:43:17.761301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86625607d7cf'
down_revision: Union[str, Sequence[str], None] = ('6ecfecb50825', 'b64ff962d40b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
