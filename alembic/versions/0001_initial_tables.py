"""initial tables: webhook_deliveries and failure_events

Revision ID: 0001
Revises:
Create Date: 2026-11-26
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# Alembic identifiers.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "webhook_deliveries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("delivery_id", sa.String(length=255), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.UniqueConstraint("delivery_id", name="uq_webhook_delivery_id"),
    )
    op.create_index("ix_webhook_deliveries_delivery_id", "webhook_deliveries", ["delivery_id"])

    op.create_table(
        "failure_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repo", sa.String(length=255), nullable=False),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("run_attempt", sa.Integer(), nullable=False),
        sa.Column("workflow_name", sa.String(length=255), nullable=False),
        sa.Column("head_sha", sa.String(length=64), nullable=False),
        sa.Column("branch", sa.String(length=255), nullable=False),
        sa.Column("conclusion", sa.String(length=32), nullable=False),
        sa.Column("component", sa.String(length=64), nullable=True),
        sa.Column("job_type", sa.String(length=32), nullable=True),
        sa.Column("environment", sa.String(length=32), nullable=True),
        sa.Column("layer", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("repo", "run_id", "run_attempt", name="uq_failure_run"),
    )
    op.create_index("ix_failure_events_repo", "failure_events", ["repo"])
    op.create_index("ix_failure_events_run_id", "failure_events", ["run_id"])
    op.create_index("ix_failure_events_component", "failure_events", ["component"])
    op.create_index("ix_failure_events_status", "failure_events", ["status"])


def downgrade() -> None:
    op.drop_table("failure_events")
    op.drop_table("webhook_deliveries")
