"""ORM models: the Python classes that map to database tables."""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from validationops.db.base import Base


class WebhookDelivery(Base):
    """One raw webhook as the CI tool sent it. Kept for audit and dedup."""

    __tablename__ = "webhook_deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # GitHub's X-GitHub-Delivery header; unique so we can ignore repeats.
    delivery_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    event_type: Mapped[str] = mapped_column(String(64))
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # The whole payload, stored as JSONB so we can query inside it later.
    payload: Mapped[dict] = mapped_column(JSONB)


class FailureEvent(Base):
    """One failed test run, normalized into our own shape."""

    __tablename__ = "failure_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Where it came from (filled from the webhook payload in Step 5).
    repo: Mapped[str] = mapped_column(String(255), index=True)
    run_id: Mapped[int] = mapped_column(BigInteger, index=True)
    run_attempt: Mapped[int] = mapped_column(Integer, default=1)
    workflow_name: Mapped[str] = mapped_column(String(255))
    head_sha: Mapped[str] = mapped_column(String(64))
    branch: Mapped[str] = mapped_column(String(255))
    conclusion: Mapped[str] = mapped_column(String(32))

    # Our four labels (nullable now; classified in later phases).
    component: Mapped[str | None] = mapped_column(String(64), index=True)
    job_type: Mapped[str | None] = mapped_column(String(32))
    environment: Mapped[str | None] = mapped_column(String(32))
    layer: Mapped[str | None] = mapped_column(String(32))

    # Processing state and multi-tenant placeholder.
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    tenant_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # The same run+attempt must never be stored twice.
    __table_args__ = (UniqueConstraint("repo", "run_id", "run_attempt", name="uq_failure_run"),)
