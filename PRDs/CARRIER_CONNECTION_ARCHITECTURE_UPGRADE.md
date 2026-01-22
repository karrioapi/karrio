# Product Requirements Document: Carrier Connection Architecture Upgrade

**Project**: Migration to System/Account/Brokered Connection Model
**Version**: 1.0
**Date**: 2025-12-16
**Status**: Planning
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Criteria](#3-goals--success-criteria)
4. [Proposed Architecture](#4-proposed-architecture)
5. [Data Models](#5-data-models)
6. [Architecture Diagrams](#6-architecture-diagrams)
7. [API Design](#7-api-design)
8. [Migration Strategy](#8-migration-strategy)
9. [Implementation Plan](#9-implementation-plan)
10. [Testing Strategy](#10-testing-strategy)
11. [Risk Assessment](#11-risk-assessment)
12. [Rollout Plan](#12-rollout-plan)

---

## 1. Executive Summary

This document outlines a comprehensive architectural upgrade to the Karrio carrier connection system, transforming it from a single `Carrier` model with an `is_system` flag and separate `CarrierConfig` into a **normalized three-model architecture**:

| Model | Purpose | Credentials | Config |
|-------|---------|-------------|--------|
| **SystemConnection** (car_xxx) | Platform-wide carrier templates managed by admins | Admin-only access | Base operational config |
| **AccountConnection** (car_xxx) | User/Org-owned carrier connections | User-managed | Full control |
| **BrokeredConnection** (car_xxx) | Links user to system connection with config overrides | Inherited (read-only) | Override JSONField |

### Key Benefits

- **Eliminates N+1 queries**: Config merged into connection, no separate model
- **Explicit ownership**: Clear distinction between system vs user vs brokered
- **Simplified filtering**: `gateway.Carriers.list()` becomes cleaner
- **Follows ShippingMethods pattern**: Proven architecture already in production
- **Seamless migration**: Users see no change in behavior

### Key Design Decisions

#### Architecture Decisions
1. **Brokered configs are operational only** - No credential overrides, only operational settings
2. **System credentials never exposed** - BrokeredConnection.credentials always returns `None`; gateway accesses `_get_credentials()` internally
3. **Capabilities are overridable** - Brokered connections can restrict/modify capabilities (e.g., disable rating)
4. **Implicit visibility** - BrokeredConnection existence grants access; Carrier in OSS is system-wide accessible (Insiders: org-scoped via CarrierLink)
5. **Rate sheets inherited** - Brokered uses system connection's rate sheet as-is
6. **Unified REST API** - Single schema, GraphQL exposes three types separately
7. **Pattern-based migration** - Detect "system-like" carriers (is_system=True) for automatic conversion
8. **Unified ID prefix** - All connection types use `car_xxx` prefix for consistency
9. **Simple property names** - BrokeredConnection uses `config`, `carrier_id`, `display_name`, `capabilities` (not `effective_*`)

#### Model & Naming Decisions
10. **Keep Carrier model name** - Do NOT rename to AccountConnection; remove `is_system`, `active_users`, `active_orgs` fields
11. **Single utility module** - Consolidate GatewayMixin, UnifiedConnection, ConnectionResolver into single `carriers.py` utility with `resolve_carrier()` and `create_snapshot()` functions
12. **Gateway logic on models** - Each model (Carrier, SystemConnection, BrokeredConnection) keeps its own `gateway` property
13. **Complete gateway.Carriers replacement** - `gateway.Connections` completely replaces `gateway.Carriers` (no alias)
14. **Models-only exports** - Export SystemConnection, BrokeredConnection, Carrier; keep utilities internal

#### Migration Decisions
15. **MOVE data, not copy** - System carriers are MOVED to SystemConnection table (deleted from Carrier after migration)
16. **Copy CarrierConfig to BrokeredConnection** - User/org-specific CarrierConfig.config migrated to BrokeredConnection.config_overrides
17. **Delete CarrierConfig table** - Remove CarrierConfig model and table in same migration
18. **Prefer orgs over users** - In Insiders mode: create BrokeredConnections for active_orgs only; OSS: active_users only
19. **Unused system carriers preserved** - System carriers with no active_users/active_orgs still become SystemConnection (can be enabled later)
20. **Django ORM migrations only** - No raw SQL; regenerate fresh migrations

#### Legacy FK Decisions
21. **FK → JSONField conversion** - Remove all carrier FKs (pickup_carrier, tracking_carrier, etc.) and replace with `carrier_snapshot` JSONField
22. **Drop Shipment.carriers M2M** - Remove entirely; `selected_rate` JSONField already contains carrier info
23. **Carrier snapshot minimal data** - Store: connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode (no capabilities, no config)
24. **Visibility via CarrierLink only** - Remove active_users/active_orgs M2M; OSS: all carriers visible; Insiders: org-scoped via CarrierLink
25. **Orgs package in same PR** - Create BrokeredConnectionLink in orgs package as part of this migration

#### Implementation Details
26. **Utility in core/utils.py** - Add `resolve_carrier()` and `create_snapshot()` functions to existing core utils module
27. **Org brokered created_by is null** - Org-scoped BrokeredConnections have created_by=null; access via BrokeredConnectionLink
28. **Simple snapshot, no fallback ID** - Snapshot contains connection_id only; if connection deleted, use snapshot for display only
29. **resolve_carrier() returns None** - When connection not found or access denied, return None (caller handles)
30. **Brokered snapshot uses system ID** - When BrokeredConnection is used, snapshot stores SystemConnection ID (stable if brokered deleted)
31. **Connection type values** - Use "account", "system", "brokered" as connection_type values in snapshots
32. **SystemConnection.created_by** - Nullable FK(User, on_delete=SET_NULL) to track admin who created it
33. **Brokered resolution with system ID** - When resolving type='brokered' snapshot: find user's BrokeredConnection for that SystemConnection; return it if found, else return SystemConnection
34. **Brokered snapshot uses computed values** - Snapshot stores system.id as connection_id but uses brokered's computed carrier_id, carrier_name (respects overrides)
35. **Connections API: list() and first()** - Keep simple: `list()` returns all matching, `first()` returns first match
36. **Forward-only migration** - No reverse migration. Data is moved. Manual intervention needed for rollback.

### Areas Requiring Updates (Carrier References)

The following files/modules reference the Carrier model and will need updates:

**Core Module:**
- `modules/core/karrio/server/core/gateway.py` - Main gateway.Carriers class
- `modules/core/karrio/server/core/filters.py` - Carrier filtering
- `modules/core/karrio/server/providers/serializers/base.py` - Carrier serializers
- `modules/core/karrio/server/providers/views/carriers.py` - Carrier REST views
- `modules/core/karrio/server/providers/admin.py` - Django admin

**Manager Module:**
- `modules/manager/karrio/server/manager/models.py` - Pickup, Tracking, Shipment, etc.
- `modules/manager/karrio/server/manager/serializers/shipment.py` - Shipment serializers

**Graph Module:**
- `modules/graph/karrio/server/graph/schemas/base/types.py` - GraphQL types
- `modules/graph/karrio/server/graph/schemas/base/mutations.py` - GraphQL mutations
- `modules/graph/karrio/server/graph/utils.py` - GraphQL utilities

**Orgs Module (Insiders):**
- `ee/insiders/modules/orgs/karrio/server/orgs/models.py` - Organization model with system_carriers M2M
- `ee/insiders/modules/admin/karrio/server/admin/schemas/` - Admin GraphQL schemas

**Pricing Module:**
- `modules/pricing/karrio/server/pricing/models.py` - Surcharge carrier accounts

**Data Module:**
- `modules/data/karrio/server/data/resources/trackers.py` - Tracker resources

---

## 2. Problem Statement

### 2.1 Current Architecture Issues

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CURRENT ARCHITECTURE PROBLEMS                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 1: N+1 Query Pattern in CarrierConfig Resolution                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Carrier.resolve_config() performs separate query per carrier:                  │
│                                                                                 │
│    for carrier in carriers:                                                     │
│        config = CarrierConfig.objects.filter(carrier=carrier).first()  # N+1!  │
│                                                                                 │
│  Current mitigation with Subquery annotation is complex:                        │
│                                                                                 │
│    config_query = CarrierConfig.objects.filter(carrier=OuterRef("pk"))          │
│        .annotate(priority=Case(When(my_config_filter, then=0), default=1))     │
│        .order_by("priority")                                                    │
│    queryset.annotate(_computed_config=Subquery(config_query.values("config")))  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 2: Ambiguous Ownership Model                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Current model uses multiple overlapping patterns:                              │
│                                                                                 │
│    Carrier                                                                      │
│      ├── is_system: bool          # Flag-based type distinction                 │
│      ├── created_by: FK(User)     # Creator tracking                            │
│      ├── active_users: M2M(User)  # OSS visibility                              │
│      ├── active_orgs: M2M(Org)    # Insiders visibility                         │
│      └── org: M2M via CarrierLink # Ownership link                              │
│                                                                                 │
│    CarrierConfig                                                                │
│      ├── carrier: FK(Carrier)     # Linked carrier                              │
│      ├── created_by: FK(User)     # Config creator                              │
│      └── org: M2M via CarrierConfigLink  # Org link                             │
│                                                                                 │
│  Questions that arise:                                                          │
│    - Is this carrier system-wide or user-owned?                                 │
│    - Which config applies to this user/org?                                     │
│    - Can user override system carrier config?                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 3: Complex gateway.Carriers.list() Logic                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Current filtering logic (gateway.py:24-124):                                   │
│                                                                                 │
│    1. Get user_filter from get_access_filter(context)                           │
│    2. Build creator_filter for personal carriers                                │
│    3. Query user_carriers with (user_filter | creator_filter)                   │
│    4. Query system_carriers with active_users/active_orgs check                 │
│    5. Union: _user_carriers | _system_carriers                                  │
│    6. Apply test_mode, active, carrier_id, capability filters                   │
│    7. Apply metadata_key, metadata_value filters                                │
│    8. Apply carrier_ids, services, carrier_name filters                         │
│    9. Call .distinct()                                                          │
│                                                                                 │
│  This 100+ line method is hard to maintain and test.                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 4: Separate CarrierConfig Model Adds Complexity                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  CarrierConfig exists to allow per-user/per-org config overrides for system     │
│  carriers, but creates:                                                         │
│                                                                                 │
│    - Extra database table and migrations                                        │
│    - Extra Link table for org association                                       │
│    - Complex resolution logic (user config > system config)                     │
│    - Confusion about what goes in Carrier.credentials vs CarrierConfig.config   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Current Data Model

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            CURRENT DATA MODEL                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│              Carrier                 │
├──────────────────────────────────────┤
│  id: CharField (car_xxx)             │
│  carrier_code: CharField             │  ← "dhl_express", "fedex", etc.
│  carrier_id: CharField               │  ← User-defined identifier
│  credentials: JSONField              │  ← API keys, account numbers
│  capabilities: MultiChoiceField      │
│  metadata: JSONField                 │
│  active: BooleanField                │
│  is_system: BooleanField             │  ← Overloaded type flag
│  test_mode: BooleanField             │
│  created_by: FK(User)                │
│  active_users: M2M(User)             │  ← OSS visibility
│  rate_sheet: FK(RateSheet)           │
├──────────────────────────────────────┤
│  [If MULTI_ORGANIZATIONS]            │
│  org: M2M via CarrierLink            │
│  active_orgs: M2M(Organization)      │  ← Insiders visibility
└──────────────────────────────────────┘
           │
           │ has_many
           ▼
┌──────────────────────────────────────┐
│           CarrierConfig              │
├──────────────────────────────────────┤
│  id: CharField (cfg_xxx)             │
│  carrier: FK(Carrier)                │
│  config: JSONField                   │  ← Operational overrides
│  created_by: FK(User)                │
├──────────────────────────────────────┤
│  [If MULTI_ORGANIZATIONS]            │
│  org: M2M via CarrierConfigLink      │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│           CarrierLink                │
├──────────────────────────────────────┤
│  org: FK(Organization)               │
│  item: OneToOne(Carrier)             │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        CarrierConfigLink             │
├──────────────────────────────────────┤
│  org: FK(Organization)               │
│  item: OneToOne(CarrierConfig)       │
└──────────────────────────────────────┘
```

---

## 3. Goals & Success Criteria

### 3.1 Goals

| Goal | Description |
|------|-------------|
| **G1** | Eliminate N+1 queries by merging config into connection model |
| **G2** | Explicit type distinction (System/Account/Brokered) instead of flag |
| **G3** | Simplified `gateway.Carriers.list()` with cleaner filtering logic |
| **G4** | Clear ownership model aligned with ShippingMethods pattern |
| **G5** | Seamless migration with zero user-facing changes |
| **G6** | Unified REST API schema (single connection type exposed) |

### 3.2 Success Criteria

| Criteria | Metric | Target |
|----------|--------|--------|
| **Query Performance** | Queries per carrier list request | 1-3 (down from N+1) |
| **Code Complexity** | Lines in `gateway.Carriers.list()` | < 50 (down from 100+) |
| **Migration Success** | Data integrity post-migration | 100% |
| **API Schema** | Breaking changes to REST API | 0 |
| **Test Coverage** | Unit test coverage for new models | > 90% |

### 3.3 Non-Goals

- Changing the carrier SDK/gateway interface
- Modifying carrier credentials structure
- Changing rate sheet architecture
- Adding new carrier capabilities

---

## 4. Proposed Architecture

### 4.1 Three-Model Design

Taking inspiration from the ShippingMethods architecture (`SystemShippingMethod`, `ShippingMethod`, `BrokeredShippingMethod`), we introduce:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PROPOSED ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                      SystemConnection (car_xxx)                           │  │
│  │                                                                           │  │
│  │  Platform-wide carrier connections managed by administrators.             │  │
│  │  - Credentials: Admin-only (users cannot view or modify)                  │  │
│  │  - Config: Base operational settings (label format, defaults)             │  │
│  │  - Rate Sheet: Optional, inherited by brokered connections                │  │
│  │  - Visibility: Available to all users who create a BrokeredConnection     │  │
│  │                                                                           │  │
│  │  Examples:                                                                │  │
│  │  - Platform DHL Express account for all tenants                           │  │
│  │  - Pre-negotiated UPS rates for reselling                                 │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                     AccountConnection (car_xxx)                           │  │
│  │                                                                           │  │
│  │  User/Organization-owned carrier connections with full control.           │  │
│  │  - Credentials: User-managed (full access)                                │  │
│  │  - Config: Full operational control                                       │  │
│  │  - Rate Sheet: User-assigned                                              │  │
│  │  - Visibility: OSS = all users; Insiders = org members only               │  │
│  │                                                                           │  │
│  │  Examples:                                                                │  │
│  │  - Merchant's own FedEx account                                           │  │
│  │  - Company's negotiated DHL rates                                         │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    BrokeredConnection (car_xxx)                           │  │
│  │                                                                           │  │
│  │  User's enabled instance of a SystemConnection with config overrides.     │  │
│  │  - Credentials: Inherited from system (read-only, not exposed)            │  │
│  │  - Config: Override JSONField (additive, operational only)                │  │
│  │  - Rate Sheet: Inherited from system connection (as-is)                   │  │
│  │  - Visibility: Implicit (existence grants access)                         │  │
│  │                                                                           │  │
│  │  Examples:                                                                │  │
│  │  - Merchant enables platform DHL with custom label settings               │  │
│  │  - Tenant uses platform UPS with different default package type           │  │
│  │                                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Comparison with ShippingMethods

| Aspect | ShippingMethods | Carrier Connections (New) |
|--------|-----------------|---------------------------|
| System Model | `SystemShippingMethod` | `SystemConnection` |
| Account Model | `ShippingMethod` (AccountShippingMethod) | `AccountConnection` |
| Brokered Model | `BrokeredShippingMethod` | `BrokeredConnection` |
| System→Brokered Link | `system_method: FK` | `system_connection: FK` |
| Config Override | `carrier_options`, `constraint_overrides` | `config_overrides: JSONField` |
| Credential Handling | N/A (uses carrier_connection) | Inherited, not exposed |
| Rate Sheet | Via carrier_connection | Direct FK or inherited |

### 4.3 Config Override Scope

The `config_overrides` JSONField in `BrokeredConnection` supports **operational settings only**:

```json
{
  "label_format": "PDF",
  "label_size": "4x6",
  "default_package_type": "your_packaging",
  "default_weight_unit": "KG",
  "default_dimension_unit": "CM",
  "insurance_enabled": true,
  "signature_required": false,
  "reference_prefix": "ACME-",
  "notification_email": "shipping@acme.com"
}
```

**NOT allowed in config_overrides:**
- API keys, tokens, secrets
- Account numbers
- Billing references
- Authentication credentials

---

## 5. Data Models

### 5.1 New Model Definitions

```python
# karrio/server/providers/models/connection.py

import typing
import functools
import django.conf as conf
import django.db.models as models

import karrio.server.core.models as core


# =============================================================================
# SYSTEM CONNECTION - Admin-managed platform-wide connections
# =============================================================================

class SystemConnectionManager(models.Manager):
    """Manager for system connections with optimized queries."""

    def get_queryset(self):
        return super().get_queryset().select_related("rate_sheet")


@core.register_model
class SystemConnection(core.Entity):
    """
    Platform-wide carrier connections managed by administrators.

    Key characteristics:
    - Created and managed by platform admins only
    - Credentials are admin-only (not exposed to users)
    - Users access via BrokeredConnection
    - Rate sheet inherited by brokered connections
    """

    class Meta:
        db_table = "system_connection"
        verbose_name = "System Connection"
        verbose_name_plural = "System Connections"
        ordering = ["carrier_code", "-created_at"]
        indexes = [
            models.Index(fields=["carrier_code", "is_active"]),
            models.Index(fields=["is_active", "test_mode"]),
        ]

    objects = SystemConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_code = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Carrier identifier (e.g., 'dhl_express', 'fedex')",
    )
    carrier_id = models.CharField(
        max_length=150,
        db_index=True,
        help_text="User-defined connection identifier",
    )
    display_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Human-readable name for the connection",
    )

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIALS (Admin-only access)
    # ─────────────────────────────────────────────────────────────────
    credentials = models.JSONField(
        default=core.field_default({}),
        help_text="Carrier API credentials (admin-only)",
    )

    # ─────────────────────────────────────────────────────────────────
    # CONFIGURATION (Base operational settings)
    # ─────────────────────────────────────────────────────────────────
    config = models.JSONField(
        default=core.field_default({}),
        help_text="Base operational configuration",
    )

    # ─────────────────────────────────────────────────────────────────
    # CAPABILITIES & STATUS
    # ─────────────────────────────────────────────────────────────────
    capabilities = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
        help_text="Enabled carrier capabilities",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    test_mode = models.BooleanField(default=True, db_index=True)

    # ─────────────────────────────────────────────────────────────────
    # RATE SHEET (Optional)
    # ─────────────────────────────────────────────────────────────────
    rate_sheet = models.ForeignKey(
        "RateSheet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="system_connections",
    )

    # ─────────────────────────────────────────────────────────────────
    # METADATA
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        default=core.field_default({}),
        blank=True,
    )

    @property
    def object_type(self):
        return "system-connection"

    @property
    def carrier_name(self):
        return self.carrier_code

    def __str__(self):
        return f"{self.display_name or self.carrier_id} ({self.carrier_code})"


# =============================================================================
# ACCOUNT CONNECTION - User/Org-owned connections
# =============================================================================

class AccountConnectionQuerySet(models.QuerySet):
    """QuerySet with optimized loading."""

    def with_related(self):
        return self.select_related("rate_sheet", "created_by")


class AccountConnectionManager(models.Manager):
    def get_queryset(self):
        return AccountConnectionQuerySet(self.model, using=self._db)

    def with_related(self):
        return self.get_queryset().with_related()


@core.register_model
class AccountConnection(core.OwnedEntity):
    """
    User/Organization-owned carrier connections with full control.

    IMPORTANT: This model REUSES the existing Carrier table (db_table="carrier").
    The model class is renamed but the underlying table stays the same.

    Key characteristics:
    - Created and managed by users/orgs
    - Full access to credentials and config
    - Independent of system connections
    - Visibility:
      - OSS: Accessible to ALL users (system-wide shared)
      - Insiders: Scoped to organization members only
    """

    class Meta:
        db_table = "carrier"  # REUSE existing Carrier table
        verbose_name = "Account Connection"
        verbose_name_plural = "Account Connections"
        ordering = ["carrier_code", "-created_at"]
        indexes = [
            models.Index(fields=["carrier_code", "is_active"]),
        ]

    objects = AccountConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_code = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Carrier identifier (e.g., 'dhl_express', 'fedex')",
    )
    carrier_id = models.CharField(
        max_length=150,
        db_index=True,
        help_text="User-defined connection identifier",
    )

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIALS (User-managed)
    # ─────────────────────────────────────────────────────────────────
    credentials = models.JSONField(
        default=core.field_default({}),
        help_text="Carrier API credentials",
    )

    # ─────────────────────────────────────────────────────────────────
    # CONFIGURATION (Full control)
    # ─────────────────────────────────────────────────────────────────
    config = models.JSONField(
        default=core.field_default({}),
        help_text="Operational configuration",
    )

    # ─────────────────────────────────────────────────────────────────
    # CAPABILITIES & STATUS
    # ─────────────────────────────────────────────────────────────────
    capabilities = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
    )
    is_active = models.BooleanField(default=True, db_index=True)
    test_mode = models.BooleanField(default=True, db_index=True)

    # ─────────────────────────────────────────────────────────────────
    # RATE SHEET
    # ─────────────────────────────────────────────────────────────────
    rate_sheet = models.ForeignKey(
        "RateSheet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="account_connections",
    )

    # ─────────────────────────────────────────────────────────────────
    # OWNERSHIP
    # ─────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    # NOTE: Organization linking is handled via AccountConnectionLink in orgs package (Insiders only)
    # The M2M relationship is defined on Organization model, not here, to avoid OSS import issues

    # ─────────────────────────────────────────────────────────────────
    # METADATA
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        default=core.field_default({}),
        blank=True,
    )

    @property
    def object_type(self):
        return "account-connection"

    @property
    def carrier_name(self):
        return self.carrier_code

    @property
    def display_name(self):
        return self.credentials.get("display_name") or self.carrier_id


# =============================================================================
# NOTE: AccountConnectionLink is defined in orgs package (Insiders only)
# See: karrio/server/orgs/models.py
#
# class AccountConnectionLink(models.Model):
#     org = models.ForeignKey("orgs.Organization", ...)
#     item = models.OneToOneField("providers.AccountConnection", related_name="link", ...)
# =============================================================================


# =============================================================================
# BROKERED CONNECTION - User's enabled system connection
# =============================================================================

class BrokeredConnectionQuerySet(models.QuerySet):
    """QuerySet with optimized loading for effective config resolution."""

    def with_effective_config(self):
        """
        Prefetch system connection for efficient config resolution.
        Single query returns brokered + system + rate_sheet.
        """
        return self.select_related(
            "system_connection",
            "system_connection__rate_sheet",
        )

    def for_carrier(self, carrier_code: str):
        """Filter by carrier code (via system connection)."""
        return self.filter(system_connection__carrier_code=carrier_code)


class BrokeredConnectionManager(models.Manager):
    def get_queryset(self):
        return BrokeredConnectionQuerySet(self.model, using=self._db)

    def with_effective_config(self):
        return self.get_queryset().with_effective_config()


@core.register_model
class BrokeredConnection(core.OwnedEntity):
    """
    User's enabled instance of a SystemConnection.

    Key characteristics:
    - MUST link to a SystemConnection (required FK)
    - Inherits credentials from system_connection (read-only, not exposed)
    - Can ADD config_overrides but cannot modify credentials
    - Inherits rate_sheet from system_connection
    - Visibility is implicit (existence grants access)
    """

    class Meta:
        db_table = "brokered_connection"
        verbose_name = "Brokered Connection"
        verbose_name_plural = "Brokered Connections"
        ordering = ["system_connection__carrier_code", "-created_at"]
        indexes = [
            models.Index(fields=["system_connection", "is_enabled"]),
        ]
        # Ensure one brokered connection per system connection per org/user
        constraints = [
            models.UniqueConstraint(
                fields=["system_connection", "created_by"],
                condition=models.Q(link__isnull=True),
                name="unique_brokered_per_user",
            ),
        ]

    objects = BrokeredConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )

    # ─────────────────────────────────────────────────────────────────
    # RELATIONSHIP TO SYSTEM CONNECTION (Required)
    # ─────────────────────────────────────────────────────────────────
    system_connection = models.ForeignKey(
        SystemConnection,
        on_delete=models.CASCADE,
        related_name="brokered_connections",
        help_text="The system connection this is derived from",
    )

    # ─────────────────────────────────────────────────────────────────
    # OVERRIDES (Operational only - no credentials)
    # ─────────────────────────────────────────────────────────────────
    config_overrides = models.JSONField(
        default=core.field_default({}),
        blank=True,
        help_text="Operational config overrides (merged with system config)",
    )
    capabilities_overrides = models.JSONField(
        default=core.field_default([]),
        blank=True,
        help_text="Capabilities overrides (merged with system capabilities)",
    )

    # ─────────────────────────────────────────────────────────────────
    # CUSTOM IDENTIFIER
    # ─────────────────────────────────────────────────────────────────
    carrier_id_override = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        db_column="carrier_id",  # Keep column name for simplicity
        help_text="Custom identifier (falls back to system_connection.carrier_id)",
    )
    display_name_override = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_column="display_name",  # Keep column name for simplicity
        help_text="Custom display name (falls back to system connection)",
    )

    # ─────────────────────────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────────────────────────
    is_enabled = models.BooleanField(default=True, db_index=True)

    # ─────────────────────────────────────────────────────────────────
    # OWNERSHIP
    # ─────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    # NOTE: Organization linking is handled via BrokeredConnectionLink in orgs package (Insiders only)
    # The M2M relationship is defined on Organization model, not here, to avoid OSS import issues

    # ─────────────────────────────────────────────────────────────────
    # METADATA
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        default=core.field_default({}),
        blank=True,
    )

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES
    # ─────────────────────────────────────────────────────────────────

    @property
    def object_type(self):
        return "brokered-connection"

    @property
    def carrier_code(self) -> str:
        """Get carrier code from system connection."""
        return self.system_connection.carrier_code

    @property
    def carrier_name(self) -> str:
        """Get carrier name from system connection."""
        return self.system_connection.carrier_name

    @property
    def carrier_id(self) -> str:
        """Get carrier_id with fallback to system connection."""
        return self.carrier_id_override or self.system_connection.carrier_id

    @property
    def display_name(self) -> str:
        """Get display name with fallback chain."""
        return (
            self.display_name_override
            or self.system_connection.display_name
            or self.system_connection.carrier_id
        )

    @property
    def config(self) -> dict:
        """Merge system config with overrides (overrides take precedence)."""
        base = dict(self.system_connection.config or {})
        overrides = dict(self.config_overrides or {})
        return {**base, **overrides}

    @property
    def credentials(self) -> dict:
        """
        Always returns None - system credentials are never exposed.
        The gateway uses system_connection.credentials internally.
        """
        return None

    @property
    def capabilities(self) -> list:
        """Merge system capabilities with overrides (overrides replace if provided)."""
        system_caps = list(self.system_connection.capabilities or [])
        overrides = list(self.capabilities_overrides or [])
        # If overrides provided, use them; otherwise use system capabilities
        return overrides if overrides else system_caps

    @property
    def test_mode(self) -> bool:
        """Get test_mode from system connection."""
        return self.system_connection.test_mode

    @property
    def rate_sheet(self):
        """Get rate sheet from system connection."""
        return self.system_connection.rate_sheet

    @property
    def is_active(self) -> bool:
        """Active if enabled AND system connection is active."""
        return self.is_enabled and self.system_connection.is_active


# =============================================================================
# NOTE: BrokeredConnectionLink is defined in orgs package (Insiders only)
# See: karrio/server/orgs/models.py
#
# class BrokeredConnectionLink(models.Model):
#     org = models.ForeignKey("orgs.Organization", ...)
#     item = models.OneToOneField("providers.BrokeredConnection", related_name="link", ...)
# =============================================================================
```

### 5.2 Unified Connection Interface

To provide a consistent interface for the gateway and API layer that works with all connection types, we create a unified interface:

```python
# karrio/server/providers/models/unified.py

from dataclasses import dataclass
from typing import Union, Optional
import karrio.server.providers.models as providers


@dataclass
class UnifiedConnection:
    """
    Unified interface for all connection types.
    Used by gateway and API layer to work with any connection type.
    """

    id: str
    carrier_code: str
    carrier_id: str
    carrier_name: str
    display_name: str
    credentials: dict
    config: dict
    capabilities: list
    metadata: dict
    is_active: bool
    test_mode: bool
    rate_sheet: Optional[object]
    connection_type: str  # "system", "account", "brokered"

    # Source reference
    _source: Union[
        "providers.SystemConnection",
        "providers.AccountConnection",
        "providers.BrokeredConnection",
    ]

    @classmethod
    def from_system(cls, conn: "providers.SystemConnection") -> "UnifiedConnection":
        return cls(
            id=conn.id,
            carrier_code=conn.carrier_code,
            carrier_id=conn.carrier_id,
            carrier_name=conn.carrier_name,
            display_name=conn.display_name or conn.carrier_id,
            credentials=conn.credentials,
            config=conn.config,
            capabilities=conn.capabilities,
            metadata=conn.metadata,
            is_active=conn.is_active,
            test_mode=conn.test_mode,
            rate_sheet=conn.rate_sheet,
            connection_type="system",
            _source=conn,
        )

    @classmethod
    def from_account(cls, conn: "providers.AccountConnection") -> "UnifiedConnection":
        return cls(
            id=conn.id,
            carrier_code=conn.carrier_code,
            carrier_id=conn.carrier_id,
            carrier_name=conn.carrier_name,
            display_name=conn.display_name,
            credentials=conn.credentials,
            config=conn.config,
            capabilities=conn.capabilities,
            metadata=conn.metadata,
            is_active=conn.is_active,
            test_mode=conn.test_mode,
            rate_sheet=conn.rate_sheet,
            connection_type="account",
            _source=conn,
        )

    @classmethod
    def from_brokered(cls, conn: "providers.BrokeredConnection") -> "UnifiedConnection":
        # NOTE: For gateway use, we need actual credentials from system_connection
        # But conn.credentials returns None for security - get directly from system
        return cls(
            id=conn.id,
            carrier_code=conn.carrier_code,
            carrier_id=conn.carrier_id,           # Computed: override or system fallback
            carrier_name=conn.carrier_name,
            display_name=conn.display_name,       # Computed: override or system fallback
            credentials=conn.system_connection.credentials,  # Direct access for gateway
            config=conn.config,                   # Computed: merged config
            capabilities=conn.capabilities,       # Computed: merged capabilities
            metadata=conn.metadata,
            is_active=conn.is_active,
            test_mode=conn.test_mode,
            rate_sheet=conn.rate_sheet,
            connection_type="brokered",
            _source=conn,
        )
```

---

## 6. Architecture Diagrams

### 6.1 Class/Model Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CLASS/MODEL RELATIONSHIP DIAGRAM                         │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │    RateSheet    │
                              │    (rate_xxx)   │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
┌───────────────────────────┐  (inherits FK)  ┌───────────────────────────┐
│    SystemConnection       │◄────────────────│    BrokeredConnection     │
│        (car_xxx)          │                 │        (car_xxx)          │
├───────────────────────────┤                 ├───────────────────────────┤
│ id: CharField             │                 │ id: CharField             │
│ carrier_code: CharField   │                 │ system_connection: FK ────┼───┐
│ carrier_id: CharField     │                 │ config_overrides: JSON    │   │
│ display_name: CharField   │                 │ carrier_id: CharField     │   │
│ credentials: JSONField    │◄────────────────│ display_name: CharField   │   │
│ config: JSONField         │  (credentials)  │ is_enabled: BooleanField  │   │
│ capabilities: MultiChoice │                 │ created_by: FK(User)      │   │
│ is_active: BooleanField   │                 │ metadata: JSONField       │   │
│ test_mode: BooleanField   │                 └─────────────┬─────────────┘   │
│ rate_sheet: FK ───────────┼─────────┐                     │                 │
│ metadata: JSONField       │         │                     │ M2M             │
└───────────────────────────┘         │                     ▼                 │
                                      │       ┌─────────────────────────┐     │
┌───────────────────────────┐         │       │ BrokeredConnectionLink  │     │
│    AccountConnection      │         │       ├─────────────────────────┤     │
│        (car_xxx)          │         │       │ org: FK(Organization)   │     │
├───────────────────────────┤         │       │ item: OneToOne(Brokered)│     │
│ id: CharField             │         │       └─────────────────────────┘     │
│ carrier_code: CharField   │         │                                       │
│ carrier_id: CharField     │         │       ┌─────────────────────────┐     │
│ credentials: JSONField    │         └──────►│      Organization       │     │
│ config: JSONField         │                 ├─────────────────────────┤     │
│ capabilities: MultiChoice │                 │ account_connections M2M │     │
│ is_active: BooleanField   │                 │ brokered_connections M2M│     │
│ test_mode: BooleanField   │                 │ system_connections M2M* │     │
│ rate_sheet: FK ───────────┼─────────────────┤ (* via brokered links)  │     │
│ created_by: FK(User)      │                 └─────────────────────────┘     │
│ metadata: JSONField       │                                                 │
└─────────────┬─────────────┘                                                 │
              │ M2M                                                           │
              ▼                                                               │
┌─────────────────────────────┐                                               │
│  AccountConnectionLink      │                         Required FK           │
├─────────────────────────────┤                              │                │
│ org: FK(Organization)       │                              └────────────────┘
│ item: OneToOne(Account)     │
└─────────────────────────────┘


Legend:
  ─────►  Foreign Key (required)
  - - -►  Foreign Key (optional)
  ◄─────  Inherited property (read-only)
  ══════  M2M relationship via Link table
```

### 6.2 Data Flow Diagram - Connection Resolution

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    CONNECTION RESOLUTION DATA FLOW                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                              API Request                                       │
│                    GET /v1/carriers or POST /v1/rates                          │
└───────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                         Context Extraction                                     │
│                                                                               │
│   context = {                                                                 │
│       user: request.user,                                                     │
│       org: request.org,           # Insiders only                             │
│       test_mode: request.test_mode                                            │
│   }                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                       gateway.Connections.list()                               │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────────┐ │
│   │  Step 1: Get Account Connections                                        │ │
│   │                                                                         │ │
│   │  if MULTI_ORGANIZATIONS and context.org:                                │ │
│   │      # Insiders: Scoped to organization                                 │ │
│   │      account_conns = AccountConnection.objects.filter(                  │ │
│   │          link__org=context.org,                                         │ │
│   │          is_active=True,                                                │ │
│   │          test_mode=context.test_mode                                    │ │
│   │      )                                                                  │ │
│   │  else:                                                                  │ │
│   │      # OSS: All account connections are system-wide accessible          │ │
│   │      account_conns = AccountConnection.objects.filter(                  │ │
│   │          is_active=True,                                                │ │
│   │          test_mode=context.test_mode                                    │ │
│   │      )                                                                  │ │
│   └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────────┐ │
│   │  Step 2: Get Brokered Connections (implicit visibility)                 │ │
│   │                                                                         │ │
│   │  if MULTI_ORGANIZATIONS and context.org:                                │ │
│   │      # Insiders: Scoped to organization                                 │ │
│   │      brokered_conns = BrokeredConnection.objects                        │ │
│   │          .with_effective_config()                                       │ │
│   │          .filter(                                                       │ │
│   │              link__org=context.org,                                     │ │
│   │              is_enabled=True,                                           │ │
│   │              system_connection__is_active=True,                         │ │
│   │              system_connection__test_mode=context.test_mode             │ │
│   │          )                                                              │ │
│   │  else:                                                                  │ │
│   │      # OSS: User-specific brokered connections (for their overrides)    │ │
│   │      brokered_conns = BrokeredConnection.objects                        │ │
│   │          .with_effective_config()                                       │ │
│   │          .filter(                                                       │ │
│   │              created_by=context.user,                                   │ │
│   │              is_enabled=True,                                           │ │
│   │              system_connection__is_active=True,                         │ │
│   │              system_connection__test_mode=context.test_mode             │ │
│   │          )                                                              │ │
│   └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────────┐ │
│   │  Step 3: Convert to UnifiedConnection                                   │ │
│   │                                                                         │ │
│   │  connections = [                                                        │ │
│   │      UnifiedConnection.from_account(c) for c in account_conns           │ │
│   │  ] + [                                                                  │ │
│   │      UnifiedConnection.from_brokered(c) for c in brokered_conns         │ │
│   │  ]                                                                      │ │
│   └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────────┐ │
│   │  Step 4: Apply filters (carrier_code, capability, etc.)                 │ │
│   │                                                                         │ │
│   │  if carrier_code:                                                       │ │
│   │      connections = [c for c in connections                              │ │
│   │                     if c.carrier_code == carrier_code]                  │ │
│   │  if capability:                                                         │ │
│   │      connections = [c for c in connections                              │ │
│   │                     if capability in c.capabilities]                    │ │
│   └─────────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                         Return Connections                                     │
│                                                                               │
│   [                                                                           │
│       UnifiedConnection(id="car_xxx", carrier_code="fedex", ...),             │
│       UnifiedConnection(id="car_xxx", carrier_code="dhl_express", ...),       │
│   ]                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Sequence Diagram - Create Brokered Connection

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              SEQUENCE DIAGRAM: CREATE BROKERED CONNECTION                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────┐     ┌─────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────┐
│  User   │     │   API   │     │   Service    │     │ SystemConnection│     │ Database │
└────┬────┘     └────┬────┘     └──────┬───────┘     └───────┬────────┘     └────┬─────┘
     │               │                  │                     │                   │
     │ POST /v1/connections/brokered    │                     │                   │
     │ {                                │                     │                   │
     │   system_connection_id: "car_x", │                     │                   │
     │   config_overrides: {...}        │                     │                   │
     │ }                                │                     │                   │
     │──────────────►│                  │                     │                   │
     │               │                  │                     │                   │
     │               │ validate_request │                     │                   │
     │               │─────────────────►│                     │                   │
     │               │                  │                     │                   │
     │               │                  │ get_system_connection                   │
     │               │                  │────────────────────►│                   │
     │               │                  │                     │                   │
     │               │                  │                     │ SELECT * FROM     │
     │               │                  │                     │ system_connection │
     │               │                  │                     │ WHERE id = 'sys_x'│
     │               │                  │                     │──────────────────►│
     │               │                  │                     │                   │
     │               │                  │                     │◄──────────────────│
     │               │                  │                     │  SystemConnection │
     │               │                  │◄────────────────────│                   │
     │               │                  │                     │                   │
     │               │                  │ verify_active       │                   │
     │               │                  │ verify_not_duplicate                    │
     │               │                  │                     │                   │
     │               │                  │ create_brokered_connection              │
     │               │                  │─────────────────────────────────────────►
     │               │                  │                     │                   │
     │               │                  │                     │  INSERT INTO      │
     │               │                  │                     │  brokered_connection
     │               │                  │                     │  (id, system_connection_id,
     │               │                  │                     │   config_overrides,
     │               │                  │                     │   created_by, ...)│
     │               │                  │◄─────────────────────────────────────────
     │               │                  │                     │                   │
     │               │                  │ if MULTI_ORGANIZATIONS:                 │
     │               │                  │   create_link(org, brokered)            │
     │               │                  │─────────────────────────────────────────►
     │               │                  │                     │                   │
     │               │                  │◄─────────────────────────────────────────
     │               │                  │                     │                   │
     │               │◄─────────────────│                     │                   │
     │               │  BrokeredConnection                    │                   │
     │               │                  │                     │                   │
     │◄──────────────│                  │                     │                   │
     │ 201 Created   │                  │                     │                   │
     │ {             │                  │                     │                   │
     │   id: "car_x",│                  │                     │                   │
     │   carrier_code: "dhl_express",   │                     │                   │
     │   config: {...}                  │                     │                   │
     │ }             │                  │                     │                   │
     │               │                  │                     │                   │
```

### 6.4 Sequence Diagram - Rate Fetch with Mixed Connections

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              SEQUENCE DIAGRAM: RATE FETCH WITH MIXED CONNECTIONS                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────┐  ┌─────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐
│  User   │  │   API   │  │   Gateway    │  │ Connections  │  │  Carrier Gateways  │
└────┬────┘  └────┬────┘  └──────┬───────┘  └──────┬───────┘  └─────────┬──────────┘
     │            │               │                 │                    │
     │ POST /v1/rates             │                 │                    │
     │ { shipper, recipient, ... }│                 │                    │
     │───────────►│               │                 │                    │
     │            │               │                 │                    │
     │            │ Rates.fetch() │                 │                    │
     │            │──────────────►│                 │                    │
     │            │               │                 │                    │
     │            │               │ list(context,   │                    │
     │            │               │      capability="rating")            │
     │            │               │────────────────►│                    │
     │            │               │                 │                    │
     │            │               │                 │ Query Account +    │
     │            │               │                 │ Brokered with      │
     │            │               │                 │ single query each  │
     │            │               │                 │ (no N+1)           │
     │            │               │                 │                    │
     │            │               │◄────────────────│                    │
     │            │               │ [UnifiedConnection(...),             │
     │            │               │  UnifiedConnection(...)]             │
     │            │               │                 │                    │
     │            │               │                 │                    │
     │            │               │ For each connection:                 │
     │            │               │ ┌─────────────────────────────────┐  │
     │            │               │ │ conn.gateway = karrio.gateway   │  │
     │            │               │ │   [conn.carrier_code].create(   │  │
     │            │               │ │     conn.credentials,           │  │
     │            │               │ │     conn.config                 │  │
     │            │               │ │   )                             │  │
     │            │               │ └─────────────────────────────────┘  │
     │            │               │                 │                    │
     │            │               │ karrio.Rating.fetch(request)         │
     │            │               │   .from_(*gateways)                  │
     │            │               │─────────────────────────────────────►│
     │            │               │                 │                    │
     │            │               │                 │     ┌──────────────┴──────────────┐
     │            │               │                 │     │  Parallel API calls to:     │
     │            │               │                 │     │  - FedEx (AccountConnection)│
     │            │               │                 │     │  - DHL (BrokeredConnection  │
     │            │               │                 │     │        → SystemConnection)  │
     │            │               │                 │     └──────────────┬──────────────┘
     │            │               │                 │                    │
     │            │               │◄─────────────────────────────────────│
     │            │               │ [Rate(...), Rate(...), ...]          │
     │            │               │                 │                    │
     │            │◄──────────────│                 │                    │
     │            │ RateResponse  │                 │                    │
     │◄───────────│               │                 │                    │
     │ 200 OK     │               │                 │                    │
     │ { rates: [...] }           │                 │                    │
     │            │               │                 │                    │
```

### 6.5 Config Merge Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    CONFIG MERGE STRATEGY FOR BROKERED CONNECTIONS                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SystemConnection.config                                  │
│  (Base operational settings defined by admin)                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  {                                                                              │
│    "label_format": "ZPL",                  ← Platform default                   │
│    "label_size": "4x6",                    ← Platform default                   │
│    "default_package_type": "carrier_box",  ← Platform default                   │
│    "insurance_enabled": false,             ← Platform default                   │
│    "tracking_notifications": true,         ← Platform enforced                  │
│    "customs_signer": "Platform Inc"        ← Platform identity                  │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Base config
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      BrokeredConnection.config_overrides                         │
│  (User's operational customizations)                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│  {                                                                              │
│    "label_format": "PDF",                  ← User override                      │
│    "insurance_enabled": true,              ← User override                      │
│    "reference_prefix": "ACME-",            ← User addition                      │
│    "notification_email": "ship@acme.com"   ← User addition                      │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Merge (overrides win)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    BrokeredConnection.config                                     │
│  (Final config used at runtime - computed property)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  {                                                                              │
│    "label_format": "PDF",                  ← From override (wins)               │
│    "label_size": "4x6",                    ← From base                          │
│    "default_package_type": "carrier_box",  ← From base                          │
│    "insurance_enabled": true,              ← From override (wins)               │
│    "tracking_notifications": true,         ← From base                          │
│    "customs_signer": "Platform Inc",       ← From base                          │
│    "reference_prefix": "ACME-",            ← From override (added)              │
│    "notification_email": "ship@acme.com"   ← From override (added)              │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘

Merge Algorithm:
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  @property                                                                      │
│  def config(self) -> dict:                                                      │
│      base = dict(self.system_connection.config or {})                           │
│      overrides = dict(self.config_overrides or {})                              │
│      return {**base, **overrides}  # Simple merge, overrides win                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Capabilities Override Algorithm:
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  @property                                                                      │
│  def capabilities(self) -> list:                                                │
│      system_caps = list(self.system_connection.capabilities or [])              │
│      overrides = list(self.capabilities_overrides or [])                        │
│      # If overrides provided, use them; otherwise use system capabilities       │
│      return overrides if overrides else system_caps                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Note: Unlike config (which merges), capabilities are replaced entirely when
overridden. This allows organizations to enable/disable specific features
(e.g., disable "rating" capability for a brokered connection).
```

---

## 7. API Design

### 7.1 REST API (Unified Schema)

The REST API presents all connection types through a unified schema:

```yaml
# GET /v1/carriers
# Returns all connections accessible to the user

Response:
  - id: "car_xxx"
    carrier_code: "fedex"
    carrier_id: "my_fedex"
    carrier_name: "fedex"
    display_name: "My FedEx Account"
    capabilities: ["shipping", "rating", "tracking"]
    active: true
    test_mode: false
    metadata: {}
    # Note: credentials are NEVER exposed for brokered connections
    # Note: connection_type is internal only, not exposed via REST

# POST /v1/carriers
# Creates an AccountConnection (user-owned)
# Existing behavior preserved

# DELETE /v1/carriers/{id}
# Deletes AccountConnection or BrokeredConnection
# Cannot delete SystemConnection via this endpoint
```

### 7.2 GraphQL API (Separated Types)

GraphQL exposes the three types separately for more granular control:

```graphql
# Schema

type SystemConnection {
  id: ID!
  carrierCode: String!
  carrierId: String!
  displayName: String
  config: JSON!
  capabilities: [String!]!
  isActive: Boolean!
  testMode: Boolean!
  rateSheet: RateSheet
  metadata: JSON
  # Note: credentials NOT exposed
}

type AccountConnection {
  id: ID!
  carrierCode: String!
  carrierId: String!
  displayName: String
  credentials: JSON!  # Exposed for user-owned
  config: JSON!
  capabilities: [String!]!
  isActive: Boolean!
  testMode: Boolean!
  rateSheet: RateSheet
  metadata: JSON
  createdAt: DateTime!
  updatedAt: DateTime!
}

type BrokeredConnection {
  id: ID!
  systemConnection: SystemConnection!
  configOverrides: JSON!
  carrierId: String
  displayName: String
  isEnabled: Boolean!
  metadata: JSON

  # Computed fields
  carrierCode: String!       # From system
  effectiveConfig: JSON!     # Merged
  effectiveCarrierId: String!
  effectiveDisplayName: String!
  capabilities: [String!]!   # From system
  testMode: Boolean!         # From system
  rateSheet: RateSheet       # From system
  isActive: Boolean!         # is_enabled AND system.is_active
}

# Union for unified queries
union Connection = AccountConnection | BrokeredConnection

type Query {
  # Separated queries
  systemConnections(
    carrierCode: String
    isActive: Boolean
  ): [SystemConnection!]!

  accountConnections(
    carrierCode: String
    isActive: Boolean
  ): [AccountConnection!]!

  brokeredConnections(
    carrierCode: String
    isEnabled: Boolean
  ): [BrokeredConnection!]!

  # Unified query (for convenience)
  connections(
    carrierCode: String
    capability: String
  ): [Connection!]!
}

type Mutation {
  # Account connections (full CRUD)
  createAccountConnection(input: CreateAccountConnectionInput!): AccountConnection!
  updateAccountConnection(id: ID!, input: UpdateAccountConnectionInput!): AccountConnection!
  deleteAccountConnection(id: ID!): Boolean!

  # Brokered connections
  createBrokeredConnection(input: CreateBrokeredConnectionInput!): BrokeredConnection!
  updateBrokeredConnection(id: ID!, input: UpdateBrokeredConnectionInput!): BrokeredConnection!
  deleteBrokeredConnection(id: ID!): Boolean!

  # System connections (admin only)
  createSystemConnection(input: CreateSystemConnectionInput!): SystemConnection!
  updateSystemConnection(id: ID!, input: UpdateSystemConnectionInput!): SystemConnection!
  deleteSystemConnection(id: ID!): Boolean!
}

# Inputs

input CreateBrokeredConnectionInput {
  systemConnectionId: ID!
  configOverrides: JSON
  carrierId: String
  displayName: String
  metadata: JSON
}

input UpdateBrokeredConnectionInput {
  configOverrides: JSON
  carrierId: String
  displayName: String
  isEnabled: Boolean
  metadata: JSON
}
```

### 7.3 New gateway.Connections Class

```python
# karrio/server/core/gateway.py

class Connections:
    """
    Simplified connection resolution replacing the complex Carriers.list() method.
    """

    @staticmethod
    def list(
        context=None,
        carrier_code: str = None,
        carrier_id: str = None,
        capability: str = None,
        active_only: bool = True,
        **kwargs
    ) -> typing.List[UnifiedConnection]:
        """
        Get all connections accessible to the context (user/org).

        Returns AccountConnections + BrokeredConnections converted to
        UnifiedConnection for consistent interface.
        """
        from karrio.server.providers.models import (
            AccountConnection,
            BrokeredConnection,
        )

        test_mode = getattr(context, "test_mode", None)
        connections = []

        # Get account connections
        account_qs = Connections._get_account_queryset(context)
        if active_only:
            account_qs = account_qs.filter(is_active=True)
        if test_mode is not None:
            account_qs = account_qs.filter(test_mode=test_mode)
        if carrier_code:
            account_qs = account_qs.filter(carrier_code=carrier_code)
        if carrier_id:
            account_qs = account_qs.filter(carrier_id=carrier_id)
        if capability:
            account_qs = account_qs.filter(capabilities__icontains=capability)

        connections.extend([
            UnifiedConnection.from_account(c) for c in account_qs
        ])

        # Get brokered connections
        brokered_qs = Connections._get_brokered_queryset(context)
        if active_only:
            brokered_qs = brokered_qs.filter(
                is_enabled=True,
                system_connection__is_active=True
            )
        if test_mode is not None:
            brokered_qs = brokered_qs.filter(
                system_connection__test_mode=test_mode
            )
        if carrier_code:
            brokered_qs = brokered_qs.filter(
                system_connection__carrier_code=carrier_code
            )
        if carrier_id:
            brokered_qs = brokered_qs.filter(
                Q(carrier_id=carrier_id) |
                Q(carrier_id__isnull=True, system_connection__carrier_id=carrier_id)
            )
        if capability:
            brokered_qs = brokered_qs.filter(
                system_connection__capabilities__icontains=capability
            )

        connections.extend([
            UnifiedConnection.from_brokered(c) for c in brokered_qs
        ])

        return connections

    @staticmethod
    def _get_account_queryset(context):
        """Get account connections for context."""
        from karrio.server.providers.models import AccountConnection

        if settings.MULTI_ORGANIZATIONS and hasattr(context, "org") and context.org:
            # Insiders: Scoped to organization
            return AccountConnection.objects.filter(link__org=context.org)
        else:
            # OSS: All account connections are system-wide accessible
            return AccountConnection.objects.all()

    @staticmethod
    def _get_brokered_queryset(context):
        """Get brokered connections for context with optimized loading."""
        from karrio.server.providers.models import BrokeredConnection

        qs = BrokeredConnection.objects.with_effective_config()

        if settings.MULTI_ORGANIZATIONS and hasattr(context, "org") and context.org:
            # Insiders: Scoped to organization
            return qs.filter(link__org=context.org)
        elif hasattr(context, "user") and context.user:
            # OSS: User-specific brokered connections (for their config overrides)
            return qs.filter(created_by=context.user)
        return qs.none()

    @staticmethod
    def first(**kwargs) -> typing.Optional[UnifiedConnection]:
        """Get first matching connection."""
        connections = Connections.list(**kwargs)
        return connections[0] if connections else None
```

---

## 8. Migration Strategy

### 8.1 Migration Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            MIGRATION STRATEGY                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

Phase 1: Schema Changes (Reuse Existing Table)
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Rename Carrier model → AccountConnection (same table, new class name)       │
│  2. Add 'config' JSONField to AccountConnection (merge CarrierConfig)          │
│  3. Create NEW SystemConnection table                                           │
│  4. Create NEW BrokeredConnection table                                         │
│  5. Create BrokeredConnectionLink table (in orgs package - Insiders only)       │
│  6. Reuse existing CarrierLink → AccountConnectionLink (in orgs package)        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Phase 2: Data Migration (Pattern Detection)
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  Pattern Detection Rules:                                                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ SYSTEM-LIKE CARRIER (→ SystemConnection + BrokeredConnections)          │   │
│  │                                                                         │   │
│  │ Criteria:                                                               │   │
│  │   - is_system = True                                                    │   │
│  │   - created_by is staff/superuser                                       │   │
│  │   - has active_orgs or active_users entries                             │   │
│  │                                                                         │   │
│  │ Migration:                                                              │   │
│  │   1. MOVE carrier record to SystemConnection table                      │   │
│  │   2. DELETE from AccountConnection (old Carrier table)                  │   │
│  │   3. For each org in active_orgs:                                       │   │
│  │        Create BrokeredConnection linked to org                          │   │
│  │        If CarrierConfig exists for org:                                 │   │
│  │          Copy config → config_overrides                                 │   │
│  │   4. For each user in active_users (OSS):                               │   │
│  │        Create BrokeredConnection linked to user                         │   │
│  │        If CarrierConfig exists for user:                                │   │
│  │          Copy config → config_overrides                                 │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ USER-OWNED CARRIER (→ AccountConnection - stays in same table)          │   │
│  │                                                                         │   │
│  │ Criteria:                                                               │   │
│  │   - is_system = False                                                   │   │
│  │   - created_by is not staff OR has org link                             │   │
│  │                                                                         │   │
│  │ Migration:                                                              │   │
│  │   1. KEEP in AccountConnection table (no data move needed)              │   │
│  │   2. If CarrierConfig exists:                                           │   │
│  │        Merge config into AccountConnection.config field                 │   │
│  │   3. Keep existing org link                                             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Phase 3: Code Migration (Direct Cutover)
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Replace gateway.Carriers with new Connections class                        │
│  2. Update all serializers to use new models                                    │
│  3. Update GraphQL schemas to expose new types                                  │
│  4. Update admin interface for new models                                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Phase 4: Cleanup
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Remove is_system field from AccountConnection                              │
│  2. Remove active_users, active_orgs M2M fields                                │
│  3. Drop CarrierConfig table                                                    │
│  4. Drop CarrierConfigLink table                                                │
│  5. Remove old managers (CarrierManager, SystemCarrierManager)                  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Migration Script

```python
# karrio/server/providers/migrations/0xxx_migrate_to_connection_architecture.py

from django.db import migrations, connection
from django.conf import settings
from uuid import uuid4


def migrate_carriers_forward(apps, schema_editor):
    """
    Migrate Carrier + CarrierConfig to new connection architecture.

    Key approach:
    - AccountConnection REUSES the existing 'carrier' table (same db_table)
    - System-like carriers are MOVED to new 'system_connection' table
    - BrokeredConnections are created for each enabled org/user
    - CarrierConfig is merged into respective models
    """

    # Get model references (AccountConnection uses same table as Carrier)
    Carrier = apps.get_model("providers", "Carrier")  # Same as AccountConnection
    CarrierConfig = apps.get_model("providers", "CarrierConfig")
    SystemConnection = apps.get_model("providers", "SystemConnection")
    BrokeredConnection = apps.get_model("providers", "BrokeredConnection")

    if settings.MULTI_ORGANIZATIONS:
        BrokeredConnectionLink = apps.get_model("orgs", "BrokeredConnectionLink")

    # Step 1: Identify system-like carriers
    system_carrier_ids = []
    for carrier in Carrier.objects.all():
        if is_system_like(carrier):
            system_carrier_ids.append(carrier.id)

    # Step 2: Move system carriers to SystemConnection table
    for carrier_id in system_carrier_ids:
        carrier = Carrier.objects.get(id=carrier_id)

        # Create SystemConnection (MOVE data)
        system_conn = SystemConnection.objects.create(
            id=carrier.id,  # Keep same ID
            carrier_code=carrier.carrier_code,
            carrier_id=carrier.carrier_id,
            display_name=carrier.credentials.get("display_name"),
            credentials=carrier.credentials,
            config=get_merged_system_config(carrier, CarrierConfig),
            capabilities=carrier.capabilities,
            is_active=carrier.active,
            test_mode=carrier.test_mode,
            rate_sheet_id=carrier.rate_sheet_id,
            metadata=carrier.metadata,
        )

        # Create BrokeredConnections for each enabled org/user
        create_brokered_connections(
            apps, carrier, system_conn, CarrierConfig, BrokeredConnection
        )

        # DELETE from Carrier table (now that data is moved)
        carrier.delete()

    # Step 3: Merge CarrierConfig into remaining AccountConnections
    for carrier in Carrier.objects.all():  # Only non-system carriers remain
        config = CarrierConfig.objects.filter(carrier=carrier).first()
        if config:
            carrier.config = config.config
            carrier.save(update_fields=["config"])


def is_system_like(carrier):
    """Detect if carrier should become SystemConnection."""
    if carrier.is_system:
        return True

    # Check if created by staff
    if carrier.created_by and carrier.created_by.is_staff:
        # And has multiple orgs/users enabled
        if hasattr(carrier, "active_orgs") and carrier.active_orgs.exists():
            return True
        if hasattr(carrier, "active_users") and carrier.active_users.count() > 1:
            return True

    return False


def get_merged_system_config(carrier, CarrierConfig):
    """Get base config for system connection from staff-created CarrierConfig."""
    staff_config = CarrierConfig.objects.filter(
        carrier=carrier,
        created_by__is_staff=True,
    ).first()
    return staff_config.config if staff_config else {}


def create_brokered_connections(apps, carrier, system_conn, CarrierConfig, BrokeredConnection):
    """Create brokered connections for each enabled org/user."""
    if settings.MULTI_ORGANIZATIONS:
        BrokeredConnectionLink = apps.get_model("orgs", "BrokeredConnectionLink")

        for org in carrier.active_orgs.all():
            # Get org-specific config override
            org_config = CarrierConfig.objects.filter(
                carrier=carrier,
                link__org=org,
            ).first()

            brokered = BrokeredConnection.objects.create(
                id=f"car_{uuid4().hex}",
                system_connection=system_conn,
                config_overrides=org_config.config if org_config else {},
                is_enabled=True,
                metadata={
                    "migrated_from_carrier": carrier.id,
                    "migrated_from_org": org.id,
                },
            )

            BrokeredConnectionLink.objects.create(
                org=org,
                item=brokered,
            )
    else:
        # OSS: Create for active_users
        for user in carrier.active_users.all():
            user_config = CarrierConfig.objects.filter(
                carrier=carrier,
                created_by=user,
            ).first()

            BrokeredConnection.objects.create(
                id=f"car_{uuid4().hex}",
                system_connection=system_conn,
                config_overrides=user_config.config if user_config else {},
                is_enabled=True,
                created_by=user,
                metadata={
                    "migrated_from_carrier": carrier.id,
                    "migrated_from_user": user.id,
                },
            )


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0xxx_create_connection_models"),
    ]

    operations = [
        migrations.RunPython(
            migrate_carriers_forward,
            reverse_code=migrations.RunPython.noop,  # Manual rollback
        ),
    ]
```

### 8.3 Rollback Strategy

```python
# karrio/server/providers/management/commands/rollback_connection_migration.py

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Rollback connection migration if issues are detected"

    def handle(self, *args, **options):
        # 1. Verify no new data was created in new models
        # 2. Restore Carrier.is_system flags
        # 3. Restore CarrierConfig entries
        # 4. Delete new connection records
        # 5. Re-enable old code paths
        pass
```

---

## 9. Implementation Plan

### 9.1 Phase Breakdown

| Phase | Duration | Description |
|-------|----------|-------------|
| **Phase 1** | 1 week | Create new model files, migrations for tables |
| **Phase 2** | 1 week | Migration script development and testing |
| **Phase 3** | 2 weeks | Update gateway, serializers, GraphQL |
| **Phase 4** | 1 week | REST API updates and cleanup |
| **Phase 5** | 1 week | Integration testing, edge cases |
| **Phase 6** | 1 week | Staging deployment, monitoring |
| **Phase 7** | 1 week | Production rollout, cleanup |

### 9.2 Detailed Task List

**Phase 1: Model Creation**
- [ ] Create `SystemConnection` model
- [ ] Create `AccountConnection` model
- [ ] Create `BrokeredConnection` model
- [ ] Create Link tables for org association
- [ ] Create `UnifiedConnection` interface class
- [ ] Add model indexes and constraints
- [ ] Generate and run migrations

**Phase 2: Migration Script**
- [ ] Implement pattern detection logic
- [ ] Implement system carrier migration
- [ ] Implement account carrier migration
- [ ] Implement config merging logic
- [ ] Create rollback command
- [ ] Test migration on staging data

**Phase 3: Gateway Update**
- [ ] Create `Connections` class
- [ ] Implement `list()` method
- [ ] Implement `first()` method
- [ ] Update `Rates.fetch()` to use new connections
- [ ] Update `Shipments.create()` to use new connections
- [ ] Verify all code paths use new models

**Phase 4: API Update**
- [ ] Update REST serializers
- [ ] Add GraphQL types
- [ ] Add GraphQL queries
- [ ] Add GraphQL mutations
- [ ] Update admin interface

**Phase 5: Testing**
- [ ] Unit tests for new models
- [ ] Unit tests for migration
- [ ] Integration tests for gateway
- [ ] API contract tests
- [ ] Performance benchmarks

**Phase 6-7: Deployment**
- [ ] Deploy to staging
- [ ] Run migration on staging
- [ ] Verify data integrity
- [ ] Performance testing
- [ ] Deploy to production
- [ ] Monitor for issues
- [ ] Schedule cleanup migration

---

## 10. Testing Strategy

### 10.1 Unit Tests

```python
# tests/providers/test_connection_models.py

class TestBrokeredConnection:
    def test_config_merges_correctly(self):
        system = SystemConnectionFactory(
            config={"label_format": "ZPL", "insurance": False}
        )
        brokered = BrokeredConnectionFactory(
            system_connection=system,
            config_overrides={"label_format": "PDF", "ref_prefix": "X-"}
        )

        assert brokered.config == {
            "label_format": "PDF",      # Override wins
            "insurance": False,          # From base
            "ref_prefix": "X-",          # Added
        }

    def test_credentials_always_returns_none(self):
        """Brokered connection never exposes system credentials."""
        system = SystemConnectionFactory(
            credentials={"api_key": "secret"}
        )
        brokered = BrokeredConnectionFactory(system_connection=system)

        # Credentials are never exposed through brokered connection
        assert brokered.credentials is None
        # But system connection has them (for gateway internal use)
        assert brokered.system_connection.credentials == {"api_key": "secret"}

    def test_capabilities_with_overrides(self):
        """Capabilities can be overridden per brokered connection."""
        system = SystemConnectionFactory(
            capabilities=["shipping", "tracking", "rating"]
        )
        brokered = BrokeredConnectionFactory(
            system_connection=system,
            capabilities_overrides=["shipping", "tracking"]  # Rating disabled
        )

        assert brokered.capabilities == ["shipping", "tracking"]

    def test_capabilities_fallback_to_system(self):
        """Without overrides, use system capabilities."""
        system = SystemConnectionFactory(
            capabilities=["shipping", "tracking", "rating"]
        )
        brokered = BrokeredConnectionFactory(
            system_connection=system,
            capabilities_overrides=[]  # No overrides
        )

        assert brokered.capabilities == ["shipping", "tracking", "rating"]

    def test_is_active_requires_both_enabled_and_system_active(self):
        system = SystemConnectionFactory(is_active=True)
        brokered = BrokeredConnectionFactory(
            system_connection=system,
            is_enabled=True
        )
        assert brokered.is_active is True

        system.is_active = False
        system.save()
        brokered.refresh_from_db()
        assert brokered.is_active is False


class TestConnectionsList:
    def test_oss_returns_all_account_connections(self):
        """In OSS, all account connections are accessible to any user."""
        user1 = UserFactory()
        user2 = UserFactory()
        account1 = AccountConnectionFactory(created_by=user1)
        account2 = AccountConnectionFactory(created_by=user2)

        # user2 can see account1 (created by user1) in OSS
        context = MockContext(user=user2)
        connections = Connections.list(context=context)

        assert len(connections) == 2
        assert any(c.id == account1.id for c in connections)
        assert any(c.id == account2.id for c in connections)

    def test_returns_account_and_brokered_connections(self):
        user = UserFactory()
        account = AccountConnectionFactory(created_by=user)
        system = SystemConnectionFactory()
        brokered = BrokeredConnectionFactory(
            system_connection=system,
            created_by=user
        )

        context = MockContext(user=user)
        connections = Connections.list(context=context)

        assert len(connections) == 2
        assert any(c.id == account.id for c in connections)
        assert any(c.id == brokered.id for c in connections)

    def test_filters_by_capability(self):
        user = UserFactory()
        account = AccountConnectionFactory(
            created_by=user,
            capabilities=["shipping", "rating"]
        )

        context = MockContext(user=user)

        # Should find
        connections = Connections.list(context=context, capability="rating")
        assert len(connections) == 1

        # Should not find
        connections = Connections.list(context=context, capability="tracking")
        assert len(connections) == 0
```

### 10.2 Migration Tests

```python
# tests/providers/test_migration.py

class TestCarrierMigration:
    def test_system_carrier_creates_system_connection(self):
        carrier = CarrierFactory(
            is_system=True,
            carrier_code="dhl_express",
            credentials={"api_key": "xxx"},
        )

        run_migration()

        system = SystemConnection.objects.get(
            carrier_code="dhl_express"
        )
        assert system.credentials == {"api_key": "xxx"}

    def test_system_carrier_creates_brokered_for_each_org(self):
        carrier = CarrierFactory(is_system=True)
        org1 = OrganizationFactory()
        org2 = OrganizationFactory()
        carrier.active_orgs.add(org1, org2)

        run_migration()

        brokered_conns = BrokeredConnection.objects.filter(
            system_connection__carrier_code=carrier.carrier_code
        )
        assert brokered_conns.count() == 2

    def test_carrier_config_becomes_config_overrides(self):
        carrier = CarrierFactory(is_system=True)
        org = OrganizationFactory()
        carrier.active_orgs.add(org)

        CarrierConfigFactory(
            carrier=carrier,
            config={"label_format": "PDF"},
            org=org,
        )

        run_migration()

        brokered = BrokeredConnection.objects.get(link__org=org)
        assert brokered.config_overrides == {"label_format": "PDF"}
```

### 10.3 Performance Benchmarks

```python
# tests/providers/test_performance.py

class TestQueryPerformance:
    def test_no_n_plus_one_for_brokered_connections(self):
        # Create 100 brokered connections
        system = SystemConnectionFactory()
        for _ in range(100):
            BrokeredConnectionFactory(system_connection=system)

        # Should be 1-2 queries, not 100+
        with self.assertNumQueries(2):
            connections = Connections.list(context=context)
            for conn in connections:
                _ = conn.config
                _ = conn.rate_sheet
```

---

## 11. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss during migration | Low | Critical | Backup before migration, dry-run on staging |
| API breaking changes | Medium | High | Unified interface, comprehensive API tests |
| Performance regression | Medium | Medium | Benchmark tests, query optimization |
| Missing edge cases in migration | Medium | Medium | Thorough pattern analysis, manual verification |
| Rollback complexity | Low | High | Keep old tables until verification complete |

---

## 12. Rollout Plan

### 12.1 Rollout Stages

1. **Week 1-2**: Development and code review
2. **Week 3**: Deploy to staging, run migration
3. **Week 4**: QA testing on staging
4. **Week 5**: Production deployment (read-only migration first)
5. **Week 6**: Enable write path, monitor
6. **Week 7-8**: Cleanup and verification

### 12.2 Monitoring

- Query performance metrics
- Error rates for carrier operations
- Data integrity checks (counts, references)
- User-reported issues

---

## Appendix A: Database Schema Changes

```sql
-- New tables

CREATE TABLE system_connection (
    id VARCHAR(50) PRIMARY KEY,
    carrier_code VARCHAR(100) NOT NULL,
    carrier_id VARCHAR(150) NOT NULL,
    display_name VARCHAR(200),
    credentials JSONB NOT NULL DEFAULT '{}',
    config JSONB NOT NULL DEFAULT '{}',
    capabilities VARCHAR(500)[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    test_mode BOOLEAN DEFAULT TRUE,
    rate_sheet_id VARCHAR(50) REFERENCES rate_sheet(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- AccountConnection REUSES existing 'carrier' table
-- Only schema changes needed:
ALTER TABLE carrier ADD COLUMN IF NOT EXISTS config JSONB DEFAULT '{}';

-- Post-migration cleanup (remove columns no longer needed):
ALTER TABLE carrier DROP COLUMN IF EXISTS is_system;
ALTER TABLE carrier DROP COLUMN IF EXISTS active_users;
ALTER TABLE carrier DROP COLUMN IF EXISTS active_orgs;

CREATE TABLE brokered_connection (
    id VARCHAR(50) PRIMARY KEY,
    system_connection_id VARCHAR(50) NOT NULL REFERENCES system_connection(id),
    config_overrides JSONB DEFAULT '{}',
    carrier_id VARCHAR(150),
    display_name VARCHAR(200),
    is_enabled BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES auth_user(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Link tables (defined in orgs package - Insiders only)
-- These tables are only created in Insiders builds with MULTI_ORGANIZATIONS=True

-- AccountConnectionLink REUSES existing 'carrier_link' table (renamed model only)
-- No schema change needed for carrier_link table
-- Location: karrio/server/orgs/models.py

-- BrokeredConnectionLink (NEW - in orgs package)
-- Location: karrio/server/orgs/models.py
CREATE TABLE brokered_connection_link (
    id SERIAL PRIMARY KEY,
    org_id VARCHAR(50) NOT NULL REFERENCES organization(id),
    item_id VARCHAR(50) NOT NULL UNIQUE REFERENCES brokered_connection(id)
);

-- Indexes

CREATE INDEX idx_system_conn_carrier ON system_connection(carrier_code, is_active);
-- carrier table already has indexes
CREATE INDEX idx_brokered_conn_system ON brokered_connection(system_connection_id, is_enabled);
```

---

## Appendix B: Migration Mapping

| Old Model/Field | New Model/Field | Notes |
|-----------------|-----------------|-------|
| `Carrier` table | `AccountConnection` | **Same table** (reused, renamed model) |
| `Carrier` (is_system=True) | `SystemConnection` | **Moved** to new table |
| `Carrier` (is_system=False) | `AccountConnection` | **Stays** in same table |
| `Carrier.credentials` | `AccountConnection.credentials` | Same column |
| `Carrier.is_system` | N/A | **Removed** (type is implicit by model) |
| `Carrier.active_orgs` | `BrokeredConnection` per org | **Removed** (replaced by brokered links) |
| `Carrier.active_users` | `BrokeredConnection` per user | **Removed** (replaced by brokered links) |
| `CarrierConfig.config` | `AccountConnection.config` or `BrokeredConnection.config_overrides` | **Merged** into connection |
| `CarrierLink` | `AccountConnectionLink` | **Renamed** (same table, in orgs package) |
| `CarrierConfigLink` | N/A | **Dropped** (merged into BrokeredConnection) |
| `CarrierConfig` table | N/A | **Dropped** (merged into connections) |

---

*Document End*
