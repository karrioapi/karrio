# Rate Sheet System vs Account Separation

<!-- REFACTORING: Architecture + migration PRD -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-03-10 |
| Status | Draft |
| Owner | Engineering Team |
| Type | Refactoring |
| Reference | [AGENTS.md](../AGENTS.md) |
| Related PRD | [CARRIER_CONNECTION_ARCHITECTURE_UPGRADE.md](./CARRIER_CONNECTION_ARCHITECTURE_UPGRADE.md) |

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

---

## Executive Summary

The recent carrier-connection refactor introduced explicit **SystemConnection / AccountConnection / BrokeredConnection** separation, but `RateSheet` still uses a mixed model with `is_system` and `created_by`. This PRD proposes splitting rate sheets into explicit **system** vs **account** objects while keeping GraphQL operations and payload shapes as close as possible to today.

The result is cleaner ownership boundaries: **system sheets are platform objects (no owner required, admin GraphQL only)** and **account sheets are tenant objects (base GraphQL only)**.

### Key Architecture Decisions

1. **Separate objects, same behavior shape**: Introduce explicit system/account rate sheet objects while preserving current GraphQL field structure (`services`, `zones`, `surcharges`, `service_rates`, `pricing_config`).
2. **System sheet is non-owned**: System sheets must not depend on `created_by` ownership and are writable only through admin GraphQL mutations.
3. **GraphQL names stay stable where possible**: Keep `create_rate_sheet` / `update_rate_sheet` mutation names in both base/admin schemas, but bind them to different underlying models/querysets.
4. **No user-visible pricing behavior changes**: This is an API/ownership architecture upgrade, not pricing-logic changes.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Separate system vs account rate sheet persistence objects | Changes to surcharge/rate computation logic |
| Restrict system sheet writes to admin GraphQL | New dashboard UX work |
| Align SystemConnection and CarrierConnection FK targets to corresponding sheet type | Redesign of service/zones/surcharges JSON contracts |
| Migrate existing `is_system` data to explicit model separation | Markup model changes |

---

## Open Questions & Decisions

### Pending Questions

None — all resolved.

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Ownership model | System sheet has no `created_by` ownership requirement | System-object semantics — not tenant owned | 2026-03-10 |
| D2 | Mutation surface | System sheet mutations must be admin GraphQL only | Prevent accidental tenant writes to platform pricing | 2026-03-10 |
| D3 | DB table split | **Two separate tables** — full split | Explicit object types, cleaner migration path, matches connection architecture | 2026-03-10 |
| D4 | Base GraphQL visibility for system sheets | **Not exposed** — base GraphQL shows account sheets only | Brokered users don't need to see or query system sheets | 2026-03-10 |
| D5 | Admin mutation scope | **System-only** — admin GraphQL operates exclusively on system sheets | Keep admin domain pure; account sheet mutations remain in base schema | 2026-03-10 |
| D6 | System sheet deletion | **No delete** — system sheets cannot be deleted | System-level pricing objects; deletion is too destructive | 2026-03-10 |

---

## Problem Statement

### Existing Code Analysis

| Area | File | Current State |
|------|------|---------------|
| Data model | `modules/core/karrio/server/providers/models/sheet.py` | Single `RateSheet` model with `is_system` + `created_by` |
| Base GraphQL rate sheets | `modules/graph/karrio/server/graph/schemas/base/types.py` + `mutations.py` | Operates on `providers.RateSheet.access_by(...)` |
| Admin GraphQL rate sheets | `modules/admin/karrio/server/admin/schemas/base/types.py` + `mutations.py` | Uses `is_system=True` filtering in some resolvers, inconsistent in others |
| Carrier links | `modules/core/karrio/server/providers/models/carrier.py` + `connection.py` | `CarrierConnection.rate_sheet` and `SystemConnection.rate_sheet` both target same `RateSheet` model |

### Current State

```python
# modules/core/.../models/sheet.py
class RateSheet(core.OwnedEntity):
    is_system = models.BooleanField(default=False, db_index=True)
    created_by = models.ForeignKey(...)
```

```python
# base graph mutation
instance = providers.RateSheet.access_by(info.context.request).get(id=input["id"])
```

```python
# admin graph mutation
instance = providers.RateSheet.objects.get(id=input["id"], is_system=True)
# Some downstream mutations fetch by id without is_system guard
```

### Desired State

```python
class AccountRateSheet(core.OwnedEntity, BaseRateSheetMixin):
    ...

class SystemRateSheet(models.Model, BaseRateSheetMixin):
    # no owned-entity requirement
    # admin-managed lifecycle only
    ...
```

```python
# base graph
queryset = providers.AccountRateSheet.access_by(info.context.request)

# admin graph
queryset = providers.SystemRateSheet.objects.filter(...)
```

### Problems

1. **Mixed ownership semantics**: `is_system` + `created_by` on same model mixes platform and tenant data into one object lifecycle.
2. **Guard inconsistency risk**: admin mutations mostly use `is_system=True`, but some operations fetch by id only; this creates potential cross-scope mutation bugs.
3. **Connection-model mismatch**: after SystemConnection/Brokered refactor, rate sheets remain flag-based rather than explicit object types.
4. **Testing ambiguity**: current tests do not strongly enforce system/account mutation boundaries as separate domains.

---

## Goals & Success Criteria

### Goals

1. Establish explicit **SystemRateSheet** and **AccountRateSheet** domains.
2. Keep GraphQL APIs highly compatible while enforcing mutation boundaries.
3. Ensure no behavior regressions in rate-sheet editing flows.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Base GraphQL cannot mutate system sheets | 100% enforced by queryset/model boundary | Must-have |
| Admin GraphQL can mutate only system sheets (by default) | 100% enforced | Must-have |
| Existing rate-sheet payload contracts unchanged | No schema break in core fields | Must-have |
| Existing rate sheet tests continue to pass with new architecture | Green | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Explicit system/account rate-sheet object separation in persistence layer
- [ ] Admin-only write path for system sheets
- [ ] Base write path limited to account sheets
- [ ] FK relationships updated for CarrierConnection vs SystemConnection
- [ ] Migration script for existing `is_system` rows

**Nice-to-have (P1):**
- [ ] Add read-only admin view for account sheets if needed
- [ ] Optional system sheet archive lifecycle

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Keep single `RateSheet` + stronger `is_system` guards everywhere | Low migration effort | Easy to regress guard logic; still mixed model | Rejected |
| Split models/tables: `AccountRateSheet` + `SystemRateSheet` | Clear ownership and mutation boundaries | Migration + FK move complexity | **Selected** |
| Keep one table, add `scope` enum + DB constraints | Moderate migration | Still one object lifecycle, less explicit | Rejected |

### Trade-off Analysis

The selected approach mirrors the connection architecture refactor: explicit model domains reduce policy bugs and make authorization mechanical (queryset by model) instead of conditional (`is_system` checks sprinkled in resolvers/mutations).

---

## Technical Design

### 1) Proposed Model Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        BaseRateSheetMixin                           │
│  name, slug, carrier_name, services, zones, surcharges,            │
│  service_rates, metadata, pricing_config                            │
└──────────────────────────────────────────────────────────────────────┘
                ▲                                  ▲
                │                                  │
┌────────────────────────────────┐   ┌────────────────────────────────┐
│ AccountRateSheet              │   │ SystemRateSheet               │
│ - OwnedEntity (created_by)    │   │ - admin managed, non-owned    │
│ - tenant/base GraphQL scope   │   │ - admin GraphQL scope only    │
└────────────────────────────────┘   └────────────────────────────────┘
```

### 2) Connection FK Alignment

| Connection Model | FK Target (New) | Behavior |
|------------------|------------------|----------|
| `CarrierConnection.rate_sheet` | `AccountRateSheet` | Tenant account rates |
| `SystemConnection.rate_sheet` | `SystemRateSheet` | Platform default rates |
| `BrokeredConnection` | inherits via SystemConnection | No direct system-sheet ownership |

### 3) GraphQL Boundary Mapping

| GraphQL Schema | Query/Mutation Target |
|----------------|------------------------|
| Base (`modules/graph/...`) | `AccountRateSheet` only |
| Admin (`modules/admin/...`) | `SystemRateSheet` only |

### 4) Sequence Diagram (Create)

```
Base user -> GraphQL(base): create_rate_sheet
GraphQL(base) -> AccountRateSheetSerializer: validate/save
GraphQL(base) -> CarrierConnection: link selected carriers
GraphQL(base) -> Response(AccountRateSheet)

Admin -> GraphQL(admin): create_rate_sheet
GraphQL(admin) -> SystemRateSheetSerializer: validate/save
GraphQL(admin) -> SystemConnection: link selected system connections
GraphQL(admin) -> Response(SystemRateSheet)
```

### 5) Dataflow Diagram (Migration)

```
Current rate-sheet rows
   ├─ is_system = false  ───────────────► AccountRateSheet
   └─ is_system = true   ───────────────► SystemRateSheet

CarrierConnection.rate_sheet FK ----------► AccountRateSheet(id map)
SystemConnection.rate_sheet FK ----------► SystemRateSheet(id map)
```

### 6) Serializer Strategy

- Reuse existing `RateSheetModelSerializer` logic via a base serializer mixin.
- Keep shape compatibility for `zones`, `surcharges`, `service_rates`, `services`.
- Add explicit serializer classes for each model only where queryset/linking differs.

---

## Edge Cases & Failure Modes

| Edge Case | Failure Mode | Mitigation |
|-----------|--------------|------------|
| Admin mutation called with account sheet id | Cross-domain mutation | Model-bound query prevents lookup |
| Base mutation attempts system sheet update | Unauthorized write | Account-only queryset returns not found/forbidden |
| Existing rows with null/invalid `created_by` for account sheets | Migration rejects row | Data migration validation + report + skip/fix plan |
| System sheet referenced by active system connections during delete | Orphan connections | Enforce delete guard or archive strategy |
| Insiders org links for account rate sheets | Missing org relation migration | Maintain existing `RateSheetLink` semantics for account sheets |

---

## Implementation Plan

### Phase 0 — Validation & Decision Lock

| Step | Action | Output |
|------|--------|--------|
| 0.1 | Confirm Q1–Q4 decisions | Final architecture choice |
| 0.2 | Catalog existing system/account rate-sheet counts | Migration readiness report |

### Phase 1 — Model Split

| Step | Action | Files |
|------|--------|-------|
| 1.1 | Introduce base mixin + two concrete models | `providers/models/sheet.py` (+ new module split if needed) |
| 1.2 | Update FK targets in connection models | `providers/models/carrier.py`, `providers/models/connection.py` |
| 1.3 | Add migrations for new tables/FKs | `modules/manager/.../migrations/*` |

### Phase 2 — GraphQL Scope Hardening

| Step | Action | Files |
|------|--------|-------|
| 2.1 | Base schema resolvers/mutations -> AccountRateSheet | `modules/graph/.../types.py`, `mutations.py` |
| 2.2 | Admin schema resolvers/mutations -> SystemRateSheet | `modules/admin/.../types.py`, `mutations.py` |
| 2.3 | Ensure shared-zone/surcharge/service-rate mutations honor model scope | same as above |

### Phase 3 — Migration + Compatibility

| Step | Action | Output |
|------|--------|--------|
| 3.1 | Migrate old rows (`is_system`) to explicit models | Data migration |
| 3.2 | Keep GraphQL payload compatibility | No client payload break |
| 3.3 | Remove/retire `is_system` flag usage | Cleaner model surface |

### Phase 4 — Verification

| Step | Action |
|------|--------|
| 4.1 | Run graph ratesheet tests + add scope tests |
| 4.2 | Add admin mutation boundary tests |
| 4.3 | Manual smoke on create/update/delete for both schemas |

---

## Testing Strategy

### Current Baseline Verification (run)

Command run from repo root:

```bash
source bin/activate-env
karrio test --failfast karrio.server.graph.tests.test_rate_sheets
```

Result: **74 tests passed** (baseline before implementation).

### Tests to Add/Update

| Test Area | Expected Assertion |
|-----------|--------------------|
| Base `update_rate_sheet` | Cannot update system sheet id |
| Base shared-zone/surcharge mutations | Scope constrained to account sheet queryset |
| Admin `update_rate_sheet` | Cannot update account sheet id |
| Admin shared-zone/surcharge mutations | Scope constrained to system sheet queryset |
| FK migration tests | SystemConnection points to system sheet only; CarrierConnection to account sheet only |
| GraphQL schema compatibility tests | `RateSheetType`/`SystemRateSheetType` field parity maintained |

---

## Risk Assessment

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| Migration mis-maps connection FKs | High | Medium | Dry-run migration + row-level validation report |
| Hidden dependency on old `is_system` | Medium | High | Grep-based audit + CI gate |
| Unexpected client reliance on mixed sheet visibility | Medium | Medium | Decide Q2 explicitly + document |
| Admin tooling assumptions break | Medium | Low | Add admin GraphQL regression tests |

---

## Migration & Rollback

### Migration Strategy

1. Introduce new models and parallel tables.
2. Copy/transform existing rows by `is_system` into target model.
3. Update connection FK mappings.
4. Cut GraphQL resolvers/mutations to explicit models.
5. Remove legacy flag dependence.

### Rollback Strategy

- **Forward-preferred** rollout (recommended).
- Keep migration snapshots (`old_id -> new_id`) for emergency restoration.
- If rollback required before cutover complete, restore old FK fields and flip resolver feature flag.

---

## Notes for Implementation PR

- Keep external mutation names stable where possible.
- Treat this as a **non-breaking API upgrade**: ownership boundary tightening, not payload redesign.
- Preserve editor behavior and service/zone/surcharge JSON schema.
