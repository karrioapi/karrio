# PRD: Test Suite Performance, Quality & Coverage Improvement

**Status:** Draft  
**Author:** Dan Prime (assessment)  
**Scope:** `karrio/karrio` — all server tests, SDK tests, connector tests  
**Branch:** `chore/test-suite-assessment`

---

## 1. Problem Statement

The karrio test suite has grown organically across 246 test files totalling ~104,000 lines of test code. While coverage exists for most surfaces, three compounding problems make the suite difficult to work with and too slow to be a tight feedback loop:

1. **Speed** — core server tests take ~72s for 74 tests (~1s/test); proxy tests take ~67s for 8 tests (~8.5s/test). CI server-test runtime is ~10–12 minutes. This slows down every PR and every developer.

2. **Quality** — tests range from well-structured parameterised unit tests to massive 3,000+ line integration blobs where every test method independently re-creates the entire world in `setUp`. Many connector tests only verify serialized XML strings rather than semantic behavior, making them brittle to whitespace changes.

3. **Coverage gaps** — entire critical paths (admin mutation tests, event query tests, order-linked shipment flow) are either commented out or absent. The `admin/tests.py` monolith has 97 test methods across 3,268 lines but none test failure paths or permission boundaries.

---

## 2. Goals

| # | Goal | Success Metric |
|---|------|---------------|
| G1 | Reduce server-test wall-clock time ≥60% | CI passes in <5min on a 4-core runner |
| G2 | Remove or fix all dead/commented-out tests | Zero `# def test_` occurrences in codebase |
| G3 | No test class with setUp that does DB I/O > 3 objects | Measured at PR review |
| G4 | Raise branch coverage on critical paths to ≥80% | Measured via `coverage run --branch` |
| G5 | Connector tests assert semantics, not raw XML strings | All connector tests use typed model comparisons |

---

## 3. Exhaustive Assessment

### 3.1 Speed Root Causes

#### 3.1.1 `setUp` runs for every single test method

Django's default test runner calls `setUp` / `tearDown` around **every** test method. The base `APITestCase` in `modules/core/karrio/server/core/tests/base.py` creates:

- 1 user (password hash bcrypt, ~50ms alone)
- 4 carrier connections

That's ~5 DB writes × n test methods. For `TestShipmentFixture` (39 methods) this means **39 × 5 = 195 DB insertions** just for the shared fixture.

**Fix:** Promote stable, shared objects to `setUpTestData` (class-level, wrapped in a single transaction, rolled back only once per class rather than once per test):

```python
class APITestCase(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(...)
        cls.carrier = providers.CarrierConnection.objects.create(...)
        cls.token = Token.objects.create(user=cls.user, test_mode=True)
    
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
```

`setUpTestData` wraps all class fixtures in a single savepoint — each test method operates in a transaction that is rolled back, leaving the class-level data intact. bcrypt is run once per class.

**Estimated savings:** ~65% reduction in `setUp` DB cost across all 10 server test modules.

#### 3.1.2 Password hashing in every setUp

`create_superuser("admin@example.com", "test")` runs bcrypt on every test. bcrypt is intentionally slow.

**Fix:** Use `set_unusable_password()` or `create_user(password=make_password("test", hasher="md5"))` in tests. Or better: use `django.test.override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])` in test settings.

Current `karrio/server/settings/test.py` does not set `PASSWORD_HASHERS`. Adding it saves 40-60ms per user creation.

#### 3.1.3 Test DB is SQLite — fine, but not in-memory

Tests run against a file-based SQLite DB (`.karrio/db.sqlite3`). Using `':memory:'` removes all disk I/O:

```python
# settings/test.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}
```

File-based SQLite with fsync adds ~5-15ms per transaction. With hundreds of transactions this adds up.

#### 3.1.4 Serial test execution — no parallelism

`bin/run-server-tests` runs 10 test modules serially:

```bash
karrio test karrio.server.core.tests || exit 1
karrio test karrio.server.proxy.tests || exit 1
...
```

These modules are **independent** — they share no test state. They can run in parallel with Django's `--parallel` flag (Python `multiprocessing`):

```bash
karrio test --parallel karrio.server.core.tests karrio.server.proxy.tests karrio.server.manager.tests ...
```

Or using `pytest-xdist` if migrating to pytest:

```bash
pytest -n auto modules/
```

**Estimated savings:** On a 4-core CI runner, 4× theoretical speedup for independent modules.

#### 3.1.5 `GraphTestCase.setUp` conditionally creates Organization

Every GraphQL test conditionally creates an `Organization` + `TokenLink` when `MULTI_ORGANIZATIONS=True`. In the insiders test environment this fires 2 additional DB writes per test method × ~200 graph test methods = 400 extra inserts.

**Fix:** Promote to `setUpTestData` at class level.

#### 3.1.6 Proxy tests — 8 tests at ~67s = ~8.4s each

Each proxy test patches `karrio.server.core.gateway.utils.identity` and posts to a live Django test client. The extreme slowness (~8.4s/test) suggests the Django app is being re-initialized per test module or the carrier resolver is doing expensive work on first request.

Profile with: `python -m cProfile -s cumulative -m karrio test karrio.server.proxy.tests`

Likely cause: first request triggers `AppConfig.ready()` signal registration or carrier plugin discovery on each test DB. Consider using `--keepdb` for repeated local runs.

---

### 3.2 Dead / Commented-Out Tests

| File | Lines | Issue |
|------|-------|-------|
| `modules/events/karrio/server/events/tests/test_events.py` | 20 | `test_query_events` is commented out — only `test_query_event` (singular) runs |
| `modules/orders/karrio/server/orders/tests/test_orders.py` | 130 | `test_linked_shipment` is commented out — the order→shipment link is completely untested |
| `community/plugins/locate2u/tests/locate2u/test_shipment.py` | 30 | `test_create_shipment` commented out — create path has no coverage |

**Action:** Uncomment and fix all 3. If they cannot be fixed due to missing feature, delete the comment and add a `@unittest.skip("reason")` decorator with a linked issue.

---

### 3.3 Redundant / Low-Value Tests

#### 3.3.1 Connector XML snapshot tests

The pattern across almost all 100+ connector test files:

```python
def test_create_rate_request(self):
    request = gateway.mapper.create_rate_request(self.RateRequest)
    self.assertEqual(
        re.sub(r"\s+", " ", request.serialize()),
        re.sub(r"\s+", " ", EXPECTED_XML_BLOB)
    )
```

These tests assert that an XML/JSON *string* exactly matches a hardcoded blob that is hundreds of lines long. Problems:

1. **They break on any format change** (whitespace, field order) even when semantics are identical
2. **They don't test behavior** — they test that the mapper produces a known string, not that the produced request contains correct semantics (shipper address, correct service code, correct weight unit)
3. **They provide false confidence** — a test that passes only because the expected string matches the actual string tells you nothing about whether a parcel's `weight_unit` was correctly mapped to "KGS" vs "LBS" in a new carrier

**Better pattern:**

```python
def test_create_rate_request_weight_unit(self):
    request = gateway.mapper.create_rate_request(self.RateRequest)
    parsed = xmltodict.parse(request.serialize())
    self.assertEqual(
        parsed["RatingServiceSelectionRequest"]["Shipment"]["Package"]["PackageWeight"]["UnitOfMeasurement"]["Code"],
        "KGS"
    )
```

Or for JSON carriers, use typed `dataclasses` deserialization. This makes tests **refactor-safe** and **semantically meaningful**.

#### 3.3.2 `admin/tests.py` — 3,268 lines, single file, no failure-path coverage

The admin test monolith has 97 test methods in one file. Every test follows:

```python
def test_create_X(self):
    response = self.query(MUTATION_CREATE_X, {"input": {...}})
    self.assertResponseNoErrors(response)
    self.assertDictEqual(response.data, EXPECTED_DATA)
```

Zero tests for:
- Authentication failure (missing/invalid token)
- Authorization (non-admin calling admin-only mutation)
- Invalid input (missing required field, wrong type)
- Concurrent modification / optimistic locking

Split into `test_admin_carriers.py`, `test_admin_rate_sheets.py`, `test_admin_billing.py`, etc. and add failure paths.

#### 3.3.3 `test_rate_sheets.py` — 3,156 lines, 74 tests, all happy-path

The GraphQL rate sheet test covers CRUD but all tests are happy-path `assertResponseNoErrors`. No test verifies:
- Querying someone else's rate sheet returns 403 / empty result
- Creating a rate sheet with an invalid carrier name returns a meaningful error
- Zone ID collision behavior
- The `SystemRateSheet` vs `AccountRateSheet` routing introduced in 0106

#### 3.3.4 `test_shipments.py` — 1,876 lines but thin on edge cases

Manager shipment tests create a full carrier + user stack in `setUp` then test create/list/retrieve. Missing:
- Purchase failure (carrier rejects)
- Cancel after already cancelled (idempotency)
- Shipment with no matching carrier (should 400, not 500)
- Bulk operations

#### 3.3.5 `test_request_id.py` — 29 tests mostly duplicate middleware behavior

29 tests for `x-request-id` middleware: 12 test the same "request ID is propagated" assertion with different HTTP methods. These can be collapsed to a single parameterized test:

```python
@parameterized.expand(["GET", "POST", "PUT", "DELETE", "PATCH"])
def test_request_id_propagated_for_{method}(self, method):
    ...
```

Reduces 12 tests → 1 parameterized test with the same coverage.

---

### 3.4 Coverage Gaps by Module

| Module | Key missing coverage |
|--------|---------------------|
| `manager` | Shipment purchase failure, bulk cancel, `test_mode=True` isolation, partial parcel data |
| `events` | `test_query_events` (commented out), webhook retry on failure, deduplication |
| `orders` | `test_linked_shipment` (commented out), order with multiple shipments, order status transitions |
| `graph` | Mutation error paths, cross-user data access, SystemRateSheet queries |
| `proxy` | Multi-carrier rate request, partial carrier failure, timeout handling |
| `core/providers` | `SecretManager` — thread-safety under concurrent write, rotation with partial failure |
| `documents` | Template rendering with missing field, template with custom renderer, base64 output |
| `admin` | Permission denied paths, invalid input validation, concurrent edit |
| `ee/automation` | Workflow failure-branch paths, dead-letter behavior, rate-limit hit |

---

### 3.5 Specific Improvements Per Critical Path

#### Shipment lifecycle (manager)
```
create → purchase → cancel
create → purchase → manifest
create → void
create → missing carrier → 400
```
Currently only `create → purchase` is tested.

#### Carrier connection credentials (providers)
```
create with wrong credentials → validation error
rotate encrypted credentials → verify re-decryptable
delete connection → verify orphaned shipments handled
```
Currently only happy-path create is tested in `test_connections.py`.

#### Webhook event delivery (events)
```
event fired → webhook queued → webhook delivered (mocked HTTP)
event fired → webhook fails → retry after backoff
event fired → webhook exceeds retries → marked failed
```
`test_batch_webhooks.py` only tests the queue insertion, not delivery.

#### Rate sheet resolution (graph / proxy)
```
rate sheet present → used for pricing
rate sheet absent → fallback to carrier default
system rate sheet → used for system connections only
account rate sheet → used for account connections
```
`test_rate_sheets.py` has 74 tests but zero tests for pricing resolution.

---

## 4. Implementation Plan

### Phase 1 — Speed wins (1-2 days, no behavior change)

1. Add `PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]` to `karrio/server/settings/test.py`
2. Migrate `APITestCase.setUp` → `setUpTestData` in `modules/core/karrio/server/core/tests/base.py` and `modules/graph/karrio/server/graph/tests/base.py`
3. Set `DATABASES["default"]["NAME"] = ":memory:"` in test settings
4. Switch `bin/run-server-tests` to run all modules in a single `karrio test --parallel` call

**Expected outcome:** 72s core tests → ~15s; total CI server tests ~3-4min.

### Phase 2 — Dead code removal (0.5 days)

1. Uncomment + fix `test_query_events`, `test_linked_shipment`, `test_create_shipment`
2. Replace remaining `# def test_` with `@unittest.skip("tracked in issue #NNN")`
3. Collapse `test_request_id.py` duplicated method-variant tests to `@parameterized.expand`

### Phase 3 — Admin test split (2-3 days)

1. Split `admin/tests.py` into per-resource files
2. Add at minimum one failure-path test per mutation class (auth failure, validation failure)
3. Add permission-boundary tests (regular user calling admin endpoint)

### Phase 4 — Connector test quality (ongoing, per connector)

1. Write a migration guide: XML string → structured semantic assertions
2. Apply to the 5 most-changed connectors first: `dhl_express`, `dhl_parcel_de`, `canadapost`, `fedex`, `ups`
3. Add a linting rule (custom `flake8` check or `pre-commit` hook) that warns when a test asserts against a string > 200 chars

### Phase 5 — Coverage gaps (3-5 days)

Priority order based on production risk:
1. Shipment lifecycle failure paths
2. SystemRateSheet vs AccountRateSheet routing
3. Webhook delivery and retry
4. Order → shipment link
5. SecretManager concurrent rotation

---

## 5. Settings Changes Required

### `karrio/server/settings/test.py`

```python
# Speed up test password hashing dramatically
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# In-memory SQLite — no disk I/O for test DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}

# Suppress celery/async tasks in test environment
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable migration checks during test (use --keepdb for repeated runs)
# MIGRATION_MODULES = {app: None for app in INSTALLED_APPS}  # optional nuclear option
```

---

## 6. `bin/run-server-tests` Rewrite

```bash
#!/usr/bin/env bash
source "bin/activate-env" >/dev/null 2>&1

echo 'run server tests...'

# Run all server modules in one invocation with --parallel
# Django will distribute across CPU cores automatically
karrio test --parallel --failfast \
    karrio.server.core.tests \
    karrio.server.providers.tests \
    karrio.server.proxy.tests \
    karrio.server.pricing.tests \
    karrio.server.manager.tests \
    karrio.server.events.tests \
    karrio.server.graph.tests \
    karrio.server.orders.tests \
    karrio.server.documents.tests \
    karrio.server.admin.tests \
    || exit 1

if [[ "${HAS_INSIDERS}" == "true" && ! "$*" == *--exclude-insiders* ]]; then
    karrio test --parallel --failfast \
        karrio.server.orgs.tests \
        || exit 1
    WORKER_IMMEDIATE_MODE=True karrio test --failfast karrio.server.automation.tests || exit 1
fi

echo -e "\033[0;32mAll server tests completed successfully\033[0m"
```

Note: `automation.tests` must remain serial because `WORKER_IMMEDIATE_MODE=True` is not safe with `--parallel`.

---

## 7. Quick Wins Summary

| Change | Effort | Estimated Speedup |
|--------|--------|-------------------|
| MD5 hasher in test settings | 1 line | ~40ms/user × N tests |
| `setUpTestData` in base test classes | 2h | 60-70% reduction in setUp DB cost |
| In-memory SQLite | 3 lines | 5-15ms/transaction |
| `--parallel` in run-server-tests | 5 lines | ~3-4× on 4-core CI |
| Collapse request_id duplicates | 30min | 12 tests → 1 |
| **Total expected** | **~1 day** | **~75% CI speedup** |

---

## 8. Out of Scope

- E2E / browser tests (Playwright specs) — separate effort
- SDK connector tests (they are fast, unit-only, no DB)
- Load testing / performance benchmarks
- Adding `pytest` as the test runner (migration path exists but not in scope here)

---

## Appendix A — Full Test File Inventory by Module

| Module | Test files | Test methods | Lines |
|--------|-----------|-------------|-------|
| `modules/core` | 6 | 103 | ~2,800 |
| `modules/manager` | 8 | ~120 | ~7,200 |
| `modules/graph` | 8 | ~100 | ~7,500 |
| `modules/admin` | 1 | 97 | 3,268 |
| `modules/events` | 4 | ~30 | ~900 |
| `modules/proxy` | 4 | 8 | ~600 |
| `modules/orders` | 1 | ~12 | ~800 |
| `modules/documents` | 2 | ~15 | ~400 |
| `modules/sdk` | 7 | ~100 | ~2,500 |
| `modules/connectors/*` | 100+ | ~400 | ~50,000 |
| `ee/insiders/orgs` | 7 | ~80 | ~3,000 |
| `ee/insiders/automation` | 7 | ~100 | ~4,500 |
| `community/plugins` | 80+ | ~300 | ~20,000 |

---

## Appendix B — Connector Test Pattern Anti-patterns

**Current pattern (anti-pattern):**
```python
def test_create_shipment_request(self):
    request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
    self.assertEqual(
        re.sub(r"\s+", " ", request.serialize()),
        re.sub(r"\s+", " ", """<?xml version="1.0" encoding="UTF-8"?>
<ShipmentRequest>
  <RequestedShipment>
    <ShipTimestamp>2021-01-01T00:00:00</ShipTimestamp>
    ...300 more lines...
  </RequestedShipment>
</ShipmentRequest>""")
    )
```

**Better pattern:**
```python
def test_shipment_request_has_correct_service_type(self):
    request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
    parsed = xmltodict.parse(request.serialize())
    self.assertEqual(
        parsed["ShipmentRequest"]["RequestedShipment"]["ServiceType"],
        "FEDEX_GROUND"
    )

def test_shipment_request_weight_converted_to_lbs(self):
    request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
    parsed = xmltodict.parse(request.serialize())
    weight = parsed["ShipmentRequest"]["RequestedShipment"]["RequestedPackageLineItems"]["Weight"]
    self.assertEqual(weight["Units"], "LB")
    self.assertAlmostEqual(float(weight["Value"]), 2.205, places=1)  # 1kg → 2.205lb
```

This catches real bugs (wrong unit, wrong service code) rather than formatting changes.
