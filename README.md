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
