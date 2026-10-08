"""baseline user table

Revision ID: b7e1a4c2d9f0
Revises:
Create Date: 2026-10-08 16:38:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "b7e1a4c2d9f0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_status_enum = postgresql.ENUM("active", "guest", name="user_status_enum", create_type=False)


def upgrade() -> None:
    user_status_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True, unique=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=80), nullable=True),
        sa.Column("last_name", sa.String(length=80), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(length=16), nullable=True),
        sa.Column("avatar_url", sa.String(length=2048), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=15), nullable=True),
        sa.Column("status", user_status_enum, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
    user_status_enum.drop(op.get_bind(), checkfirst=True)
