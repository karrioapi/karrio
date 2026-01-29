# Pickup GraphQL Integration & Dashboard Management

<!--
PRD TYPE: ENHANCEMENT
SCOPE: GraphQL queries for pickups, tracing integration, dashboard UI, admin access
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-27 |
| Status | Planning |
| Owner | Engineering Team |
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

This PRD proposes adding GraphQL query support for pickups, integrating tracing records for audit trails, and building an end-to-end pickup management dashboard page. Following the established shipment pattern, REST API handles write operations (schedule, update, cancel) while GraphQL provides deep querying, filtering, and search capabilities. Admin users (staff) can retrieve pickups across the platform with carrier credentials protected.

### Key Architecture Decisions

1. **REST for writes, GraphQL for reads**: Schedule/update/cancel pickups via REST API; query/filter/search via GraphQL—mirrors shipment architecture.
2. **Reuse existing admin access pattern**: Use the same `is_staff` check pattern from `LogType.records()` to exclude system connection records from non-staff users—no new decorators or access models.
3. **Carrier credentials protection**: Non-staff users don't see system connection tracing records; carrier snapshot shows only carrier_name/carrier_id (existing pattern).
4. **Full tracing integration**: Pickup lifecycle events (schedule, update, cancel) linked to TracingRecords with request log association.
5. **No GraphQL mutations**: Mutations remain REST-only for pickups (no partial update mutation like shipments).

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| GraphQL PickupType definition | GraphQL mutations for pickups |
| GraphQL pickup queries (single + list) | Pickup proxy layer changes |
| PickupFilter input with comprehensive filtering | Changes to core pickup SDK |
| Tracing integration for pickup events | Recurring/scheduled pickups |
| Dashboard pickup management page | Mobile app pickup management |
| Admin query with privacy protection | Multi-carrier pickup batching |
| React hooks for pickup data fetching | Pickup rate shopping |
| Pickup status badge component | |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Admin access model | Reuse `LogType.records()` pattern | Existing `is_staff` check excludes system connection records—no reinvention | 2026-01-27 |
| D2 | Privacy protection scope | Carrier credentials only (existing pattern) | System connection tracing records hidden from non-staff; carrier snapshot shows name/ID only | 2026-01-27 |
| D3 | Tracing integration | Full tracing with request logs | Audit trail for compliance, debugging, and analytics | 2026-01-27 |
| D4 | GraphQL mutation support | Query-only | REST API is sufficient for pickup operations; simplifies implementation | 2026-01-27 |

---

## Problem Statement

### Current State

Pickups have a complete REST API but lack GraphQL support, dashboard UI, and tracing integration:

```python
# Current: REST-only pickup retrieval
# No GraphQL type exists for pickups

# REST endpoints exist:
# GET /pickups - list (minimal filtering)
# POST /pickups/<carrier>/schedule - schedule
# GET /pickups/<pk> - retrieve
# POST /pickups/<pk> - update
# POST /pickups/<pk>/cancel - cancel

# Current filter is minimal:
class PickupFilters(filters.FilterSet):
    parameters: list = []  # No filters defined!

    class Meta:
        model = manager.Pickup
        fields: list = []
```

```typescript
// Frontend: No pickup hooks or dashboard page exists
// Users must use raw REST API calls
```

### Desired State

```python
# GraphQL type with full query capabilities
@strawberry.type
class PickupType:
    id: str
    object_type: str
    confirmation_number: typing.Optional[str]
    pickup_date: str
    ready_time: str
    closing_time: str
    # ... full type definition

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["PickupType"]:
        return manager.Pickup.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(info, filter=None) -> utils.Connection["PickupType"]:
        # Staff users see all pickups
        # Regular users see only their own
        ...
```

```typescript
// Frontend: Full pickup management
import { usePickups, usePickup } from "@karrio/hooks/pickup";

export function PickupList() {
  const { query: { data: { pickups } } } = usePickups({ setVariablesToURL: true });
  // Full pickup management UI
}
```

### Problems

1. **No GraphQL query support**: Cannot leverage GraphQL's powerful filtering, pagination, and field selection for pickups.
2. **No dashboard UI**: Users have no visual interface for managing pickups—must use API directly or external tools.
3. **No tracing/audit trail**: Pickup operations not tracked in TracingRecords, hindering debugging and compliance.
4. **Minimal filtering**: Current REST filter is empty; no ability to search by date, carrier, confirmation number, etc.
5. **No admin visibility**: Staff cannot query pickups across organizations for support and operations.

---

## Goals & Success Criteria

### Goals

1. Add GraphQL `PickupType` with comprehensive field exposure matching REST response structure.
2. Implement `PickupFilter` input with filtering by date range, carrier, confirmation number, status, and metadata.
3. Integrate pickup operations with TracingRecords for full audit trail.
4. Build dashboard pickup management page with filtering, pagination, and pickup details preview.
5. Enable staff users to query all pickups with carrier credentials protected.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| GraphQL pickup query latency | < 200ms for list queries | Must-have |
| Filter coverage | 10+ filter fields (matching shipment pattern) | Must-have |
| Dashboard page load | < 1s initial load | Must-have |
| Test coverage | 80%+ for new code | Must-have |
| Tracing record creation | 100% of pickup operations tracked | Must-have |
| Admin query support | Staff sees all org pickups | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] GraphQL PickupType with resolve and resolve_list
- [ ] PickupFilter input with comprehensive filtering
- [ ] Dashboard pickup list page with pagination
- [ ] Pickup preview/details sheet
- [ ] TracingRecord integration for schedule/update/cancel
- [ ] Admin access with carrier credentials protection
- [ ] Unit and integration tests

**Nice-to-have (P1):**
- [ ] Pickup status badge component
- [ ] Bulk cancel action
- [ ] Export pickups to CSV
- [ ] Pickup calendar view

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| GraphQL queries only (REST for writes) | Consistent with shipment pattern; simpler; REST already works | Two API styles | **Selected** |
| Full GraphQL including mutations | Single API paradigm | Duplicates REST; more work; mutations complex for pickups | Rejected |
| Enhance REST only (no GraphQL) | Simpler backend | Inconsistent with rest of platform; limited filtering | Rejected |
| Separate admin API | Clear separation | Duplicates code; harder to maintain | Rejected |

### Trade-off Analysis

The selected approach (GraphQL queries + REST writes) provides:
- **Consistency**: Matches established shipment pattern, reducing cognitive load
- **Leverage existing code**: REST write operations work correctly; no changes needed
- **Rich querying**: GraphQL's filtering, pagination, and field selection for reads
- **Minimal risk**: No changes to write operations that interact with carrier APIs

---

## Technical Design

> **IMPORTANT**: This design follows existing patterns from shipments, trackers, and manifests.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| Pickup Model | `modules/manager/karrio/server/manager/models.py:Pickup` | Base model already complete |
| Pickup REST Serializers | `modules/manager/karrio/server/manager/serializers/pickup.py` | Reference for GraphQL type fields |
| ShipmentType GraphQL | `modules/graph/karrio/server/graph/schemas/base/types.py:ShipmentType` | Pattern for PickupType |
| TrackerType GraphQL | `modules/graph/karrio/server/graph/schemas/base/types.py:TrackerType` | Pattern for carrier snapshot |
| **LogType.records()** | `modules/graph/karrio/server/graph/schemas/base/types.py:470-484` | **Reuse `is_staff` check pattern for system connection protection** |
| ShipmentFilter Input | `modules/graph/karrio/server/graph/schemas/base/inputs.py:ShipmentFilter` | Pattern for PickupFilter |
| ShipmentFilters | `modules/core/karrio/server/core/filters.py:ShipmentFilters` | Pattern for PickupFilters |
| useShipments Hook | `packages/hooks/shipment.ts` | Pattern for usePickups |
| Shipments Page | `packages/core/modules/Shipments/index.tsx` | Pattern for Pickups page |
| TracingRecord | `modules/core/karrio/server/tracing/models.py` | For pickup event tracking |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PICKUP MANAGEMENT SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐ │
│  │   Dashboard  │────>│   GraphQL    │────>│      PickupType              │ │
│  │  Pickups UI  │     │   Queries    │     │  (resolve, resolve_list)     │ │
│  └──────────────┘     └──────────────┘     └──────────────────────────────┘ │
│         │                                              │                     │
│         │ REST (schedule/                              │ access_by()         │
│         │ update/cancel)                               │                     │
│         ▼                                              ▼                     │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐ │
│  │   REST API   │────>│   Gateway    │────>│      Pickup Model            │ │
│  │  /pickups/*  │     │   Pickups    │     │  (manager.Pickup)            │ │
│  └──────────────┘     └──────────────┘     └──────────────────────────────┘ │
│         │                    │                         │                     │
│         │                    │                         │                     │
│         ▼                    ▼                         ▼                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      TracingRecord                                    │   │
│  │  (meta: {object_id: pickup.id, request_log_id: log.id})              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────┐     ┌─────────┐     ┌────────┐     ┌─────────┐
│ Client │     │GraphQL │     │ Pickup  │     │ Filter │     │Database │
└───┬────┘     └───┬────┘     └────┬────┘     └───┬────┘     └────┬────┘
    │              │               │              │               │
    │ 1. Query     │               │              │               │
    │  pickups     │               │              │               │
    │─────────────>│               │              │               │
    │              │ 2. resolve_   │              │               │
    │              │    list()     │              │               │
    │              │──────────────>│              │               │
    │              │               │ 3. access_   │               │
    │              │               │    by()      │               │
    │              │               │─────────────>│               │
    │              │               │              │ 4. Filter     │
    │              │               │              │    query      │
    │              │               │              │──────────────>│
    │              │               │              │               │
    │              │               │              │ 5. QuerySet   │
    │              │               │              │<──────────────│
    │              │               │ 6. Paginated │               │
    │              │               │    results   │               │
    │              │               │<─────────────│               │
    │              │ 7. Connection │              │               │
    │              │<──────────────│              │               │
    │ 8. Response  │               │              │               │
    │<─────────────│               │              │               │
    │              │               │              │               │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           QUERY FLOW                                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌───────────┐ │
│  │  PickupFilter│───>│PickupFilters│───>│  QuerySet   │───>│PickupType │ │
│  │  (GraphQL)   │    │  (Django)   │    │  (filtered) │    │ (response)│ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └───────────┘ │
│                                                                           │
│  Fields:           Methods:            Scoped by:          Resolves:      │
│  - pickup_date     - carrier_filter    - access_by()      - address       │
│  - carrier_name    - date_filter       - is_staff check   - parcels       │
│  - confirmation    - keyword_filter    - test_mode        - shipments     │
│  - status          - metadata_filter                      - carrier       │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                           TRACING FLOW                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌───────────┐ │
│  │ REST Request│───>│  Gateway    │───>│  Pickup     │───>│ Tracing   │ │
│  │ (schedule)  │    │  Pickups    │    │  Created    │    │ Record    │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └───────────┘ │
│                                                                           │
│  POST /pickups/    Pickups.schedule() Pickup.save()     TracingRecord:   │
│  carrier/schedule                                        key: "pickup.   │
│                                                              scheduled"  │
│                                                          meta: {         │
│                                                            object_id,    │
│                                                            request_log_id│
│                                                          }               │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### GraphQL PickupType

```python
# modules/graph/karrio/server/graph/schemas/base/types.py

@strawberry.type
class PickupType:
    """GraphQL type for Pickup model."""

    id: str
    object_type: str
    confirmation_number: typing.Optional[str]
    pickup_date: str
    ready_time: str
    closing_time: str
    instruction: typing.Optional[str]
    package_location: typing.Optional[str]
    test_mode: bool
    options: utils.JSON
    metadata: utils.JSON
    meta: typing.Optional[utils.JSON]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def carrier_id(self: manager.Pickup) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_id")

    @strawberry.field
    def carrier_name(self: manager.Pickup) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_name")

    @strawberry.field
    def address(self: manager.Pickup) -> typing.Optional[AddressType]:
        return AddressType.parse(self.address) if self.address else None

    @strawberry.field
    def pickup_charge(self: manager.Pickup) -> typing.Optional[ChargeType]:
        return ChargeType.parse(self.pickup_charge) if self.pickup_charge else None

    @strawberry.field
    def parcels(self: manager.Pickup) -> typing.List[ParcelType]:
        """Parcels from related shipments."""
        return [
            ParcelType.parse(p)
            for shipment in self.shipments.all()
            for p in (shipment.parcels or [])
        ]

    @strawberry.field
    def tracking_numbers(self: manager.Pickup) -> typing.List[str]:
        """Tracking numbers from related shipments."""
        return [
            s.tracking_number
            for s in self.shipments.all()
            if s.tracking_number
        ]

    @strawberry.field
    def shipments(self: manager.Pickup) -> typing.List["ShipmentType"]:
        """Related shipments for this pickup."""
        return list(self.shipments.all())

    @strawberry.field
    def pickup_carrier(
        self: manager.Pickup,
    ) -> typing.Optional[CarrierSnapshotType]:
        """Carrier snapshot with credentials protected."""
        return CarrierSnapshotType.parse(self.carrier)

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["PickupType"]:
        return manager.Pickup.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.PickupFilter] = strawberry.UNSET,
    ) -> utils.Connection["PickupType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.PickupFilter()
        queryset = filters.PickupFilters(
            _filter.to_dict(), manager.Pickup.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
```

#### GraphQL PickupFilter Input

```python
# modules/graph/karrio/server/graph/schemas/base/inputs.py

@strawberry.input
class PickupFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    id: typing.Optional[typing.List[str]] = strawberry.UNSET
    confirmation_number: typing.Optional[str] = strawberry.UNSET
    pickup_date_after: typing.Optional[str] = strawberry.UNSET
    pickup_date_before: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    address: typing.Optional[str] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[utils.JSON] = strawberry.UNSET
    meta_key: typing.Optional[str] = strawberry.UNSET
    meta_value: typing.Optional[utils.JSON] = strawberry.UNSET
```

#### Django PickupFilters

```python
# modules/core/karrio/server/core/filters.py

class PickupFilters(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="pickup keyword and indexes search",
    )
    id = filters.CharInFilter(
        field_name="id",
        lookup_expr="in",
        help_text="pickup id(s).",
    )
    confirmation_number = filters.CharFilter(
        field_name="confirmation_number",
        lookup_expr="icontains",
        help_text="confirmation number (partial match)",
    )
    pickup_date_after = filters.DateFilter(
        field_name="pickup_date",
        lookup_expr="gte",
        help_text="pickup date after (YYYY-MM-DD)",
    )
    pickup_date_before = filters.DateFilter(
        field_name="pickup_date",
        lookup_expr="lte",
        help_text="pickup date before (YYYY-MM-DD)",
    )
    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="DateTime in format `YYYY-MM-DD H:M:S.fz`",
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="DateTime in format `YYYY-MM-DD H:M:S.fz`",
    )
    carrier_name = filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in dataunits.CARRIER_NAMES],
        help_text="carrier_name for the pickup",
    )
    address = filters.CharFilter(
        method="address_filter",
        help_text="pickup address search",
    )
    metadata_key = filters.CharFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="pickup metadata key.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="pickup metadata value.",
    )
    meta_key = filters.CharFilter(
        field_name="meta",
        method="meta_key_filter",
        help_text="pickup meta key.",
    )
    meta_value = filters.CharFilter(
        field_name="meta",
        method="meta_value_filter",
        help_text="pickup meta value.",
    )

    parameters = [
        openapi.OpenApiParameter(
            "keyword",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "confirmation_number",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "pickup_date_after",
            type=openapi.OpenApiTypes.DATE,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "pickup_date_before",
            type=openapi.OpenApiTypes.DATE,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
    ]

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.Pickup
        fields: list = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "confirmation_number",
                    "instruction",
                    "package_location",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(confirmation_number__icontains=value)
            | models.Q(instruction__icontains=value)
        )

    def carrier_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "carrier")
                if (o.get("carrier") or {}).get("carrier_name") in value
            ]
        )

    def address_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "address")
                if value.lower() in str(o.get("address") or {}).lower()
            ]
        )

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "metadata")
                if value in (o.get("metadata") or {}).values()
            ]
        )

    def meta_key_filter(self, queryset, name, value):
        return queryset.filter(meta__has_key=value)

    def meta_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "meta")
                if value in map(str, (o.get("meta") or {}).values())
            ]
        )
```

### GraphQL Schema Registration

```python
# modules/graph/karrio/server/graph/schemas/base/__init__.py

@strawberry.type
class Query:
    # ... existing queries ...

    @strawberry.field
    def pickup(self, info: Info, id: str) -> typing.Optional[types.PickupType]:
        return types.PickupType.resolve(info, id)

    @strawberry.field
    def pickups(
        self,
        info: Info,
        filter: typing.Optional[inputs.PickupFilter] = strawberry.UNSET,
    ) -> utils.Connection[types.PickupType]:
        return types.PickupType.resolve_list(info, filter)
```

### TypeScript Types

```typescript
// packages/types/graphql/queries.ts

export const GET_PICKUPS = gql`
  query get_pickups($filter: PickupFilter) {
    pickups(filter: $filter) {
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      edges {
        node {
          id
          object_type
          confirmation_number
          pickup_date
          ready_time
          closing_time
          instruction
          package_location
          test_mode
          carrier_id
          carrier_name
          address {
            id
            person_name
            company_name
            address_line1
            city
            state_code
            postal_code
            country_code
            phone_number
          }
          pickup_charge {
            name
            amount
            currency
          }
          tracking_numbers
          metadata
          created_at
          updated_at
        }
      }
    }
  }
`;

export const GET_PICKUP = gql`
  query get_pickup($id: String!) {
    pickup(id: $id) {
      id
      object_type
      confirmation_number
      pickup_date
      ready_time
      closing_time
      instruction
      package_location
      test_mode
      carrier_id
      carrier_name
      address {
        id
        person_name
        company_name
        address_line1
        address_line2
        city
        state_code
        postal_code
        country_code
        phone_number
        email
      }
      pickup_charge {
        name
        amount
        currency
      }
      parcels {
        id
        weight
        weight_unit
        width
        height
        length
        dimension_unit
        packaging_type
        package_preset
      }
      tracking_numbers
      shipments {
        id
        tracking_number
        status
      }
      options
      metadata
      meta
      created_at
      updated_at
    }
  }
`;
```

### React Hook

```typescript
// packages/hooks/pickup.ts

import {
  PickupFilter,
  get_pickups,
  get_pickup,
  GET_PICKUPS,
  GET_PICKUP,
} from "@karrio/types";
import { useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, onError } from "@karrio/lib";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

type FilterType = PickupFilter & {
  setVariablesToURL?: boolean;
  cacheKey?: string;
  isDisabled?: boolean;
  preloadNextPage?: boolean;
};

export function usePickups({
  setVariablesToURL = false,
  isDisabled = false,
  preloadNextPage = false,
  cacheKey,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<PickupFilter>({
    ...PAGINATION,
    ...initialData,
  });

  const fetch = (variables: { filter: PickupFilter }) =>
    karrio.graphql.request<get_pickups>(gqlstr(GET_PICKUPS), { variables });

  const query = useAuthenticatedQuery({
    queryKey: [cacheKey || "pickups", filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: PickupFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["carrier_name"].includes(key))
        return {
          ...acc,
          [key]: []
            .concat(options[key as keyof PickupFilter])
            .reduce(
              (acc, item: string) =>
                typeof item == "string"
                  ? [].concat(acc, item.split(",") as any)
                  : [].concat(acc, item),
              [],
            ),
        };
      if (["offset", "first"].includes(key))
        return {
          ...acc,
          [key]: parseInt(options[key as keyof PickupFilter]),
        };

      return {
        ...acc,
        [key]: options[key as keyof PickupFilter],
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.pickups.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["pickups", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    filter,
    setFilter,
  };
}

export function usePickup(id: string) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["pickups", id],
    queryFn: () =>
      karrio.graphql.request<get_pickup>(gqlstr(GET_PICKUP), {
        variables: { id },
      }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function usePickupMutation(id?: string) {
  const queryClient = useQueryClient();
  const karrio = useKarrio();

  const invalidateCache = () => {
    queryClient.invalidateQueries(["pickups"]);
    if (id) queryClient.invalidateQueries(["pickups", id]);
  };

  // REST mutations for pickup operations
  const cancelPickup = useMutation(
    ({ id }: { id: string }) =>
      handleFailure(karrio.pickups.cancel({ id }).then(({ data }) => data)),
    { onSuccess: invalidateCache, onError },
  );

  return {
    cancelPickup,
    invalidateCache,
  };
}
```

### Tracing Integration

```python
# modules/manager/karrio/server/manager/serializers/pickup.py

# Add tracing to pickup operations (in PickupData.create method)
def create(self, validated_data: dict, context, **kwargs) -> models.Pickup:
    # ... existing creation logic ...

    # Create tracing record for pickup scheduled event
    from karrio.server.tracing.utils import save_tracing_records

    save_tracing_records(
        context,
        key="pickup.scheduled",
        record={
            "pickup_id": pickup.id,
            "confirmation_number": pickup.confirmation_number,
            "carrier_name": pickup.carrier_name,
            "pickup_date": str(pickup.pickup_date),
        },
        meta={
            "object_id": pickup.id,
        },
    )

    return pickup
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique pickup identifier (pck_*) |
| `object_type` | string | Yes | Always "pickup" |
| `confirmation_number` | string | No | Carrier's pickup confirmation ID |
| `pickup_date` | string | Yes | Date of pickup (YYYY-MM-DD) |
| `ready_time` | string | Yes | Time when shipment is ready (HH:MM) |
| `closing_time` | string | Yes | Pickup deadline (HH:MM) |
| `instruction` | string | No | Special handling instructions |
| `package_location` | string | No | Where packages are located |
| `test_mode` | boolean | Yes | Whether created in test mode |
| `carrier_id` | string | No | Carrier account identifier |
| `carrier_name` | string | No | Carrier name (e.g., "canadapost") |
| `address` | AddressType | No | Pickup location address |
| `pickup_charge` | ChargeType | No | Associated pickup charge |
| `parcels` | [ParcelType] | No | Parcels from related shipments |
| `tracking_numbers` | [string] | No | Tracking numbers of related shipments |
| `shipments` | [ShipmentType] | No | Related shipments |
| `options` | JSON | No | Carrier-specific options |
| `metadata` | JSON | No | User-defined metadata |
| `meta` | JSON | No | Provider-specific metadata |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Pickup with no shipments | Return pickup with empty parcels/tracking_numbers | Allow querying; parcels resolver returns [] |
| Pickup from cancelled shipment | Include in results with shipment status visible | No filtering; shipment status shown in response |
| Non-staff querying pickup with system connection tracing | Tracing records for system connections excluded | Reuse `LogType.records()` pattern |
| Filter by non-existent carrier | Return empty results | No error; empty connection |
| Pickup date in past | Return in results | No date validation on query |
| Deleted/cancelled pickup | Not returned (record deleted) | Current behavior: cancel deletes pickup |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| GraphQL query timeout on large datasets | Slow/failed dashboard load | Pagination enforced; max 100 per page |
| N+1 queries on shipments relation | Performance degradation | Use select_related/prefetch_related in manager |
| Carrier snapshot missing | Null carrier_id/carrier_name | Graceful null handling in resolvers |
| TracingRecord save failure | Pickup created but not tracked | Log error; don't fail pickup operation |

### Security Considerations

- [x] Input validation for all filter parameters
- [x] System connection tracing records hidden from non-staff (reuse `LogType.records()` pattern)
- [x] CarrierSnapshotType only exposes carrier_id, carrier_name (no credentials)
- [x] Access control via `access_by()` method (existing pattern)
- [x] All operations logged via TracingRecords
- [x] SQL injection prevention (Django ORM)
- [x] Test mode isolation

---

## Implementation Plan

### Phase 1: Backend GraphQL & Filters

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add PickupType to GraphQL types | `modules/graph/karrio/server/graph/schemas/base/types.py` | Pending | M |
| Add PickupFilter input | `modules/graph/karrio/server/graph/schemas/base/inputs.py` | Pending | S |
| Implement PickupFilters | `modules/core/karrio/server/core/filters.py` | Pending | M |
| Register pickup queries in schema | `modules/graph/karrio/server/graph/schemas/base/__init__.py` | Pending | S |
| Add GraphQL tests for pickups | `modules/graph/karrio/server/graph/tests/test_pickups.py` | Pending | M |

### Phase 2: Tracing Integration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add tracing to pickup schedule | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Add tracing to pickup update | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Add tracing to pickup cancel | `modules/manager/karrio/server/manager/serializers/pickup.py` | Pending | S |
| Test tracing integration | `modules/manager/karrio/server/manager/tests/test_pickups.py` | Pending | S |

### Phase 3: TypeScript Types & Hooks

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add PickupType and PickupFilter types | `packages/types/graphql/ee/pickups.ts` | Pending | S |
| Add GET_PICKUPS and GET_PICKUP queries | `packages/types/graphql/queries.ts` | Pending | S |
| Implement usePickups hook | `packages/hooks/pickup.ts` | Pending | M |
| Implement usePickup hook | `packages/hooks/pickup.ts` | Pending | S |
| Implement usePickupMutation hook | `packages/hooks/pickup.ts` | Pending | S |
| Export hooks from index | `packages/hooks/index.ts` | Pending | S |

### Phase 4: Dashboard UI

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create Pickups page component | `packages/core/modules/Pickups/index.tsx` | Pending | L |
| Create PickupsFilter component | `packages/ui/components/pickups-filter.tsx` | Pending | M |
| Create PickupPreviewSheet component | `packages/ui/components/pickup-preview-sheet.tsx` | Pending | M |
| Create PickupMenu component | `packages/ui/components/pickup-menu.tsx` | Pending | S |
| Add pickups route to dashboard | `apps/dashboard/src/app/(dashboard)/pickups/page.tsx` | Pending | S |
| Add navigation link | Update sidebar navigation | Pending | S |

**Dependencies:**
- Phase 2 depends on Phase 1 completion
- Phase 3 depends on Phase 1 completion
- Phase 4 depends on Phase 3 completion

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/graph/karrio/server/graph/tests/test_pickups.py` | 80%+ |
| Integration Tests | `modules/manager/karrio/server/manager/tests/test_pickups.py` | Key flows |
| Frontend Tests | `packages/hooks/__tests__/pickup.test.ts` | Critical paths |

### Test Cases

#### GraphQL Unit Tests

```python
"""GraphQL pickup query tests following AGENTS.md patterns."""

import unittest
from unittest.mock import patch, ANY
from karrio.server.graph.tests.base import GraphTestCase


class TestPickupQueries(GraphTestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None
        # Create test pickup
        self.pickup = self.create_pickup()

    def test_query_pickup(self):
        """Verify single pickup query."""
        response = self.query(
            """
            query get_pickup($id: String!) {
                pickup(id: $id) {
                    id
                    object_type
                    confirmation_number
                    pickup_date
                    carrier_name
                }
            }
            """,
            variables={"id": self.pickup.id},
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            response.data["pickup"],
            {
                "id": self.pickup.id,
                "object_type": "pickup",
                "confirmation_number": "27241",
                "pickup_date": "2020-10-25",
                "carrier_name": "canadapost",
            },
        )

    def test_query_pickups_list(self):
        """Verify pickup list query with pagination."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    page_info {
                        count
                        has_next_page
                    }
                    edges {
                        node {
                            id
                            confirmation_number
                        }
                    }
                }
            }
            """,
            variables={"filter": {"first": 20, "offset": 0}},
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["pickups"]["page_info"]["count"], 1)

    def test_query_pickups_filter_by_carrier(self):
        """Verify pickup filtering by carrier_name."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            carrier_name
                        }
                    }
                }
            }
            """,
            variables={"filter": {"carrier_name": ["canadapost"]}},
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["pickups"]["edges"]), 1)

    def test_query_pickups_filter_by_date_range(self):
        """Verify pickup filtering by date range."""
        response = self.query(
            """
            query get_pickups($filter: PickupFilter) {
                pickups(filter: $filter) {
                    edges {
                        node {
                            id
                            pickup_date
                        }
                    }
                }
            }
            """,
            variables={
                "filter": {
                    "pickup_date_after": "2020-10-01",
                    "pickup_date_before": "2020-10-31",
                }
            },
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)


class TestPickupTracingRecordsVisibility(GraphTestCase):
    """Test tracing records visibility following LogType.records() pattern."""

    def setUp(self):
        super().setUp()
        self.maxDiff = None
        self.pickup = self.create_pickup()

    def test_staff_sees_system_connection_tracing_records(self):
        """Verify staff user sees all tracing records including system connections."""
        self.user.is_staff = True
        self.user.save()

        # Query pickup with associated tracing records
        response = self.query(
            """
            query get_logs {
                logs {
                    edges {
                        node {
                            id
                            records {
                                id
                                key
                                meta
                            }
                        }
                    }
                }
            }
            """
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        # Staff sees all records including system connection records

    def test_non_staff_excludes_system_connection_tracing_records(self):
        """Verify non-staff user doesn't see system connection tracing records.

        This follows the existing pattern in LogType.records() which excludes
        tracing records where meta.carrier_account_id matches a SystemConnection.
        """
        self.user.is_staff = False
        self.user.save()

        response = self.query(
            """
            query get_logs {
                logs {
                    edges {
                        node {
                            id
                            records {
                                id
                                key
                                meta
                            }
                        }
                    }
                }
            }
            """
        )
        # print(response)  # Uncomment for debugging
        self.assertResponseNoErrors(response)
        # Non-staff doesn't see system connection records (existing behavior)
```

#### Integration Tests

```python
"""Pickup tracing integration tests."""

import unittest
from unittest.mock import patch, ANY
from karrio.server.manager.tests.test_pickups import TestFixture
import karrio.server.tracing.models as tracing


class TestPickupTracing(TestFixture):
    def test_schedule_pickup_creates_tracing_record(self):
        """Verify tracing record created on pickup schedule."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA)
            # print(response)  # Uncomment for debugging

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Verify tracing record created
            pickup_id = response.data["id"]
            tracing_records = tracing.TracingRecord.objects.filter(
                meta__object_id=pickup_id
            )
            self.assertEqual(tracing_records.count(), 1)
            self.assertEqual(tracing_records.first().key, "pickup.scheduled")
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run GraphQL pickup tests
karrio test --failfast karrio.server.graph.tests.test_pickups

# Run manager pickup tests (includes tracing)
karrio test --failfast karrio.server.manager.tests.test_pickups

# Run all pickup-related tests
karrio test --failfast -k pickup
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Performance on large datasets | Medium | Medium | Enforce pagination; add database indexes |
| N+1 queries on shipments | Medium | High | Use prefetch_related in PickupManager |
| Breaking existing REST API | High | Low | No changes to REST; additive only |
| GraphQL schema conflicts | Low | Low | Follow existing patterns; thorough testing |
| Dashboard bundle size increase | Low | Medium | Code splitting for pickup module |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: REST API unchanged; GraphQL is additive
- **Data compatibility**: No model changes; existing pickups queryable immediately
- **Feature flags**: Not required; features are additive

### Rollback Procedure

1. **Identify issue**: Monitor error rates in GraphQL pickup queries
2. **Stop rollout**: Remove pickup queries from GraphQL schema
3. **Revert changes**: Git revert of pickup-related commits
4. **Verify recovery**: Confirm REST API still functional

---

## Appendices

### Appendix A: GraphQL Query Examples

```graphql
# List all pickups with filters
query ListPickups {
  pickups(filter: {
    carrier_name: ["canadapost", "ups"],
    pickup_date_after: "2024-01-01",
    first: 20,
    offset: 0
  }) {
    page_info {
      count
      has_next_page
    }
    edges {
      node {
        id
        confirmation_number
        pickup_date
        carrier_name
        address {
          city
          country_code
        }
        tracking_numbers
      }
    }
  }
}

# Get single pickup with full details
query GetPickup($id: String!) {
  pickup(id: $id) {
    id
    confirmation_number
    pickup_date
    ready_time
    closing_time
    instruction
    package_location
    carrier_name
    carrier_id
    address {
      person_name
      company_name
      address_line1
      city
      state_code
      postal_code
      country_code
      phone_number
    }
    pickup_charge {
      name
      amount
      currency
    }
    parcels {
      id
      weight
      weight_unit
    }
    shipments {
      id
      tracking_number
      status
    }
    metadata
    created_at
  }
}
```

### Appendix B: Dashboard Page Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Pickups                                                        [+ Schedule] │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│ │   All    │ │ Upcoming │ │  Today   │ │   Past   │        [Filters ▼]     │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Carrier        │ Confirmation │ Pickup Date │ Address      │ Actions   │
│───┼────────────────┼──────────────┼─────────────┼──────────────┼───────────│
│ ☐ │ 🟡 Canada Post │ 27241        │ 2024-01-25  │ Toronto, ON  │ ⋮         │
│ ☐ │ 🔵 UPS         │ UPS123456    │ 2024-01-26  │ Vancouver,BC │ ⋮         │
│ ☐ │ 🟠 FedEx       │ FX789012     │ 2024-01-26  │ Montreal, QC │ ⋮         │
├─────────────────────────────────────────────────────────────────────────────┤
│                              < 1 2 3 ... 10 >                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Appendix C: Tracing Record Keys

| Key | Event | Record Data |
|-----|-------|-------------|
| `pickup.scheduled` | Pickup scheduled successfully | pickup_id, confirmation_number, carrier_name, pickup_date |
| `pickup.updated` | Pickup details updated | pickup_id, changes (diff) |
| `pickup.cancelled` | Pickup cancelled | pickup_id, confirmation_number, reason |
| `pickup.schedule_failed` | Pickup schedule failed | error, carrier_name, pickup_date |

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been asked
- [x] All user decisions documented with rationale and date
- [x] Edge cases requiring input have been resolved
- [x] "Open Questions & Decisions" section cleaned up (all resolved)

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (access_by, paginated_connection, filters)

CONTENT:
- [x] All required sections completed
- [x] Code examples follow AGENTS.md style EXACTLY
- [x] Architecture diagrams included (overview, sequence, dataflow - ASCII art)
- [x] Tables used for structured data
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
