# Testing Guidelines

## Mandatory Testing Rule

Every feature, bug fix, or behavioral change MUST include tests. No PR should be merged without test coverage for the changed behavior.

## Non-Negotiable Code Style Rules

### Imports Always at the Top

**Never import inside a function or test method.** All imports belong at the top of the file.

```python
# ✅ CORRECT — imports at file top
import re
from unittest.mock import patch
from karrio.server.manager.signals import trackers_bulk_updated
from karrio.server.manager.serializers.tracking import bulk_save_trackers

class TestMyFeature(APITestCase):
    def test_something(self):
        ...

# ❌ WRONG — imports inside test methods
class TestMyFeature(APITestCase):
    def test_something(self):
        from unittest.mock import patch          # never
        import re                                # never
```

### Avoid Mocks Except for External Services

Tests should use **real DB objects, real signal dispatch, and real handler execution**. Only mock calls to **external services** — carrier API requests, third-party HTTP calls, Redis/queue tasks.

```python
# ✅ CORRECT — mock only the external task that would hit Redis/network
with patch("karrio.server.events.task_definitions.broadcast_tracking_event") as mock_broadcast:
    trackers_bulk_updated.send(
        sender=models.Tracking,
        changed_trackers=[(tracker, ["status", "updated_at"])],
    )
mock_broadcast.assert_called_once()

# ❌ WRONG — mocking the entire signal or Django machinery
with patch("karrio.server.manager.signals.trackers_bulk_updated") as mock_signal:
    ...
```

## Test Commands

```bash
source bin/activate-env

# SDK + all connectors
./bin/run-sdk-tests

# Single carrier (most common local flow)
python -m unittest discover -v -f modules/connectors/<carrier>/tests

# Server (Django)
./bin/run-server-tests

# Single Django module
karrio test --failfast karrio.server.<module>.tests

# Frontend tests
cd apps/dashboard && pnpm test

# TypeScript type checking
cd apps/dashboard && pnpm tsc --noEmit
```

## Key Rules

- Always run tests from the repository root.
- Always match existing test coding style.
- **NEVER use pytest** — `unittest` for SDK, `karrio test` (Django) for server.
- Test files: `test_<feature>.py` with classes `Test<Module><Feature>`.
- **Always add `print(response.data)` before assertions** when debugging — remove once tests pass.
- **Use `mock.ANY`** for dynamic fields (id, created_at, updated_at).
- **Use `self.maxDiff = None`** in `setUp()` for full diff output.

## SDK Carrier Integration Tests — 4-method Pattern

Every carrier feature requires 4 tests:

1. `test_create_<feature>_request` — unified model → carrier request payload
2. `test_get_<feature>` — proxy URL/method verification (HTTP call inspection)
3. `test_parse_<feature>_response` — carrier response → unified model
4. `test_parse_error_response` — error handling

```python
class TestCarrierFeature(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    @patch("karrio.mappers.<carrier>.proxy.lib.request")
    def test_get_rates(self, mock_request):
        mock_request.return_value = RESPONSE_JSON
        parsed_response, messages = (
            karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
        )
        print(lib.to_dict(parsed_response))  # always print before assert
        self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)
```

## Django Server Test Pattern

- Debug: add `print(response.data)` BEFORE assertions, remove when tests pass.
- Create objects via API requests, not direct model manipulation.
- Use `self.assertResponseNoErrors(response)` first for GraphQL.
- Single comprehensive assertion: `self.assertDictEqual` with full response.

```python
class TestFeatureName(TestCase):
    fixtures = ["fixtures"]  # or specific fixtures

    def test_query_or_mutation(self):
        response = self.query(QUERY_STRING, operation_name="OperationName")
        response_data = response.data

        # print(response_data)  # during debug, remove when passing

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, EXPECTED_RESPONSE)
```

## Fixture Pattern

- Module-level constants in `fixture.py`: `Payload`, `RequestData`, `Response`, `ParsedResponse`, `ErrorResponse`.
- `cached_auth` dict for OAuth carriers.
- `gateway` instance in `fixture.py`.
- `lib.to_dict()` strips `None` and empty strings — expected fixtures shouldn't include them.

## E2E Test Data

- Use `@ngneat/falso` for generating fake test data (names, companies, emails, phones) in frontend E2E tests — never hardcode personal data.
- Keep carrier-functional fields (country codes, zip codes, cities, addresses, weights) as fixed valid values — carrier APIs validate these combinations.

## Migration Testing

- Data migrations: verify data integrity with `RunPython` + reverse code.
- Always test that migration is reversible when possible.
- Test ordering: ensure dependencies are correct.
- `HUEY["immediate"] = True` in test settings — Huey tasks run synchronously.

## What to Test

| Change Type | Required Tests |
|-------------|----------------|
| New GraphQL mutation | `karrio test` with `assertResponseNoErrors` + response validation |
| New REST endpoint | DRF test with status code + response body |
| Model change | Migration test + serializer test |
| Carrier integration | 4-method pattern per feature (rate, ship, track) |
| Bug fix | Regression test proving the fix |
| Hook / extension | Test that hook fires and validates correctly |
