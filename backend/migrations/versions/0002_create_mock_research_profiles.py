"""create mock research profiles

Revision ID: 0002_mock_research_profiles
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_mock_research_profiles"
down_revision: Union[str, None] = "0001_startups_workflows"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mock_research_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("profile_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("keywords_json", sa.JSON(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_key"),
    )
    op.create_index("ix_mock_research_profiles_profile_key", "mock_research_profiles", ["profile_key"])


def downgrade() -> None:
    op.drop_index("ix_mock_research_profiles_profile_key", table_name="mock_research_profiles")
    op.drop_table("mock_research_profiles")
