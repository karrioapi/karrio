# Testing Guidelines

## Commands

```bash
source bin/activate-env

# SDK + all connectors
./bin/run-sdk-tests

# Single carrier
python -m unittest discover -v -f modules/connectors/<carrier>/tests

# Server (Django)
./bin/run-server-tests

# Single Django module
karrio test --failfast karrio.server.<module>.tests
```

## Key Rules
- Always run tests from the repository root
- Always match existing test coding style
- We do NOT use pytest anywhere — `unittest` for SDK, `karrio test` (Django) for server
- Test files: `test_<feature>.py` with classes `Test<Module><Feature>`

## Carrier Integration Tests (4-method pattern)
1. `test_create_<feature>_request` — unified model → carrier request
2. `test_<get_feature>` — proxy URL/method verification
3. `test_parse_<feature>_response` — carrier response → unified model
4. `test_parse_error_response` — error handling

## Django Test Pattern
- Debug: add `print(response.data)` BEFORE assertions, remove when tests pass
- Create objects via API requests, not direct model manipulation
- Use `self.assertResponseNoErrors(response)` first
- Single comprehensive assertion: `self.assertDictEqual` with full response
- Use `mock.ANY` for dynamic fields (id, created_at, updated_at)

## Fixture Pattern
- Module-level constants: `Payload`, `RequestData`, `Response`, `ParsedResponse`, `ErrorResponse`
- `cached_auth` dict for OAuth carriers
- `gateway` instance in `fixture.py`
