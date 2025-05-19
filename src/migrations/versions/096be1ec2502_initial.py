"""initial

Revision ID: 096be1ec2502
Revises: 
Create Date: 2025-05-19 17:12:11.683157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '096be1ec2502'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'agencies',
        sa.Column('agency_name', sa.String(50), nullable=False, primary_key=True),
    )

    op.create_table(
        'projects',
        sa.Column('project_name', sa.String(50), nullable=False, primary_key=True),
        sa.Column('corresponding_agency', sa.String(50), sa.ForeignKey('agencies.agency_name'), nullable=False),
    )

def downgrade():
    op.drop_table('projects')
    op.drop_table('agencies')
