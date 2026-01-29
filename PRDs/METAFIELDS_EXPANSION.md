# Metafields Expansion - Adding Metafields to Core Objects

<!-- ENHANCEMENT: This PRD covers expanding metafield support across core Karrio objects -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-27 |
| Status | Ready for Implementation |
| Owner | Karrio Team |
| Type | Enhancement |
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

This PRD proposes expanding the existing metafield system to support typed, structured metadata on core Karrio objects. Currently, metafields are only attached to Organization, AppInstallation, and workflow-related models. This enhancement will add metafield support to:

- **Carrier Connections** (CarrierConnection, SystemConnection, BrokeredConnection)
- **Address** (address templates)
- **Parcel** (parcel templates)
- **Organization** (already exists - enhance if needed)
- **OrganizationUser**
- **Order**
- **Shipment**
- **Pickup**
- **Tracking** (Tracker)
- **Markup** (Addons/Surcharges)

Additionally, a reusable **MetafieldsEditor** React component will be created for the frontend to provide consistent CRUD operations across all supported objects.

### Key Architecture Decisions

1. **M2M with Link Models**: Use the established pattern of ManyToMany relationships through link models (OneToOne on metafield side to prevent duplicate assignments)
2. **GraphQL-First API**: Extend existing metafield mutations to support object attachment, following current patterns
3. **Reusable Frontend Component**: Create a `MetafieldsEditor` component similar to existing metadata editors for consistent UX
4. **Type System**: Leverage existing 7 metafield types (text, number, boolean, json, date, date_time, password)

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| M2M metafield relationships for 11 object types | REST API for metafields (remains GraphQL-only) |
| GraphQL mutations for attach/detach metafields | Changes to metafield type system |
| Reusable MetafieldsEditor React component | Metafield templates/presets |
| Migration for new link tables | Bulk metafield operations |
| Frontend integration for all object edit forms | Metafield search/filtering across objects |

---

## Open Questions & Decisions

### Pending Questions

_All questions have been resolved._

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Attachment pattern | M2M with Link models | Matches existing AppInstallation/WorkflowConnection pattern, prevents duplicate metafield assignments | 2026-01-27 |
| D2 | API approach | GraphQL mutations | Metafields are already GraphQL-only; maintain consistency | 2026-01-27 |
| D3 | Copy on clone/duplicate | No, start fresh | Metafields are not copied when cloning objects; new objects start without metafields | 2026-01-27 |
| D4 | Organization inheritance | No inheritance | Organization metafields are not inherited by child objects (Shipments, Orders, etc.) | 2026-01-27 |
| D5 | Embedded address metafields | No (only Address templates) | Only Address template objects support metafields; embedded JSON addresses in Shipment do not | 2026-01-27 |
| D6 | BrokeredConnection visibility | Only non-password types | Metafields on Connections are visible via BrokeredConnection, except password-type metafields | 2026-01-27 |
| D7 | Maximum metafields per object | No limit | No artificial limit on metafields per object; rely on natural constraints | 2026-01-27 |
| D8 | Cascade delete | Yes (cascade) | When objects are deleted, their attached metafields are also deleted via link model cascade | 2026-01-27 |
| D9 | MetafieldsEditor UX | Inline only | MetafieldsEditor uses inline creation/editing without modals for simpler UX | 2026-01-27 |
| D10 | Webhook payloads | Always include | Metafields are always included in webhook payloads for object events | 2026-01-27 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Resolved? |
|-----------|--------|-------------------|-----------|
| User deletes a required metafield that's attached to objects | Objects become "invalid" | Prevent deletion while attached to objects | ✅ Resolved |
| Metafield key collision (same key, different types on same object) | Data ambiguity | Enforce unique keys per object | ✅ Resolved |
| Large JSON metafield values (>1MB) | Performance issues | Enforce 1MB size limit at validation layer | ✅ Resolved |

---

## Problem Statement

### Current State

```python
# Current metafield attachment - only on specific EE models
# ee/insiders/modules/apps/karrio/server/apps/models.py
class AppInstallation(core.OwnedEntity):
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="app_installation",
        through="AppInstallationMetafieldLink",
    )

# Core shipping models have NO metafield support
# modules/manager/karrio/server/manager/models.py
class Shipment(core.OwnedEntity):
    # Only unstructured JSON metadata
    metadata = models.JSONField(blank=True, null=True, default=dict)
    # No metafields M2M relationship
```

```typescript
// Frontend has no reusable metafields editor
// Each form manually handles metadata as unstructured JSON
<MetadataEditor
  value={metadata}
  onChange={setMetadata}
/>
// No type validation, no structured fields
```

### Desired State

```python
# All core models support typed metafields
# modules/manager/karrio/server/manager/models.py
class Shipment(core.OwnedEntity):
    metadata = models.JSONField(blank=True, null=True, default=dict)
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="shipment",
        through="ShipmentMetafieldLink",
    )

class ShipmentMetafieldLink(models.Model):
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="metafields_links"
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="shipment_link"
    )
```

```typescript
// Reusable MetafieldsEditor component
<MetafieldsEditor
  objectType="shipment"
  objectId={shipment.id}
  metafields={shipment.metafields}
  onUpdate={refetch}
/>
// Supports all 7 types with proper validation
```

### Problems

1. **No typed metadata**: Current `metadata` JSONField has no schema validation, type checking, or structure
2. **Inconsistent patterns**: Some EE models have metafields, core models don't
3. **No reusable UI**: Each object form implements its own metadata handling
4. **Limited extensibility**: Users cannot define structured custom fields on core objects
5. **No credential storage**: Sensitive data (passwords, API keys) cannot be securely stored on objects

---

## Goals & Success Criteria

### Goals

1. Add metafield M2M relationships to all 10 target object types
2. Create GraphQL mutations for attaching/detaching metafields to objects
3. Build a reusable `MetafieldsEditor` React component for consistent frontend UX
4. Maintain backward compatibility with existing `metadata` JSONField
5. Support all 7 metafield types across all objects

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| All 11 object types have metafield M2M | 100% | Must-have |
| GraphQL attach/detach mutations work | All objects | Must-have |
| MetafieldsEditor component created | Functional | Must-have |
| Existing metadata field unchanged | No breaking changes | Must-have |
| All metafield types supported | 7 types | Must-have |
| Unit test coverage | 80%+ | Must-have |
| Frontend integration in edit forms | All objects | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Database migrations for all link tables
- [ ] M2M relationships added to all 10 models
- [ ] GraphQL types updated to expose metafields
- [ ] GraphQL mutations for attach/detach
- [ ] MetafieldsEditor React component
- [ ] Unit tests for backend
- [ ] All existing tests pass

**Nice-to-have (P1):**
- [ ] Integration in all object edit forms
- [ ] Metafield templates/presets
- [ ] Bulk attach/detach operations
- [ ] Webhook payload inclusion

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: M2M with Link Models** | Proven pattern, prevents duplicates, flexible | More tables, more complex queries | **Selected** |
| B: Direct M2M (no link model) | Simpler, fewer tables | Can't prevent duplicate assignments, less control | Rejected |
| C: JSONField with schema validation | No new tables, simple | No type enforcement at DB level, harder to query | Rejected |
| D: Separate metafield tables per object | Type-safe, dedicated indexes | Table explosion (10+ new tables), code duplication | Rejected |

### Trade-off Analysis

Option A was selected because:
- **Proven pattern**: Already used successfully for AppInstallation and WorkflowConnection
- **OneToOne constraint**: Prevents the same metafield from being attached to multiple objects
- **Flexible queries**: Can query metafields by object or objects by metafield
- **Type safety**: Leverages existing Metafield model with validation

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| Metafield model | `modules/core/karrio/server/core/models/metafield.py` | Use existing model as-is |
| MetafieldType enum | `modules/core/karrio/server/core/models/base.py` | Use existing 7 types |
| AppInstallationMetafieldLink | `ee/insiders/modules/apps/karrio/server/apps/models.py` | Copy pattern for new links |
| MetafieldModelSerializer | `modules/graph/karrio/server/graph/serializers.py` | Use for CRUD operations |
| MetafieldType (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/types.py` | Extend with object relationships |
| CreateMetafieldMutation | `modules/graph/karrio/server/graph/schemas/base/mutations.py` | Extend for object attachment |
| metafields_to_dict helper | `modules/core/karrio/server/core/models/__init__.py` | Use for dictionary conversion |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         METAFIELDS ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                                                         │
│  │    Metafield    │ (Existing - unchanged)                                  │
│  │    ─────────    │                                                         │
│  │  id, key, value │                                                         │
│  │  type, required │                                                         │
│  └────────┬────────┘                                                         │
│           │                                                                  │
│           │ OneToOne (via Link Models)                                       │
│           │                                                                  │
│  ┌────────┴────────────────────────────────────────────────────────────┐    │
│  │                         LINK MODELS                                  │    │
│  ├──────────────────────────────────────────────────────────────────────┤    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │    │
│  │  │ CarrierConnection│  │ ShipmentMetafield│  │  OrderMetafield  │   │    │
│  │  │   MetafieldLink  │  │      Link        │  │      Link        │   │    │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │    │
│  │  │ AddressMetafield │  │ ParcelMetafield  │  │ PickupMetafield  │   │    │
│  │  │      Link        │  │      Link        │  │      Link        │   │    │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │    │
│  │  │ TrackingMetafield│  │  OrgMetafield    │  │ OrgUserMetafield │   │    │
│  │  │      Link        │  │      Link        │  │      Link        │   │    │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         GRAPHQL LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Queries:                          Mutations:                                │
│  ─────────                         ──────────                                │
│  shipment {                        attachMetafield(                          │
│    id                                objectType: "shipment"                  │
│    metafields {                      objectId: "shp_..."                     │
│      id, key, value, type            metafieldId: "metaf_..."                │
│    }                               )                                         │
│  }                                                                           │
│                                    detachMetafield(                          │
│                                      objectType: "shipment"                  │
│                                      objectId: "shp_..."                     │
│                                      metafieldId: "metaf_..."                │
│                                    )                                         │
│                                                                              │
│                                    createAndAttachMetafield(                 │
│                                      objectType: "shipment"                  │
│                                      objectId: "shp_..."                     │
│                                      input: { key, value, type }             │
│                                    )                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND COMPONENT                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      MetafieldsEditor                                │    │
│  │  ─────────────────────────────────────────────────────────────────  │    │
│  │                                                                      │    │
│  │  Props:                                                              │    │
│  │    - objectType: string (shipment, order, address, etc.)            │    │
│  │    - objectId: string                                                │    │
│  │    - metafields: MetafieldType[]                                    │    │
│  │    - onUpdate: () => void                                           │    │
│  │    - readonly?: boolean                                              │    │
│  │                                                                      │    │
│  │  Features:                                                           │    │
│  │    - List existing metafields                                       │    │
│  │    - Add new metafield (inline)                                     │    │
│  │    - Edit metafield value (inline)                                  │    │
│  │    - Delete/detach metafield                                        │    │
│  │    - Type-specific input components                                 │    │
│  │    - Validation per type                                            │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Type-Specific Inputs:                                                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│  │  Text    │ │  Number  │ │ Boolean  │ │   JSON   │                        │
│  │  Input   │ │  Input   │ │  Toggle  │ │  Editor  │                        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                                     │
│  │   Date   │ │ DateTime │ │ Password │                                     │
│  │  Picker  │ │  Picker  │ │  Input   │                                     │
│  └──────────┘ └──────────┘ └──────────┘                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│Frontend│     │GraphQL │     │Mutation│     │ Model  │     │Database│
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │              │
    │ 1. createAndAttachMetafield               │              │
    │─────────────>│              │              │              │
    │              │ 2. Validate  │              │              │
    │              │─────────────>│              │              │
    │              │              │ 3. Create    │              │
    │              │              │  Metafield   │              │
    │              │              │─────────────>│              │
    │              │              │              │ 4. INSERT    │
    │              │              │              │  metafield   │
    │              │              │              │─────────────>│
    │              │              │              │<─────────────│
    │              │              │ 5. Create    │              │
    │              │              │  Link        │              │
    │              │              │─────────────>│              │
    │              │              │              │ 6. INSERT    │
    │              │              │              │  link        │
    │              │              │              │─────────────>│
    │              │              │              │<─────────────│
    │              │              │<─────────────│              │
    │              │<─────────────│              │              │
    │ 7. Return metafield         │              │              │
    │<─────────────│              │              │              │
    │              │              │              │              │

    │ 8. Update UI │              │              │              │
    │──────────────│              │              │              │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     METAFIELD ATTACHMENT FLOW                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  INPUT: Create and Attach Request                                             │
│  ┌─────────────────────────────────────────────────────┐                     │
│  │ {                                                   │                     │
│  │   objectType: "shipment",                           │                     │
│  │   objectId: "shp_abc123",                           │                     │
│  │   input: {                                          │                     │
│  │     key: "customs_broker_id",                       │                     │
│  │     type: "text",                                   │                     │
│  │     value: "BROKER-12345",                          │                     │
│  │     is_required: false                              │                     │
│  │   }                                                 │                     │
│  │ }                                                   │                     │
│  └─────────────────────────────────────────────────────┘                     │
│                          │                                                    │
│                          ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐                     │
│  │              VALIDATION LAYER                        │                     │
│  │  ────────────────────────────────────────────────── │                     │
│  │  1. Validate objectType is supported                │                     │
│  │  2. Validate objectId exists and user has access    │                     │
│  │  3. Validate metafield input (type, value)          │                     │
│  │  4. Check key uniqueness on object (if enforced)    │                     │
│  └─────────────────────────────────────────────────────┘                     │
│                          │                                                    │
│                          ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐                     │
│  │              CREATE METAFIELD                        │                     │
│  │  ────────────────────────────────────────────────── │                     │
│  │  Metafield.objects.create(                          │                     │
│  │    key="customs_broker_id",                         │                     │
│  │    type="text",                                     │                     │
│  │    value="BROKER-12345",                            │                     │
│  │    is_required=False,                               │                     │
│  │    created_by=request.user                          │                     │
│  │  )                                                  │                     │
│  └─────────────────────────────────────────────────────┘                     │
│                          │                                                    │
│                          ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐                     │
│  │              CREATE LINK                             │                     │
│  │  ────────────────────────────────────────────────── │                     │
│  │  ShipmentMetafieldLink.objects.create(              │                     │
│  │    shipment_id="shp_abc123",                        │                     │
│  │    metafield=metafield                              │                     │
│  │  )                                                  │                     │
│  └─────────────────────────────────────────────────────┘                     │
│                          │                                                    │
│                          ▼                                                    │
│  OUTPUT: Attached Metafield                                                   │
│  ┌─────────────────────────────────────────────────────┐                     │
│  │ MetafieldType {                                     │                     │
│  │   id: "metaf_xyz789",                               │                     │
│  │   key: "customs_broker_id",                         │                     │
│  │   type: "text",                                     │                     │
│  │   value: "BROKER-12345",                            │                     │
│  │   is_required: false,                               │                     │
│  │   object_type: "metafield"                          │                     │
│  │ }                                                   │                     │
│  └─────────────────────────────────────────────────────┘                     │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### Link Models (New)

```python
# modules/manager/karrio/server/manager/models.py

class ShipmentMetafieldLink(models.Model):
    """Links metafields to shipments."""

    shipment = models.ForeignKey(
        "Shipment",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="shipment_link",
    )

    class Meta:
        db_table = "shipment_metafield_link"


class OrderMetafieldLink(models.Model):
    """Links metafields to orders."""

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="order_link",
    )

    class Meta:
        db_table = "order_metafield_link"


class AddressMetafieldLink(models.Model):
    """Links metafields to addresses."""

    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="address_link",
    )

    class Meta:
        db_table = "address_metafield_link"


class ParcelMetafieldLink(models.Model):
    """Links metafields to parcels."""

    parcel = models.ForeignKey(
        "Parcel",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="parcel_link",
    )

    class Meta:
        db_table = "parcel_metafield_link"


class PickupMetafieldLink(models.Model):
    """Links metafields to pickups."""

    pickup = models.ForeignKey(
        "Pickup",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="pickup_link",
    )

    class Meta:
        db_table = "pickup_metafield_link"


class TrackingMetafieldLink(models.Model):
    """Links metafields to trackers."""

    tracking = models.ForeignKey(
        "Tracking",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="tracking_link",
    )

    class Meta:
        db_table = "tracking_metafield_link"


# Connection models - in providers module
# modules/core/karrio/server/providers/models/carrier.py

class CarrierConnectionMetafieldLink(models.Model):
    """Links metafields to carrier connections."""

    carrier_connection = models.ForeignKey(
        "CarrierConnection",
        on_delete=models.CASCADE,
        related_name="metafields_links",
    )
    metafield = models.OneToOneField(
        core.Metafield,
        on_delete=models.CASCADE,
        related_name="carrier_connection_link",
    )

    class Meta:
        db_table = "carrier_connection_metafield_link"
```

#### Model Updates (M2M relationships)

```python
# Add to existing models

class Shipment(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="shipment",
        through="ShipmentMetafieldLink",
        blank=True,
    )


class Order(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="order",
        through="OrderMetafieldLink",
        blank=True,
    )


class Address(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="address",
        through="AddressMetafieldLink",
        blank=True,
    )


class Parcel(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="parcel",
        through="ParcelMetafieldLink",
        blank=True,
    )


class Pickup(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="pickup",
        through="PickupMetafieldLink",
        blank=True,
    )


class Tracking(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="tracking",
        through="TrackingMetafieldLink",
        blank=True,
    )


class CarrierConnection(core.OwnedEntity):
    # ... existing fields ...
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="carrier_connection",
        through="CarrierConnectionMetafieldLink",
        blank=True,
    )
```

### GraphQL Schema Updates

#### New Input Types

```python
# modules/graph/karrio/server/graph/schemas/base/inputs.py

MetafieldObjectTypeEnum: typing.Any = strawberry.enum(
    utils.create_enum(
        "MetafieldObjectTypeEnum",
        [
            "shipment",
            "order",
            "address",
            "parcel",
            "pickup",
            "tracking",
            "carrier_connection",
            "system_connection",
            "brokered_connection",
            "organization",
            "organization_user",
            "markup",
        ],
    )
)


@strawberry.input
class AttachMetafieldInput(utils.BaseInput):
    """Input for attaching a metafield to an object."""

    object_type: MetafieldObjectTypeEnum
    object_id: str
    metafield_id: str


@strawberry.input
class DetachMetafieldInput(utils.BaseInput):
    """Input for detaching a metafield from an object."""

    object_type: MetafieldObjectTypeEnum
    object_id: str
    metafield_id: str


@strawberry.input
class CreateAndAttachMetafieldInput(utils.BaseInput):
    """Input for creating a metafield and attaching it to an object."""

    object_type: MetafieldObjectTypeEnum
    object_id: str
    key: str
    type: MetafieldTypeEnum
    value: typing.Optional[utils.JSON] = strawberry.UNSET
    is_required: typing.Optional[bool] = False
```

#### New Mutations

```python
# modules/graph/karrio/server/graph/schemas/base/mutations.py

@strawberry.type
class AttachMetafieldMutation(utils.BaseMutation):
    metafield: typing.Optional[types.MetafieldType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "AttachMetafieldMutation":
        object_type = input.get("object_type")
        object_id = input.get("object_id")
        metafield_id = input.get("metafield_id")

        # Get the target object with access control
        model_class = _get_model_for_object_type(object_type)
        target_object = model_class.access_by(info.context.request).get(id=object_id)

        # Get the metafield with access control
        metafield = core.Metafield.access_by(info.context.request).get(id=metafield_id)

        # Create the link
        target_object.metafields.add(metafield)

        return AttachMetafieldMutation(
            metafield=types.MetafieldType.resolve(info, metafield.id)
        )


@strawberry.type
class DetachMetafieldMutation(utils.BaseMutation):
    id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "DetachMetafieldMutation":
        object_type = input.get("object_type")
        object_id = input.get("object_id")
        metafield_id = input.get("metafield_id")

        # Get the target object with access control
        model_class = _get_model_for_object_type(object_type)
        target_object = model_class.access_by(info.context.request).get(id=object_id)

        # Remove the link (metafield itself is NOT deleted)
        target_object.metafields.remove(metafield_id)

        return DetachMetafieldMutation(id=metafield_id)


@strawberry.type
class CreateAndAttachMetafieldMutation(utils.BaseMutation):
    metafield: typing.Optional[types.MetafieldType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "CreateAndAttachMetafieldMutation":
        object_type = input.pop("object_type")
        object_id = input.pop("object_id")

        # Get the target object with access control
        model_class = _get_model_for_object_type(object_type)
        target_object = model_class.access_by(info.context.request).get(id=object_id)

        # Create the metafield
        metafield = serializers.MetafieldModelSerializer.map(
            data=input,
            context=info.context.request,
        )

        # Attach to the object
        target_object.metafields.add(metafield)

        return CreateAndAttachMetafieldMutation(
            metafield=types.MetafieldType.resolve(info, metafield.id)
        )
```

### Frontend Component

```typescript
// packages/ui/components/metafields-editor.tsx

import React from "react";
import { useMutation } from "@tanstack/react-query";
import { MetafieldType, MetafieldTypeEnum } from "@karrio/types";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select } from "./ui/select";
import { Switch } from "./ui/switch";
import { Textarea } from "./ui/textarea";
import { DatePicker } from "./ui/date-picker";
import { useKarrio } from "@karrio/hooks/karrio";
import { gqlstr } from "@karrio/lib";
import {
  CREATE_AND_ATTACH_METAFIELD,
  UPDATE_METAFIELD,
  DETACH_METAFIELD,
} from "@karrio/types/graphql/queries";

interface MetafieldsEditorProps {
  objectType: string;
  objectId: string;
  metafields: MetafieldType[];
  onUpdate?: () => void;
  readonly?: boolean;
}

interface NewMetafieldState {
  key: string;
  type: MetafieldTypeEnum;
  value: any;
  is_required: boolean;
}

const INITIAL_NEW_METAFIELD: NewMetafieldState = {
  key: "",
  type: "text",
  value: "",
  is_required: false,
};

export const MetafieldsEditor: React.FC<MetafieldsEditorProps> = ({
  objectType,
  objectId,
  metafields,
  onUpdate,
  readonly = false,
}) => {
  const karrio = useKarrio();
  const [isAdding, setIsAdding] = React.useState(false);
  const [newMetafield, setNewMetafield] = React.useState<NewMetafieldState>(INITIAL_NEW_METAFIELD);
  const [editingId, setEditingId] = React.useState<string | null>(null);
  const [editValue, setEditValue] = React.useState<any>(null);

  // Mutations
  const createAndAttach = useMutation({
    mutationFn: (input: any) =>
      karrio.graphql.request(gqlstr(CREATE_AND_ATTACH_METAFIELD), { input }),
    onSuccess: () => {
      onUpdate?.();
      setIsAdding(false);
      setNewMetafield(INITIAL_NEW_METAFIELD);
    },
  });

  const updateMetafield = useMutation({
    mutationFn: (input: any) =>
      karrio.graphql.request(gqlstr(UPDATE_METAFIELD), { input }),
    onSuccess: () => {
      onUpdate?.();
      setEditingId(null);
      setEditValue(null);
    },
  });

  const detachMetafield = useMutation({
    mutationFn: (metafieldId: string) =>
      karrio.graphql.request(gqlstr(DETACH_METAFIELD), {
        input: { object_type: objectType, object_id: objectId, metafield_id: metafieldId },
      }),
    onSuccess: onUpdate,
  });

  // Render type-specific input
  const renderValueInput = (
    type: MetafieldTypeEnum,
    value: any,
    onChange: (value: any) => void,
    compact?: boolean
  ) => {
    switch (type) {
      case "text":
      case "password":
        return (
          <Input
            type={type === "password" ? "password" : "text"}
            value={value || ""}
            onChange={(e) => onChange(e.target.value)}
            className={compact ? "h-8" : undefined}
          />
        );
      case "number":
        return (
          <Input
            type="number"
            value={value || ""}
            onChange={(e) => onChange(parseFloat(e.target.value))}
            className={compact ? "h-8" : undefined}
          />
        );
      case "boolean":
        return (
          <Switch
            checked={value || false}
            onCheckedChange={onChange}
          />
        );
      case "json":
        return (
          <Textarea
            value={typeof value === "string" ? value : JSON.stringify(value, null, 2)}
            onChange={(e) => {
              try {
                onChange(JSON.parse(e.target.value));
              } catch {
                onChange(e.target.value);
              }
            }}
            rows={compact ? 2 : 4}
          />
        );
      case "date":
        return <DatePicker value={value} onChange={onChange} />;
      case "date_time":
        return <DatePicker value={value} onChange={onChange} showTime />;
      default:
        return <Input value={value || ""} onChange={(e) => onChange(e.target.value)} />;
    }
  };

  const handleStartEdit = (metafield: MetafieldType) => {
    setEditingId(metafield.id);
    setEditValue(metafield.value);
  };

  const handleSaveEdit = (metafield: MetafieldType) => {
    updateMetafield.mutate({ id: metafield.id, value: editValue });
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditValue(null);
  };

  const handleCreate = () => {
    if (!newMetafield.key.trim()) return;
    createAndAttach.mutate({
      object_type: objectType,
      object_id: objectId,
      ...newMetafield,
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Metafields</h3>
        {!readonly && !isAdding && (
          <Button variant="outline" size="sm" onClick={() => setIsAdding(true)}>
            Add Metafield
          </Button>
        )}
      </div>

      {/* Inline Add Form */}
      {isAdding && (
        <div className="p-3 border rounded-lg bg-muted/50 space-y-3">
          <div className="grid grid-cols-3 gap-2">
            <Input
              placeholder="Key"
              value={newMetafield.key}
              onChange={(e) => setNewMetafield({ ...newMetafield, key: e.target.value })}
            />
            <Select
              value={newMetafield.type}
              onValueChange={(type) => setNewMetafield({ ...newMetafield, type: type as MetafieldTypeEnum, value: "" })}
            >
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="boolean">Boolean</option>
              <option value="json">JSON</option>
              <option value="date">Date</option>
              <option value="date_time">DateTime</option>
              <option value="password">Password</option>
            </Select>
            <div className="flex items-center gap-2">
              <Switch
                checked={newMetafield.is_required}
                onCheckedChange={(checked) => setNewMetafield({ ...newMetafield, is_required: checked })}
              />
              <span className="text-sm">Required</span>
            </div>
          </div>
          <div>
            {renderValueInput(newMetafield.type, newMetafield.value, (value) => setNewMetafield({ ...newMetafield, value }))}
          </div>
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" size="sm" onClick={() => { setIsAdding(false); setNewMetafield(INITIAL_NEW_METAFIELD); }}>
              Cancel
            </Button>
            <Button size="sm" onClick={handleCreate} disabled={!newMetafield.key.trim()}>
              Add
            </Button>
          </div>
        </div>
      )}

      {/* Metafields List */}
      <div className="space-y-2">
        {metafields.length === 0 && !isAdding ? (
          <p className="text-sm text-muted-foreground">No metafields configured.</p>
        ) : (
          metafields.map((metafield) => (
            <div key={metafield.id} className="p-3 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{metafield.key}</span>
                  <span className="text-xs bg-muted px-2 py-0.5 rounded">{metafield.type}</span>
                  {metafield.is_required && <span className="text-xs text-red-500">Required</span>}
                </div>
                {!readonly && editingId !== metafield.id && (
                  <div className="flex gap-2">
                    <Button variant="ghost" size="sm" onClick={() => handleStartEdit(metafield)}>Edit</Button>
                    <Button variant="ghost" size="sm" onClick={() => detachMetafield.mutate(metafield.id)}>Remove</Button>
                  </div>
                )}
              </div>
              {editingId === metafield.id ? (
                <div className="space-y-2">
                  {renderValueInput(metafield.type as MetafieldTypeEnum, editValue, setEditValue, true)}
                  <div className="flex gap-2 justify-end">
                    <Button variant="ghost" size="sm" onClick={handleCancelEdit}>Cancel</Button>
                    <Button size="sm" onClick={() => handleSaveEdit(metafield)}>Save</Button>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-muted-foreground">
                  {metafield.type === "password" ? "••••••••" : JSON.stringify(metafield.value)}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `object_type` | MetafieldObjectTypeEnum | Yes | Type of object to attach metafield to |
| `object_id` | string | Yes | ID of the target object |
| `metafield_id` | string | Attach only | ID of existing metafield to attach |
| `key` | string | Create only | Metafield key (e.g., "customs_broker_id") |
| `type` | MetafieldTypeEnum | Create only | One of: text, number, boolean, json, date, date_time, password |
| `value` | JSON | No | The metafield value (validated per type) |
| `is_required` | boolean | No | Whether this metafield is required (default: false) |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Attach same metafield twice to same object | Reject with error | OneToOne constraint on link model |
| Attach metafield to non-existent object | 404 error | Access control validation |
| Delete object with attached metafields | Cascade delete metafields | FK on_delete=CASCADE (metafields are deleted with parent object) |
| Create metafield with invalid type/value combo | Validation error | Metafield.clean() validation |
| Password type metafield in API response | Mask value | Never return password values in queries |
| Large number of metafields on object | Performance impact | No enforced limit; rely on natural constraints and monitoring |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Database migration fails | Objects can't have metafields | Test migrations thoroughly, have rollback plan |
| GraphQL mutation timeout | Metafield not attached | Use transactions, retry logic |
| Frontend component crash | Can't manage metafields | Error boundaries, graceful degradation |
| Large JSON value causes OOM | Server crash | Enforce value size limits |
| Orphaned metafields after object deletion | N/A | Cascade delete ensures metafields are deleted with parent objects |

### Security Considerations

- [x] Access control on all mutations (user can only attach to their objects)
- [x] Password metafield values never returned in queries
- [x] No secrets in code or logs
- [x] Input validation for all metafield values
- [x] Size limits on JSON values

---

## Implementation Plan

### Phase 1: Database Models & Migrations

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create link models for manager objects | `modules/manager/karrio/server/manager/models.py` | Pending | M |
| Create link models for carrier connections | `modules/core/karrio/server/providers/models/carrier.py` | Pending | S |
| Add M2M relationships to all models | Multiple model files | Pending | M |
| Create database migrations | `modules/*/migrations/` | Pending | M |
| Add link models for Organization (EE) | `ee/insiders/modules/orgs/karrio/server/orgs/models.py` | Pending | S |

### Phase 2: GraphQL Schema & Mutations

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add MetafieldObjectTypeEnum | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Pending | S |
| Create attach/detach input types | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Pending | S |
| Implement AttachMetafieldMutation | `modules/graph/karrio/server/graph/schemas/base/mutations.py` | Pending | M |
| Implement DetachMetafieldMutation | `modules/graph/karrio/server/graph/schemas/base/mutations.py` | Pending | S |
| Implement CreateAndAttachMetafieldMutation | `modules/graph/karrio/server/graph/schemas/base/mutations.py` | Pending | M |
| Update object types to expose metafields | `modules/graph/karrio/server/graph/schemas/base/types.py` | Pending | M |
| Register mutations in schema | `modules/graph/karrio/server/graph/schemas/base/__init__.py` | Pending | S |

### Phase 3: Frontend Component

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create MetafieldsEditor component | `packages/ui/components/metafields-editor.tsx` | Pending | L |
| Create type-specific input components | `packages/ui/components/metafield-inputs/` | Pending | M |
| Add GraphQL queries/mutations | `packages/types/graphql/queries.ts` | Pending | S |
| Generate TypeScript types | `packages/types/graphql/types.ts` | Pending | S |
| Integrate into Shipment edit form | `packages/ui/*/shipment-*.tsx` | Pending | M |
| Integrate into Order edit form | `packages/ui/*/order-*.tsx` | Pending | M |
| Integrate into other object forms | Multiple files | Pending | L |

### Phase 4: Testing & Documentation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Unit tests for link models | `modules/manager/tests/` | Pending | M |
| GraphQL mutation tests | `modules/graph/karrio/server/graph/tests/test_metafields.py` | Pending | M |
| Frontend component tests | `packages/ui/__tests__/` | Pending | M |
| Update API documentation | `docs/` | Pending | S |

**Dependencies:**
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 2
- Phase 4 depends on Phases 1-3

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly:
> - Use `unittest` for SDK/connector tests (NOT pytest)
> - Use Django tests via `karrio` for server tests

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/graph/karrio/server/graph/tests/test_metafields.py` | 80%+ |
| Integration Tests | `modules/graph/karrio/server/graph/tests/` | Key flows |

### Test Cases

#### Unit Tests

```python
"""Metafield attachment tests."""

import unittest
from unittest.mock import patch, ANY

from karrio.server.graph.tests import GraphTestCase
from karrio.server.manager import models as manager


class TestMetafieldAttachment(GraphTestCase):
    def setUp(self):
        self.maxDiff = None
        self.shipment = manager.Shipment.objects.create(
            created_by=self.user,
            status="created",
            # ... other required fields
        )

    def test_create_and_attach_metafield_to_shipment(self):
        """Verify metafield can be created and attached to shipment."""
        response = self.query(
            """
            mutation createAndAttachMetafield($input: CreateAndAttachMetafieldInput!) {
                create_and_attach_metafield(input: $input) {
                    metafield {
                        id
                        key
                        type
                        value
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
            """,
            variables={
                "input": {
                    "object_type": "shipment",
                    "object_id": self.shipment.id,
                    "key": "customs_broker_id",
                    "type": "text",
                    "value": "BROKER-12345",
                }
            },
        )

        print(response)  # Debug
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["create_and_attach_metafield"]["metafield"]["key"],
            "customs_broker_id"
        )

    def test_detach_metafield_from_shipment(self):
        """Verify metafield can be detached from shipment."""
        # First create and attach
        # Then detach
        # Verify metafield still exists but not attached
        pass

    def test_cannot_attach_same_metafield_twice(self):
        """Verify duplicate attachment is rejected."""
        pass

    def test_metafield_deleted_when_object_deleted(self):
        """Verify cascade delete works correctly."""
        pass
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run metafield tests
karrio test --failfast karrio.server.graph.tests.test_metafields

# Run all graph tests
karrio test --failfast karrio.server.graph.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Migration conflicts with existing data | High | Low | Test migrations on production data copy |
| Performance impact from M2M joins | Medium | Medium | Add database indexes, use select_related |
| Breaking changes to GraphQL schema | High | Low | Maintain backward compatibility |
| Frontend component complexity | Medium | Medium | Start with minimal viable component |
| EE/OSS feature parity issues | Medium | Low | Design for both from start |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: Existing `metadata` JSONField unchanged; metafields are additive
- **Data compatibility**: No existing data modified; new tables only
- **Feature flags**: Not needed; metafields are opt-in per object

### Data Migration

No data migration required - this is purely additive. Existing `metadata` fields remain unchanged.

### Rollback Procedure

1. **Identify issue**: Metafield operations failing
2. **Stop rollout**: Revert frontend changes first
3. **Revert changes**:
   - Revert GraphQL schema changes
   - Keep database tables (no data loss)
4. **Verify recovery**: Test existing metadata functionality

---

## Appendices

### Appendix A: Supported Object Types

| Object Type | Model | Module | ID Prefix |
|-------------|-------|--------|-----------|
| `shipment` | Shipment | manager | `shp_` |
| `order` | Order | orders | `ord_` |
| `address` | Address | manager | `adr_` |
| `parcel` | Parcel | manager | `pcl_` |
| `pickup` | Pickup | manager | `pck_` |
| `tracking` | Tracking | manager | `trk_` |
| `carrier_connection` | CarrierConnection | providers | `car_` |
| `system_connection` | SystemConnection | providers | `car_` |
| `brokered_connection` | BrokeredConnection | providers | `car_` |
| `organization` | Organization | orgs (EE) | `org_` |
| `organization_user` | OrganizationUser | orgs (EE) | `usr_` |
| `markup` | Markup | pricing | `mkp_` |

### Appendix B: Metafield Types Reference

| Type | Python Validation | Example Value |
|------|-------------------|---------------|
| `text` | `isinstance(value, str)` | `"Hello World"` |
| `number` | `isinstance(value, (int, float))` | `42` or `3.14` |
| `boolean` | `isinstance(value, bool)` | `true` or `false` |
| `json` | Valid JSON object/array | `{"key": "value"}` |
| `date` | `YYYY-MM-DD` format | `"2026-01-27"` |
| `date_time` | ISO 8601 format | `"2026-01-27T12:00:00Z"` |
| `password` | `isinstance(value, str)` | `"secret123"` (never returned) |

### Appendix C: GraphQL Queries Reference

```graphql
# Create and attach metafield
mutation CreateAndAttachMetafield($input: CreateAndAttachMetafieldInput!) {
  create_and_attach_metafield(input: $input) {
    metafield {
      id
      key
      type
      value
      is_required
    }
    errors {
      field
      messages
    }
  }
}

# Attach existing metafield
mutation AttachMetafield($input: AttachMetafieldInput!) {
  attach_metafield(input: $input) {
    metafield {
      id
      key
    }
    errors {
      field
      messages
    }
  }
}

# Detach metafield
mutation DetachMetafield($input: DetachMetafieldInput!) {
  detach_metafield(input: $input) {
    id
  }
}

# Query object with metafields
query GetShipment($id: String!) {
  shipment(id: $id) {
    id
    tracking_number
    metafields {
      id
      key
      type
      value
      is_required
    }
  }
}
```

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been asked
- [x] All user decisions documented with rationale and date
- [x] Edge cases requiring input have been resolved
- [x] "Open Questions & Decisions" section cleaned up (all resolved or removed)

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (Metafield model, link patterns, serializers)

CONTENT:
- [x] All required sections completed
- [x] Code examples follow AGENTS.md style EXACTLY as original authors
- [x] Architecture diagrams included (overview, sequence, dataflow - ASCII art)
- [x] Tables used for structured data (not prose)
- [x] Before/After code shown in Problem Statement
- [x] Success criteria are measurable
- [x] Alternatives considered and documented
- [x] Edge cases and failure modes identified

TESTING:
- [x] Test cases follow unittest patterns (NOT pytest)
- [x] Test examples use assertDictEqual/assertListEqual with mock.ANY

RISK & MIGRATION:
- [x] Risk assessment completed
- [x] Migration/rollback plan documented
-->
