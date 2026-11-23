"""FastAPI application: the single entry point for all HTTP traffic."""

from fastapi import FastAPI

app = FastAPI(title="ValidationOps", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check. Step 2 adds Postgres and Redis status here."""
    return {"status": "ok"}
