# [nights]-backend

GraphQL service + Resident-Advisor scraper for the [nights] app.

## Stack

- Python 3.13
- FastAPI 0.136 (Pydantic v2) + starlette-graphene3 + graphene 3.4
- SQLAlchemy 2.0 (typed `Mapped[]` models, `select()` API)
- psycopg 3 against Postgres
- Typer-based CLI for the scraper
- structlog (JSON in prod, human-readable in dev)
- Ruff + mypy + pytest

## Setup

```bash
cp .env.example .env
# fill in DB credentials and CORS_ALLOWED_ORIGINS
poetry install
make run-service              # http://localhost:5002
```

GraphQL endpoint: `POST /graphql`. The GraphiQL playground at `GET /graphql` and
`/docs` are only enabled when `ENVIRONMENT != production`.

Scrape RA into the DB:

```bash
make retrieve-nights-local    # SQLite (src/database/nightsretrieval.db)
make retrieve-nights-prod     # Postgres (DB_* env vars)
```

## Security posture

- **CORS**: closed by default; set `CORS_ALLOWED_ORIGINS` (comma list) to open it.
- **TrustedHostMiddleware**: enforces `TRUSTED_HOSTS` header allowlist.
- **GraphQL introspection / GraphiQL**: disabled in production via `ENVIRONMENT=production`.
- **DB credentials**: built via `sqlalchemy.URL.create`, never string-interpolated.
- **SQL logging**: off by default (`SQL_ECHO=false`).
- **Generic exception handler**: full stack traces go to the structured log, never to clients.
- **HTTP scraping**: connect+read timeouts and exponential backoff via `requests.Session`.
- **Docker image**: multi-stage, non-root `app` user, `/health` HEALTHCHECK.
- **Postgres dev configs** in `docker/` are LOCAL-ONLY — see [`docker/README.md`](docker/README.md) before reusing.

## Commands

| Command | What it does |
|---|---|
| `make install` | `poetry install` |
| `make run-service` | Start the FastAPI service |
| `make retrieve-nights-local` | Run scraper against SQLite |
| `make retrieve-nights-prod` | Run scraper against Postgres |
| `make lint` | `ruff check` |
| `make format` | `ruff format` + autofix |
| `make typecheck` | `mypy src` |
| `make test` | `pytest tests` |

## Out of scope (follow-ups)

- Authentication: GraphQL endpoint is currently open. Add JWT/OAuth before exposing real user data.
- Per-query depth and complexity limits on GraphQL.
- Rate limiting (e.g. via a sidecar or `slowapi`).
- Test coverage: the `tests/` folder is empty today.
