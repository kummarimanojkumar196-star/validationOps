# ValidationOps

Agentic triage for CI test failures: fetch logs, classify each failure (real bug / flaky test / infra or bench issue), point to the likely culprit commit, rerun flaky jobs, and ask a human before filing defects.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 (pinned in `.python-version`).

```bash
uv sync
uv run validationops
```
