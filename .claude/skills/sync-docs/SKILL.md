---
name: sync-docs
description: Regenerate docs/supported_endpoints.md by running utils/docs_generate.py and verify it matches current endpoint registrations in app/main.py
disable-model-invocation: true
---

`utils/docs_generate.py` requires a running server at `localhost:8000` — it fetches `/openapi.json` to discover endpoints.

Steps:
1. Start the server in the background:
   ```
   PYTHONPATH=. VIRTUAL_ENV= /Users/arobel/repos/nd-mock/.venv/bin/uvicorn app.main:app --port 8000 &>/tmp/uvicorn.log &
   SERVER_PID=$!
   ```
2. Wait for it to be ready (`sleep 2` is sufficient), then run the script:
   ```
   PYTHONPATH=. VIRTUAL_ENV= /Users/arobel/repos/nd-mock/.venv/bin/python utils/docs_generate.py
   ```
3. Stop the server:
   ```
   kill $SERVER_PID
   ```
4. Verify the regenerated `docs/supported_endpoints.md` covers all tag groups and routers registered via `app.include_router()` in `app/main.py`.
