. Layer diagram
┌──────────────────────────────────────────────────────────────┐
│ tests/ api/ · ui/ · hybrid/ · hard_ui/ (assertions live here only)
├───────────────────────────────┬──────────────────────────────┤
│ pages/ + components/ │ api/ (one client per resource)
│ UI actions + locators │ auth_client, room_client, booking_client
│ no assertions │ returns pydantic models
├───────────────────────────────┴──────────────────────────────┤
│ data/ models (pydantic) · factories (Faker, unique per test)
├──────────────────────────────────────────────────────────────┤
│ core/ base API client (logging, masking, error handling) · logging setup
├──────────────────────────────────────────────────────────────┤
│ config/ settings per env (dev/local/demo) + env vars for secrets
└──────────────────────────────────────────────────────────────┘
fixtures (conftest per layer) wire these together; utils/ = small, tested helpers 4. Folder structure (each folder has one reason to exist)
booker-playwright-framework/
├── config/ settings.py: loads env config + secrets; one place to change environments
├── core/ base_client.py, logging_setup.py: cross-cutting plumbing every layer uses
├── api/ auth_client.py, room_client.py, booking_client.py: one client per API resource
├── pages/ public site + admin pages: what a user can do on each screen
│ └── components/ header, nav, booking form: UI pieces shared across pages
├── data/ models.py (pydantic), factories.py (Faker): valid, unique test data
├── utils/ wait_until/retry, money (Decimal), dates: only after a second use
├── tests/
│ ├── conftest.py root: --env, settings, logging, health check
│ ├── api/ API-only tests (fast, run first in CI)
│ ├── ui/ UI tests (start from API-created data)
│ ├── hybrid/ create via API → verify in UI → clean up via API
│ └── hard_ui/ The Internet patterns
├── docs/ target-notes.md, decisions.md (ADRs)
├── .github/workflows/ ci.yml
├── pytest.ini · requirements.txt · .env.example · README.md 5. Key decisions (ADR summary)

# Decision Why Trade-off accepted

D1 API tests on Playwright APIRequestContext, not requests One tool and one tracing story; the API context can share auth state with browser contexts Less familiar than requests; fewer third-party plugins
D2 pydantic models for request/response bodies Schema validation and typed objects in one step; clear errors when the API changes Extra layer to maintain when the API changes
D3 Factories with Faker, unique values per test Parallel-safe data; no collisions on a shared public demo Harder to reproduce a specific failing value, so log every generated value
D4 Auth token fixture at session scope (per worker) Login once per worker; tokens are read-only for tests A test that logs out or expires the token must use its own session
D5 Fixtures per layer (root / api / ui conftest) Each folder sees only what it needs; matches v1's folder-scoped storage_state lesson More conftest files to navigate
D6 POM + components, assertions only in tests Pages stay reusable for positive and negative tests Some duplication in assertions across tests
D7 Health-check gate before tests (session fixture) A shared public demo can be down; fail fast with one clear message instead of 50 errors Adds a few seconds per run
D8 CI order: lint → API tests → UI smoke (PR); full + cross-browser on schedule Cheapest, fastest signal first; UI only runs if the API works Full UI coverage isn't on every PR
D9 Std-lib logging, configured once, secrets masked No extra dependency; works with pytest's log capture and xdist Less pretty than structured-logging libraries 6. Example data flow: hybrid test
fixture: auth_token (session) → POST auth → token
fixture: room (function) → factory builds RoomModel → room_client.create() → yield room
test: admin UI → open rooms page → expect(room.name visible)
teardown: room_client.delete(room.id) (runs even if the test fails) 7. Risks and mitigations
Risk Mitigation
Public demo is shared and resets data periodically Unique names via factories; never assert on counts of all records; local Docker fallback
Demo down or slow D7 health check; --env local to switch to Docker
Tests leak data when teardown fails Cleanup in yield fixtures; a session-end sweep deletes records with the test-name prefix
Secrets in logs or reports Masking in core/base_client.py; never log auth headers or cookies
Over-engineering Principle 6; every abstraction must be used by at least two tests 8. Open questions to resolve during M1–M2
Auth: cookie or header token? (decides how the API context and browser context share it)
Does the public demo allow creating and deleting rooms freely, or only bookings?
Which flows count as smoke? (proposal: admin login, create room via API, room visible on public site)
