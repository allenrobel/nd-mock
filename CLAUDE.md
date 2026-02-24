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

## ND API Reference

### Object Model

- [docs/nd-object-hierarchy.md](docs/nd-object-hierarchy.md) — Nexus Dashboard object hierarchy, relationships, and constraints (Fabric Group > Fabric > VRF > Network > Switch > Interface)

### API Behavior (Real ND 4.2 Observed Behavior)

Reference these documents when implementing mock endpoints to ensure fidelity with real ND. Each file covers standard error format, HTTP status codes, and object-specific behaviors:

- [docs/nd-api-behavior-fabric.md](docs/nd-api-behavior-fabric.md) — Fabric operations (create, delete, list)
- [docs/nd-api-behavior-switch.md](docs/nd-api-behavior-switch.md) — Switch operations (add, discover, role changes)
- [docs/nd-api-behavior-vrf.md](docs/nd-api-behavior-vrf.md) — VRF operations (create, attach/detach, query)
- [docs/nd-api-behavior-network.md](docs/nd-api-behavior-network.md) — Network operations (coming soon)
- [docs/nd-api-behavior-interface.md](docs/nd-api-behavior-interface.md) — Interface operations (coming soon)
