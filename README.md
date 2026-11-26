# ValidationOps

Agentic triage for CI test failures: fetch logs, classify each failure (real bug / flaky test / infra or bench issue), point to the likely culprit commit, rerun flaky jobs, and ask a human before filing defects.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 (pinned in `.python-version`).

```bash
uv sync                                                 # create .venv with all dependencies
uv run pytest -v                                        # run the tests
uv run uvicorn validationops.api.main:app --reload      # start the API on http://localhost:8000
curl localhost:8000/health                              # -> {"status":"ok"}
```

Interactive API docs: http://localhost:8000/docs

## Local infrastructure (Step 2)

```bash
cp .env.example .env                 # first time only
docker compose up -d                 # start Postgres and Redis
uv run uvicorn validationops.api.main:app --reload
curl localhost:8000/health           # -> {"status":"ok","db":"ok","redis":"ok"}

docker compose stop redis            # take Redis down
curl -i localhost:8000/health        # -> 503, redis "down"
docker compose up -d                 # bring it back
```

## Database migrations (Step 3)

```bash
docker compose up -d                 # Postgres must be running
uv run alembic upgrade head          # create the tables
uv run alembic current               # show the applied revision

# inspect the tables:
docker compose exec postgres psql -U validationops -c "\dt"
docker compose exec postgres psql -U validationops -c "\d failure_events"
```
