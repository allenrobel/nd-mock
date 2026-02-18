---
name: gen-test
description: Generate unit tests for nd-mock API endpoints
disable-model-invocation: true
arguments:
  - name: endpoint
    description: Path to the endpoint module to test (e.g., app/v2/endpoints/manage/fabrics/fabric_get.py)
    required: true
---

# Generate Unit Tests

Generate pytest unit tests for the specified endpoint module, following the project's established testing patterns.

## Test Conventions

- Tests use `fastapi.testclient.TestClient` with an in-memory SQLite database
- Import fixtures from `tests/unit/common.py`: `client_fixture`, `session_fixture`
- Test data is loaded from JSON files via a `data_loader.py` and `load_test_data()` helper
- Test function names follow pattern: `test_{version}_{resource}_{method}_{number}` (e.g., `test_v2_fabric_post_100`)
- Each test uses `inspect.currentframe().f_code.co_name` to load its corresponding test data
- Include standard pylint disables at the top of test files

## Steps

1. Read the endpoint module specified in the `endpoint` argument
2. Read the corresponding model(s) used by the endpoint
3. Look at existing tests in `tests/unit/` to match the style exactly
4. Generate test file with:
   - Standard pylint/mypy disable comments
   - Proper relative imports for models and common fixtures
   - A `load_test_data()` helper function
   - Tests for success cases (status 200) and error cases (400, 404, 422)
   - Assertions on `response.status_code` and `response.json()` structure
5. Generate corresponding test data JSON file in a `data/` subdirectory
6. Run `pytest` on the new test file to verify it passes
