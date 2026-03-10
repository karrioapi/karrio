# Debugging Skill

Efficiently debug Karrio issues across the SDK, server, and carrier connectors.

## Request Lifecycle

Understanding the flow is critical for knowing WHERE to debug:

```
HTTP Request → API Layer → Gateway → Mapper → Proxy → Carrier API
                                       ↓
HTTP Response ← API Layer ← Gateway ← Provider ← Carrier Response
```

### Layer-by-Layer

| Layer | Location | What it does |
|-------|----------|-------------|
| API | `apps/api/karrio/server/` | Receives HTTP, validates via DRF serializers |
| Gateway | `karrio.server.core.gateway` | Routes to correct carrier module |
| Mapper | `modules/connectors/<carrier>/karrio/mappers/<carrier>/mapper.py` | Converts unified model → carrier payload |
| Proxy | `modules/connectors/<carrier>/karrio/mappers/<carrier>/proxy.py` | Sends HTTP request to carrier API |
| Provider | `modules/connectors/<carrier>/karrio/providers/<carrier>/` | Parses carrier response → unified model |

## Debugging Commands

### Run Tests

```bash
# Activate environment first
source bin/activate-env

# Single carrier connector tests
python -m unittest discover -v -f modules/connectors/<carrier>/tests

# Single test file
python -m unittest -v modules/connectors/<carrier>/tests/<carrier>/test_tracking

# Single test method
python -m unittest modules.connectors.<carrier>.tests.<carrier>.test_tracking.TestTracking.test_parse_tracking_response

# All SDK tests
./bin/run-sdk-tests

# All server/Django tests
./bin/run-server-tests

# Single Django test module
karrio test --failfast karrio.server.manager.tests

# Type checking
./bin/run-sdk-typecheck
```

### Inspect Carrier Requests

```python
# In a test or REPL, inspect what gets sent to the carrier:
import karrio.sdk as karrio
import karrio.lib as lib

request = gateway.mapper.create_tracking_request(tracking_request)
print(lib.to_dict(request.serialize()))  # See exact carrier payload
```

### Django Test Debugging

When a Django test fails:

1. **Add `print(response)` BEFORE the assertion** to see actual response data
2. **Use `print(response.data)` or `print(response.json())`** for API responses
3. **Remove print statements once tests pass**
4. **Check `self.assertResponseNoErrors(response)` first** before asserting data

```python
def test_create_shipment(self):
    response = self.client.post('/api/shipments', data={...})
    print(response.data)  # DEBUG: see actual response
    self.assertResponseNoErrors(response)
    self.assertDictEqual(response.data, expected)
```

### Common Debugging Patterns

#### `lib.to_dict()` strips None and empty strings
```python
# lib.to_dict({"a": None, "b": "", "c": 0}) → {"c": 0}
# If your test expects None/empty fields, they won't be there
```

#### `lib.failsafe()` swallows exceptions
```python
# Returns None on ANY exception - can hide bugs
result = lib.failsafe(lambda: risky())
# If result is None, temporarily remove failsafe to see the actual error
```

#### `str(None)` returns "None" not None
```python
# Guard with truthy check before str():
value = lib.failsafe(lambda: get_value())
result = str(value) if value else None  # NOT str(value)
```

#### Enum `.find()` returns the enum member
```python
# TrackingStatus.find("BKD") returns the enum member
# .name gives the normalized status string: "pending"
status = provider_units.TrackingStatus.find(code).name
```

#### Generated schema files - never edit directly
```bash
# If a schema type is wrong, fix the source JSON and regenerate:
./bin/run-generate-on modules/connectors/<carrier>
# Source JSON files: modules/connectors/<carrier>/schemas/*.json
```

## Server Debugging

### Start Development Server

```bash
./bin/start          # API (5002) + Worker
./bin/start-server   # API only (port 5002)
./bin/start-worker   # Huey worker only
```

### Docker Development

```bash
./bin/docker-env create    # Build + setup docker dev container
./bin/docker-env shell     # Open shell in container
./bin/docker-env on        # Start stopped container
./bin/docker-env off       # Stop container
./bin/docker-env destroy   # Remove container
./bin/docker-env exec '<cmd>'  # Execute command in container
```

### Database/Migrations

```bash
karrio migrate                     # Run all migrations
karrio migrate --run-syncdb        # Refresh migrations
karrio makemigrations <app_label>  # Create new migration
karrio shell                       # Django shell
```

### Redis/Queue

```bash
redis-cli FLUSHDB     # Clear all queues
redis-cli KEYS '*'    # List all keys
```

## Carrier-Specific Debugging

### Inspect Raw HTTP

Add temporary logging to the proxy:

```python
# In proxy.py, temporarily:
response = lib.request(url=url, data=data, headers=headers, method="POST")
import logging
logging.getLogger(__name__).debug(f"URL: {url}")
logging.getLogger(__name__).debug(f"Request: {data}")
logging.getLogger(__name__).debug(f"Response: {response}")
```

### Test Fixture Mismatch

When `ParsedResponse` doesn't match actual parsing:

1. Run the test with `-v` flag
2. Compare the diff carefully
3. Common issues:
   - `lib.to_dict()` stripped None/empty values from expected
   - Numeric types: `1.0` vs `1` vs `"1"`
   - Date formats: missing timezone, wrong format string
   - Missing `smartkargo_` prefix on meta keys

### HAR File Analysis

Some carriers have HAR files with real API samples:

```bash
# Check for vendor data
ls modules/connectors/<carrier>/vendor/
# HAR files contain real request/response pairs for reference
```
