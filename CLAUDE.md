# nd-mock

Mock server for Cisco Nexus Dashboard (ND) REST API, used for development and testing of [ansible-nd](https://github.com/CiscoDevNet/ansible-nd) modules without requiring a real ND instance.

## Tech Stack

- **Framework**: FastAPI with uvicorn
- **ORM/Database**: SQLModel + SQLAlchemy with SQLite (`database.db`)
- **Validation**: Pydantic v2
- **Testing**: pytest (unit + integration tests)
- **Container**: Docker/Podman

## Project Structure

```
app/
  app.py          # FastAPI app instance
  db.py           # Database session/engine setup
  main.py         # Router registration (all endpoints wired here)
  common/         # Shared enums, functions, validators
  v1/             # V1 API: endpoints, models, validators
schema/           # JSON schema files (infra.json, manage.json)
tests/
  unit/           # Unit tests
  integration/    # Integration tests (container-based)
docs/             # Documentation
utils/            # Utility scripts (docs_generate.py)
```

## Commands

- **Run server**: `uvicorn app.main:app --reload`
- **Run all tests**: `pytest`
- **Run unit tests**: `pytest tests/unit/`
- **Run integration tests**: `pytest tests/integration/`
- **Type checking**: `mypy app/`

## Code Style

- **Line length**: 180 characters
- **Formatters**: black, isort, pyink (all configured for 180 line length)
- **Linters**: ruff, pylint, flake8
- Ruff ignores: F401 (unused imports — intentional re-exports in `main.py`)
- Follow existing patterns when adding new endpoints: create router module, models, add import + `app.include_router()` in `main.py`

## Adding New Endpoints

1. Create endpoint module in `app/v1/endpoints/` with a `router = APIRouter()`
2. Create corresponding models in `app/v1/models/`
3. Import the endpoint in `app/main.py` and register with `app.include_router()`
4. Add tests in `tests/unit/`
