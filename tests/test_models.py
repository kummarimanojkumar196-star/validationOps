"""The ORM models define the two tables with the expected columns.

These checks read SQLAlchemy metadata only, so they need no database.
"""

from validationops.db.base import Base
from validationops.db.models import FailureEvent, WebhookDelivery  # noqa: F401


def test_both_tables_registered() -> None:
    assert set(Base.metadata.tables) == {"webhook_deliveries", "failure_events"}


def test_webhook_deliveries_columns() -> None:
    cols = Base.metadata.tables["webhook_deliveries"].columns.keys()
    for name in ["id", "delivery_id", "event_type", "received_at", "payload"]:
        assert name in cols


def test_failure_events_has_the_four_labels() -> None:
    cols = Base.metadata.tables["failure_events"].columns.keys()
    for label in ["component", "job_type", "environment", "layer"]:
        assert label in cols


def test_failure_events_core_columns() -> None:
    cols = Base.metadata.tables["failure_events"].columns.keys()
    for name in ["repo", "run_id", "head_sha", "branch", "conclusion", "status", "tenant_id"]:
        assert name in cols


def test_tenant_id_is_nullable_for_now() -> None:
    assert Base.metadata.tables["failure_events"].columns["tenant_id"].nullable is True
