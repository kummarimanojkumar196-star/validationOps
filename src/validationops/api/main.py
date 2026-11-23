"""FastAPI application: the single entry point for all HTTP traffic."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ValidationOps", version="0.1.0")


class HealthResponse(BaseModel):
    """Shape of the /health reply. Step 2 adds db and redis fields."""

    status: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness check: answers if the process is up and serving requests."""
    return HealthResponse(status="ok")
