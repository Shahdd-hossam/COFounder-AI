# Manus Database Setup and GitHub Transfer

## What was added

| Area | Local files |
|---|---|
| Database settings | `backend/app/core/config.py`, `backend/.env.example` |
| SQLAlchemy session | `backend/app/db/session.py` |
| Models | `backend/app/db/models.py` |
| Repositories | `backend/app/db/repositories.py` |
| Schemas | `backend/app/schemas/startups.py`, `backend/app/schemas/evidence.py` |
| Migrations | `backend/alembic.ini`, `backend/migrations/env.py`, `backend/migrations/versions/0001_create_startups_and_workflows.py` |
| FastAPI endpoints | `backend/app/api/routes/startups.py`, `backend/app/api/routes/workflows.py` |
| Readiness | `GET /health`, `GET /ready` in `backend/app/main.py` |
| React startup flow | `app/src/pages/Home.jsx`, `StartupSetup.jsx`, `StartupOverview.jsx`, `app/src/services/api.js` |
| MCP boundary | `backend/app/integrations/mcp_gateway.py`, `backend/app/services/workflow_service.py` |
| Tests | `tests/test_startups.py`, `app/src/App.test.js` |

## Environment setup

Copy `backend/.env.example` to `backend/.env`. For local development, the default SQLite value is safe:

```env
DATABASE_URL=sqlite:///./cofounder_ai.db
```

For the Manus-managed database, replace this value with the connection string provided by the Manus project runtime and install the matching SQLAlchemy driver. Never commit the real `.env` file.

## Migration

From the `backend` directory:

```bash
alembic upgrade head
```

The local SQLite startup path creates tables automatically for convenience. The Manus-managed production database should use the reviewed Alembic migration instead of relying on startup DDL.

## API checks

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
curl http://127.0.0.1:8000/api/v1/startups
```

The startup API uses the demo owner ID until authentication is added. Replace `owner_id()` in the startup and workflow routes with the project’s authenticated user subject before exposing multiple users.

## Important limitation

This local build contains the integration boundary and SQLite fallback, but it has not been connected to a real Manus database because the database URL and engine were not available in the sandbox. Before production use, configure the actual Manus URL, matching driver, migration environment, and ownership/authentication dependency.

## Transfer

Copy the entire `/home/ubuntu/cofounder-ai-local/` directory into the GitHub repository root. Preserve the directory structure, install frontend/backend dependencies, run the migration, run tests, and review the generated diff before committing.
