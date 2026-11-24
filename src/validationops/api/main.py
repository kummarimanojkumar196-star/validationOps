"""FastAPI application: the single entry point for all HTTP traffic."""

from fastapi import FastAPI, Response
from pydantic import BaseModel

from validationops.health.checks import check_db, check_redis

app = FastAPI(title="ValidationOps", version="0.1.0")


class HealthResponse(BaseModel):
    """Shape of the /health reply: overall status plus each dependency."""

    status: str
    db: str
    redis: str


@app.get("/health", response_model=HealthResponse)
def health(response: Response) -> HealthResponse:
    """Readiness check: are we up AND able to reach Postgres and Redis?

    Returns 200 when everything is reachable, 503 when any dependency is down,
    so a load balancer can route traffic away from a broken instance.
    """
    db_ok = check_db()
    redis_ok = check_redis()
    all_ok = db_ok and redis_ok

    if not all_ok:
        response.status_code = 503

    return HealthResponse(
        status="ok" if all_ok else "degraded",
        db="ok" if db_ok else "down",
        redis="ok" if redis_ok else "down",
    )
