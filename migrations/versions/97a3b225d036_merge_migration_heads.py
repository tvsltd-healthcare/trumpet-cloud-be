"""Merge migration heads

Revision ID: 97a3b225d036
Revises: fd0833bcfa90, fd52d894f0d6
Create Date: 2025-07-29 13:10:26.883980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97a3b225d036'
down_revision: Union[str, None] = ('fd0833bcfa90', 'fd52d894f0d6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
