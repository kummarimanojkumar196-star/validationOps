"""Readiness checks: can we actually reach Postgres and Redis right now?"""

import psycopg
import redis

from validationops.config import settings


def check_db() -> bool:
    """Return True if a trivial query succeeds against Postgres."""
    try:
        with psycopg.connect(settings.database_url, connect_timeout=2) as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_redis() -> bool:
    """Return True if Redis answers PING."""
    try:
        client = redis.from_url(settings.redis_url, socket_connect_timeout=2)
        return bool(client.ping())
    except Exception:
        return False
