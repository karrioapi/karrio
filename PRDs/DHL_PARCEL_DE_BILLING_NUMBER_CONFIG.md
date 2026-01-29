# DHL Parcel DE Billing Number Config Migration

<!-- REFACTORING: This PRD covers migration of billing_number from settings to service-specific config -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-22 |
| Status | Implemented |
| Owner | Karrio Team |
| Type | Refactoring |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Technical Design](#technical-design)
7. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
8. [Implementation Plan](#implementation-plan)
9. [Testing Strategy](#testing-strategy)
10. [Risk Assessment](#risk-assessment)
11. [Migration & Rollback](#migration--rollback)
12. [Appendices](#appendices)

---

## Executive Summary

This PRD proposes migrating the `billing_number` field from DHL Parcel DE connection settings to the connection config, enabling service-specific billing number configuration. DHL Parcel DE requires billing numbers per service (e.g., different billing numbers for V01PAK domestic vs V53WPAK international), and the current single `billing_number` field doesn't support this use case.

### Key Architecture Decisions

1. **Service-specific billing via config**: Introduce `service_billing_numbers` as a list of `{service, billing_number}` objects in `ConnectionConfig`
2. **Default fallback**: Add `default_billing_number` in config for backward compatibility and services without explicit mapping
3. **Metadata propagation**: Store resolved `billing_number` in `shipment.meta` during shipment creation for use in pickup operations
4. **Clean migration**: Remove `billing_number` from settings entirely, migrating all existing data to `config.default_billing_number`

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Move billing_number from settings to config | Changes to dhlRetoure billing (stays in options) |
| Service-specific billing number resolution | Billing number format validation |
| Data migration for existing connections | UI changes for config management |
| Update shipment creation to resolve billing | Changes to other DHL carriers |
| Update pickup to read from options/meta | Rate request billing changes |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Config data structure | List of objects | More explicit, easier to validate, follows karrio patterns | 2026-01-22 |
| D2 | Pickup billing source | Read from options.billing_number (from shipment.meta) | Pickups should use the same billing number as the shipment | 2026-01-22 |
| D3 | Deprecation approach | Clean migration | Simpler codebase, no legacy support burden | 2026-01-22 |
| D4 | dhlRetoure billing | Keep separate in options | Returns may use different billing numbers | 2026-01-22 |

---

## Problem Statement

### Current State

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py
class Settings(core.Settings):
    """DHL Parcel DE connection settings."""

    username: str
    password: str
    client_id: str
    client_secret: str
    billing_number: str = None  # Single billing number for all services

# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py
dhl_parcel_de.ShipmentType(
    product=service,
    billingNumber=settings.billing_number,  # Always uses single billing number
    ...
)
```

### Desired State

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py
class ConnectionConfig(lib.Enum):
    # ... existing config options ...
    default_billing_number = lib.OptionEnum("default_billing_number")
    service_billing_numbers = lib.OptionEnum("service_billing_numbers", list)
    # Format: [{"service": "dhl_parcel_de_paket", "billing_number": "123"}, ...]

# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py
class Settings(core.Settings):
    # billing_number REMOVED from settings

    def get_billing_number(self, service_code: str) -> str:
        """Resolve billing number for a service with fallback to default."""
        service_billing = next(
            (item for item in self.connection_config.service_billing_numbers.state or []
             if item.get("service") == service_code),
            None
        )
        return (
            service_billing.get("billing_number") if service_billing
            else self.connection_config.default_billing_number.state
        )

# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py
billing_number = settings.get_billing_number(service)
# ... later store in response meta for pickup use ...
```

### Problems

1. **Single billing number limitation**: DHL Parcel DE users often have different billing numbers per service (domestic vs international), but can only configure one
2. **No service-specific billing**: The current implementation applies the same billing number to all shipments regardless of service type
3. **Pickup billing inconsistency**: Pickup operations can't easily access the billing number used during shipment creation

---

## Goals & Success Criteria

### Goals

1. Enable users to configure billing numbers per DHL Parcel DE service
2. Maintain backward compatibility by supporting a default billing number
3. Propagate billing number through shipment lifecycle (creation → meta → pickup)
4. Migrate all existing connection data without manual intervention

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| All existing connections migrated | 100% | Must-have |
| SDK tests pass | 100% | Must-have |
| Server tests pass | 100% | Must-have |
| Service-specific billing resolution | Working | Must-have |
| Pickup uses shipment billing number | Working | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] billing_number removed from Settings class
- [ ] ConnectionConfig includes default_billing_number and service_billing_numbers
- [ ] Shipment creation resolves billing per service
- [ ] Shipment meta stores resolved billing_number
- [ ] Pickup reads billing_number from options
- [ ] Data migration for existing connections
- [ ] All SDK tests pass
- [ ] All server tests pass

**Nice-to-have (P1):**
- [ ] Dashboard UI for configuring service billing numbers
- [ ] Validation of billing number format (14 digits)

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: Service billing in config (list)** | Explicit, validates service codes, follows patterns | More verbose JSON | **Selected** |
| B: Service billing in config (dict) | Compact JSON, simple lookup | Less explicit, no service validation | Rejected |
| C: Keep billing_number in settings + config override | Backward compatible | Confusing dual sources, maintenance burden | Rejected |
| D: Billing number per shipment request | Maximum flexibility | Breaks abstraction, requires API changes | Rejected |

### Trade-off Analysis

Option A was selected because:
- **Explicit service names**: List of objects with `{service, billing_number}` makes configuration clear
- **Validation opportunity**: Can validate service codes against `ShippingService` enum
- **Consistent pattern**: Matches how `shipping_options` and `shipping_services` are structured in other connectors
- **Extensibility**: Easy to add more fields per service mapping in the future (e.g., `{service, billing_number, participation_number}`)

---

## Technical Design

> **IMPORTANT**: Study existing patterns in other connectors (FedEx, UPS) for connection_config usage.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| ConnectionConfig pattern | `modules/connectors/ups/karrio/providers/ups/units.py:117-123` | Follow same lib.OptionEnum pattern |
| connection_config property | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py:60-66` | Extend existing implementation |
| Shipment meta propagation | `modules/manager/karrio/server/manager/serializers/shipment.py:201-206` | Use existing meta merge pattern |
| Pickup options from shipment | `modules/manager/karrio/server/manager/serializers/pickup.py:129-158` | Add billing_number to options |
| Server migrations | `modules/core/karrio/server/providers/migrations/` | Follow existing migration patterns |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CONNECTION CONFIGURATION                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                                                         │
│  │ CarrierConnection│                                                        │
│  │   (Database)     │                                                        │
│  ├─────────────────┤                                                         │
│  │ config: JSON     │ ─────────────────────────────────────────────┐        │
│  │ {                │                                               │        │
│  │   "default_billing_number": "123...",                           │        │
│  │   "service_billing_numbers": [                                  │        │
│  │     {"service": "dhl_parcel_de_paket", "billing_number": "A"},  │        │
│  │     {"service": "dhl_parcel_de_europaket", "billing_number": "B"}        │
│  │   ]                                                              │        │
│  │ }                │                                               │        │
│  └─────────────────┘                                               │        │
│                                                                     ▼        │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐        │
│  │    Settings     │────>│ ConnectionConfig │────>│ get_billing_   │        │
│  │  (SDK Runtime)  │     │   (Parsed)       │     │ number(service)│        │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client │     │ Server │     │ Mapper  │     │ Provider│     │DHL API  │
└───┬────┘     └───┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
    │              │               │               │               │
    │ 1. Create    │               │               │               │
    │ Shipment     │               │               │               │
    │─────────────>│               │               │               │
    │              │ 2. Load       │               │               │
    │              │ Settings      │               │               │
    │              │──────────────>│               │               │
    │              │               │ 3. Resolve    │               │
    │              │               │ billing_number│               │
    │              │               │ for service   │               │
    │              │               │──────────────>│               │
    │              │               │               │ 4. Build      │
    │              │               │               │ request       │
    │              │               │               │──────────────>│
    │              │               │               │               │
    │              │               │               │<──────────────│
    │              │               │               │ 5. Response   │
    │              │               │<──────────────│               │
    │              │ 6. Store      │               │               │
    │              │ billing_number│               │               │
    │              │ in meta       │               │               │
    │              │<──────────────│               │               │
    │<─────────────│               │               │               │
    │ 7. Shipment  │               │               │               │
    │ with meta    │               │               │               │
    │              │               │               │               │
    │ 8. Schedule  │               │               │               │
    │ Pickup       │               │               │               │
    │─────────────>│               │               │               │
    │              │ 9. Extract    │               │               │
    │              │ billing_number│               │               │
    │              │ from shipment │               │               │
    │              │ meta to opts  │               │               │
    │              │──────────────>│               │               │
    │              │               │ 10. Read from │               │
    │              │               │ options       │               │
    │              │               │──────────────>│               │
    │              │               │               │──────────────>│
    │              │               │               │               │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           SHIPMENT CREATION FLOW                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────────────────┐│
│  │ Shipment     │───>│ Settings.get_    │───>│ ConnectionConfig             ││
│  │ Request      │    │ billing_number() │    │ ├─ default_billing_number    ││
│  │ {service:    │    │                  │    │ └─ service_billing_numbers[] ││
│  │  "V01PAK"}   │    └──────────────────┘    └──────────────────────────────┘│
│  └──────────────┘              │                                              │
│                                ▼                                              │
│                    ┌──────────────────┐                                       │
│                    │ Resolved:        │                                       │
│                    │ billing_number   │                                       │
│                    │ = "33333333330102"│                                      │
│                    └──────────────────┘                                       │
│                                │                                              │
│          ┌─────────────────────┼─────────────────────┐                       │
│          ▼                     ▼                     ▼                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │ DHL API      │    │ Shipment     │    │ shipment.meta│                   │
│  │ Request      │    │ Response     │    │ {billing_    │                   │
│  │ billingNumber│    │              │    │  number: ... │                   │
│  └──────────────┘    └──────────────┘    │ }            │                   │
│                                          └──────────────┘                   │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                            PICKUP SCHEDULING FLOW                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐               │
│  │ Pickup       │───>│ Server extracts  │───>│ Pickup       │               │
│  │ Request      │    │ billing_number   │    │ options      │               │
│  │ {shipments}  │    │ from shipment.   │    │ {billing_    │               │
│  │              │    │ meta             │    │  number: ...}│               │
│  └──────────────┘    └──────────────────┘    └──────────────┘               │
│                                                      │                       │
│                                                      ▼                       │
│                                          ┌──────────────────┐               │
│                                          │ DHL Pickup API   │               │
│                                          │ billingNumber    │               │
│                                          └──────────────────┘               │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### SDK Changes (ConnectionConfig)

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py

class ConnectionConfig(lib.Enum):
    profile = lib.OptionEnum("profile")
    cost_center = lib.OptionEnum("cost_center")
    creation_software = lib.OptionEnum("creation_software")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    language = lib.OptionEnum(
        "language",
        lib.units.create_enum("Language", ["de", "en"]),
    )
    label_type = lib.OptionEnum(
        "label_type",
        lib.units.create_enum("LabelType", [_.name for _ in LabelType]),
    )
    # NEW: Billing number configuration
    default_billing_number = lib.OptionEnum("default_billing_number")
    service_billing_numbers = lib.OptionEnum("service_billing_numbers", list)
```

#### SDK Changes (Settings)

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py

class Settings(core.Settings):
    """DHL Parcel DE connection settings."""

    username: str
    password: str
    client_id: str
    client_secret: str
    # REMOVED: billing_number: str = None

    account_country_code: str = "DE"

    # ... existing properties ...

    def get_billing_number(self, service_code: str = None) -> typing.Optional[str]:
        """Resolve billing number for a service with fallback to default.

        Args:
            service_code: The karrio service code (e.g., "dhl_parcel_de_paket")

        Returns:
            The billing number for the service, or default if not found
        """
        service_billing_numbers = self.connection_config.service_billing_numbers.state or []

        if service_code:
            service_billing = next(
                (
                    item for item in service_billing_numbers
                    if item.get("service") == service_code
                ),
                None,
            )
            if service_billing:
                return service_billing.get("billing_number")

        return self.connection_config.default_billing_number.state
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_billing_number` | string | No | Fallback billing number for all services |
| `service_billing_numbers` | list | No | List of service-specific billing numbers |
| `service_billing_numbers[].service` | string | Yes | Karrio service code (e.g., `dhl_parcel_de_paket`) |
| `service_billing_numbers[].billing_number` | string | Yes | Billing number for that service |

### Config JSON Example

```json
{
  "default_billing_number": "33333333330102",
  "service_billing_numbers": [
    {
      "service": "dhl_parcel_de_paket",
      "billing_number": "33333333330102"
    },
    {
      "service": "dhl_parcel_de_europaket",
      "billing_number": "33333333330201"
    },
    {
      "service": "dhl_parcel_de_paket_international",
      "billing_number": "33333333330301"
    }
  ]
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| No billing number configured | Return None, API will reject | Let DHL API return error message |
| Service not in service_billing_numbers | Fall back to default_billing_number | Handled in `get_billing_number()` |
| Empty service_billing_numbers list | Use default_billing_number | Handled in `get_billing_number()` |
| Neither default nor service billing set | Return None | DHL API will return validation error |
| Pickup without associated shipment | Use default_billing_number | Fall back when no meta available |
| Multiple shipments in pickup (different billing) | Use first shipment's billing | Document this behavior |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Migration fails mid-way | Partial data migration | Transaction wrapping, dry-run option |
| Invalid billing number format | DHL API rejection | Clear error message from API |
| Shipment.meta not saved | Pickup uses wrong billing | Ensure meta is always saved |
| Config JSON malformed | Settings parse failure | Validate config structure |

---

## Implementation Plan

### Phase 1: SDK Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add billing config to ConnectionConfig | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py` | Pending | S |
| Add get_billing_number() method to Settings | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py` | Pending | S |
| Remove billing_number from Settings | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py` | Pending | S |
| Update mapper Settings | `modules/connectors/dhl_parcel_de/karrio/mappers/dhl_parcel_de/settings.py` | Pending | S |
| Update shipment create to resolve billing | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Pending | M |
| Add billing_number to shipment response meta | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Pending | S |
| Update pickup to read from options | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/pickup/create.py` | Pending | S |
| Update SDK tests | `modules/connectors/dhl_parcel_de/tests/` | Pending | M |

### Phase 2: Server Migration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create schema migration | `modules/core/karrio/server/providers/migrations/` | Pending | S |
| Create data migration | `modules/core/karrio/server/providers/migrations/` | Pending | M |
| Update pickup serializer to pass billing_number | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Update server tests | `modules/manager/karrio/server/manager/tests/` | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1 completion.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines - use `unittest`, NOT pytest.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/connectors/dhl_parcel_de/tests/` | 80%+ |
| Integration Tests | `modules/manager/karrio/server/manager/tests/` | Key flows |

### Test Cases

#### SDK Unit Tests

```python
# modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_shipment.py

import unittest
from unittest.mock import patch, ANY

class TestDHLParcelDEShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_billing_number_resolution_with_service_mapping(self):
        """Verify billing number is resolved from service_billing_numbers."""
        # Config with service-specific billing
        config = {
            "default_billing_number": "11111111110102",
            "service_billing_numbers": [
                {"service": "dhl_parcel_de_paket", "billing_number": "33333333330102"},
            ]
        }
        settings = Settings(
            username="user",
            password="pass",
            client_id="id",
            client_secret="secret",
            config=config,
        )

        billing = settings.get_billing_number("dhl_parcel_de_paket")
        self.assertEqual(billing, "33333333330102")

    def test_billing_number_fallback_to_default(self):
        """Verify billing number falls back to default for unmapped service."""
        config = {
            "default_billing_number": "11111111110102",
            "service_billing_numbers": [
                {"service": "dhl_parcel_de_paket", "billing_number": "33333333330102"},
            ]
        }
        settings = Settings(
            username="user",
            password="pass",
            client_id="id",
            client_secret="secret",
            config=config,
        )

        # Request billing for unmapped service
        billing = settings.get_billing_number("dhl_parcel_de_europaket")
        self.assertEqual(billing, "11111111110102")

    def test_shipment_request_includes_resolved_billing(self):
        """Verify shipment request uses service-resolved billing number."""
        # ... test implementation
        pass
```

#### Pickup Tests

```python
# modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_pickup.py

class TestDHLParcelDEPickup(unittest.TestCase):
    def test_pickup_uses_billing_from_options(self):
        """Verify pickup reads billing_number from options."""
        options = {"billing_number": "33333333330102"}
        # ... test that options.billing_number is used
        pass
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run SDK tests for dhl_parcel_de
python -m unittest discover -v -f modules/connectors/dhl_parcel_de/tests

# Run server tests
karrio test --failfast karrio.server.manager.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Migration corrupts connection data | High | Low | Transaction wrapping, backup before migration |
| Existing integrations break | High | Low | Default billing number provides fallback |
| Pickup fails with wrong billing | Medium | Medium | Pass billing through shipment meta |
| Config validation too strict | Medium | Low | Accept empty config, validate on use |
| Test fixture updates missed | Low | Medium | Run full test suite before merge |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No API changes required; config is internal
- **Data compatibility**: Existing `billing_number` migrated to `config.default_billing_number`
- **Feature flags**: Not needed; migration is atomic

### Data Migration

```python
# modules/core/karrio/server/providers/migrations/XXXX_migrate_dhl_parcel_de_billing_number.py

from django.db import migrations

def migrate_billing_number_to_config(apps, schema_editor):
    """Migrate billing_number from credentials to config.default_billing_number."""
    Carrier = apps.get_model('providers', 'Carrier')

    # Find all dhl_parcel_de carriers with billing_number in credentials
    carriers = Carrier.objects.filter(
        carrier_code='dhl_parcel_de',
    )

    for carrier in carriers:
        credentials = carrier.credentials or {}
        billing_number = credentials.pop('billing_number', None)

        if billing_number:
            config = carrier.config or {}
            config['default_billing_number'] = billing_number
            carrier.config = config
            carrier.credentials = credentials
            carrier.save(update_fields=['config', 'credentials'])

def reverse_migration(apps, schema_editor):
    """Reverse: move default_billing_number back to credentials."""
    Carrier = apps.get_model('providers', 'Carrier')

    carriers = Carrier.objects.filter(
        carrier_code='dhl_parcel_de',
    )

    for carrier in carriers:
        config = carrier.config or {}
        billing_number = config.pop('default_billing_number', None)

        if billing_number:
            credentials = carrier.credentials or {}
            credentials['billing_number'] = billing_number
            carrier.credentials = credentials
            carrier.config = config
            carrier.save(update_fields=['config', 'credentials'])

class Migration(migrations.Migration):
    dependencies = [
        ('providers', 'XXXX_previous_migration'),
    ]

    operations = [
        migrations.RunPython(
            migrate_billing_number_to_config,
            reverse_migration,
        ),
    ]
```

**Migration Steps:**
1. Create migration file with forward and reverse operations
2. Test migration on staging environment
3. Run `karrio migrate` on production
4. Verify all dhl_parcel_de connections have config.default_billing_number

### Rollback Procedure

1. **Identify issue**: Monitor DHL Parcel DE shipment creation failures
2. **Stop rollout**: Do not deploy to additional environments
3. **Revert changes**:
   - Revert code changes via git
   - Run reverse migration: `karrio migrate providers XXXX_previous`
4. **Verify recovery**: Test shipment creation with reverted code

---

## Appendices

### Appendix A: DHL Parcel DE Services

| Karrio Service Code | DHL Product Code | Description |
|---------------------|------------------|-------------|
| `dhl_parcel_de_paket` | V01PAK | Domestic parcel |
| `dhl_parcel_de_kleinpaket` | V62KP | Small domestic parcel |
| `dhl_parcel_de_europaket` | V54EPAK | European parcel |
| `dhl_parcel_de_paket_international` | V53WPAK | International parcel |
| `dhl_parcel_de_warenpost_international` | V66WPI | International warenpost |

### Appendix B: Current File Locations

| Component | File Path |
|-----------|-----------|
| Settings (Provider) | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py` |
| Settings (Mapper) | `modules/connectors/dhl_parcel_de/karrio/mappers/dhl_parcel_de/settings.py` |
| ConnectionConfig | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py` |
| Shipment Create | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` |
| Pickup Create | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/pickup/create.py` |
| Plugin Metadata | `modules/connectors/dhl_parcel_de/karrio/plugins/dhl_parcel_de/__init__.py` |
| Test Fixtures | `modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/fixture.py` |
| Server Pickup Serializer | `modules/manager/karrio/server/manager/serializers/pickup.py` |
| Server Migrations | `modules/core/karrio/server/providers/migrations/` |

---

<!--
CHECKLIST BEFORE SUBMISSION:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (lib.OptionEnum, lib.to_connection_config)
- [x] All required sections completed
- [x] Code examples follow AGENTS.md style EXACTLY as original authors
- [x] Architecture diagrams included (overview, sequence, dataflow - ASCII art)
- [x] Tables used for structured data (not prose)
- [x] Before/After code shown in Problem Statement
- [x] Success criteria are measurable
- [x] Alternatives considered and documented
- [x] Edge cases and failure modes identified
- [x] Test cases follow unittest patterns (NOT pytest)
- [x] Risk assessment completed
- [x] Migration/rollback plan documented
-->
