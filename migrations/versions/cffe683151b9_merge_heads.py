"""Merge heads

Revision ID: cffe683151b9
Revises: 2b4b4e818d82, a3766e0d86ac
Create Date: 2025-07-30 19:37:06.564931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cffe683151b9'
down_revision: Union[str, None] = ('2b4b4e818d82', 'a3766e0d86ac')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
