# Skill: Run Tests

Execute the appropriate test suites based on what was changed.

## When to Use

- After implementing a feature or fix
- Before creating a commit or PR
- When validating that changes don't break existing functionality

## Determine What to Test

```bash
git diff --name-only HEAD
git diff --name-only --cached   # staged changes
git diff --name-only main...HEAD  # whole branch vs main
```

## Test Commands by Area

### SDK / Connectors

```bash
source bin/activate-env

# All SDK + connector tests (slow; full coverage)
./bin/run-sdk-tests

# Single carrier (fast; local flow)
python -m unittest discover -v -f modules/connectors/<carrier>/tests

# Single module
python -m unittest discover -v -f modules/sdk/karrio/core/tests
```

### Server Modules (Django)

```bash
# All server tests
./bin/run-server-tests

# Single module (fast, --failfast stops on first error)
karrio test --failfast karrio.server.<module>.tests

# Common modules:
karrio test --failfast karrio.server.graph.tests     # Base GraphQL
karrio test --failfast karrio.server.admin.tests     # Admin GraphQL
karrio test --failfast karrio.server.manager.tests   # Shipments / trackers REST
karrio test --failfast karrio.server.providers.tests # Carrier connections
karrio test --failfast karrio.server.pricing.tests   # Markups / fees
karrio test --failfast karrio.server.orders.tests    # Orders
karrio test --failfast karrio.server.events.tests    # Webhooks / events
karrio test --failfast karrio.server.documents.tests # Documents / labels
karrio test --failfast karrio.server.data.tests      # Imports / exports
```

### Frontend (Dashboard)

```bash
cd apps/dashboard && pnpm test
cd apps/dashboard && pnpm tsc --noEmit   # type-checking only
cd apps/dashboard && pnpm build          # full production build
```

## Decision Table

| Files changed | Command |
|---|---|
| `modules/sdk/` | `./bin/run-sdk-tests` |
| `modules/connectors/<carrier>/` | `python -m unittest discover -v -f modules/connectors/<carrier>/tests` |
| `modules/graph/` | `karrio test --failfast karrio.server.graph.tests` |
| `modules/admin/` | `karrio test --failfast karrio.server.admin.tests` |
| `modules/manager/` | `karrio test --failfast karrio.server.manager.tests` |
| `modules/orders/` | `karrio test --failfast karrio.server.orders.tests` |
| `modules/events/` | `karrio test --failfast karrio.server.events.tests` |
| `modules/documents/` | `karrio test --failfast karrio.server.documents.tests` |
| `modules/core/` | `./bin/run-server-tests` (broad impact) |
| `modules/<new-extension>/` | `karrio test --failfast karrio.server.<name>.tests` (after registering in `bin/run-server-tests`) |
| `apps/dashboard/` | `cd apps/dashboard && pnpm test && pnpm tsc --noEmit` |
| Multiple areas | `./bin/run-sdk-tests && ./bin/run-server-tests` |

## Debugging Failures

1. Add `print(response.data)` (or `print(lib.to_dict(parsed_response))`) before the failing assertion.
2. Run a single test: `karrio test --failfast karrio.server.<module>.tests.<TestClass>.<test_method>`.
3. Check for missing fixtures, seed data, or cached auth.
4. Remove `print` statements once tests pass.

## Tips

- `HUEY["immediate"] = True` in test settings — Huey tasks run synchronously. Don't mock them unless you're testing failure paths.
- `lib.to_dict()` strips `None` and empty strings — expected fixtures shouldn't include them.
- `lib.failsafe()` swallows exceptions — remove it temporarily to see the underlying error during debug.
- `str(None)` is `"None"` (not `None`) — always guard with a truthy check first.
