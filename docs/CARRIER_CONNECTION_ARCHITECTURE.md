# Carrier Connection Architecture

> **Technical Reference Document**
>
> Last Updated: January 2026
> Status: Production

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Models](#2-data-models)
3. [API Specifications](#3-api-specifications)
4. [SDK Integration](#4-sdk-integration)
5. [Frontend Integration](#5-frontend-integration)
6. [Data Flow Diagrams](#6-data-flow-diagrams)
7. [Access Control](#7-access-control)
8. [Implementation Notes](#8-implementation-notes)
9. [Migration Notes](#9-migration-notes)

---

## 1. Overview

Karrio uses a **three-tier connection architecture** for carrier integrations:

| Model | Purpose | Credentials | Visibility |
|-------|---------|-------------|------------|
| **CarrierConnection** | User/org-owned connections | Full access | Owner only |
| **SystemConnection** | Admin-managed platform connections | Admin only | Via BrokeredConnection |
| **BrokeredConnection** | User enablement of SystemConnection | Inherited (hidden) | Enabled users |

### Key Design Principles

1. **Unified ID Prefix**: All connection types use `car_xxx` prefix
2. **Write-Only REST Credentials**: REST API never returns credentials in GET responses
3. **GraphQL Full Access**: GraphQL returns credentials for user connections
4. **Implicit Visibility**: BrokeredConnection existence grants access to SystemConnection

---

## 2. Data Models

### 2.1 CarrierConnection (User/Org Owned)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CarrierConnection                            │
│                    db_table: "CarrierConnection"                │
├─────────────────────────────────────────────────────────────────┤
│ id              : CharField (car_xxx, PK)                       │
│ carrier_code    : CharField (e.g., "fedex", "ups")              │
│ carrier_id      : CharField (user-defined identifier)          │
│ credentials     : JSONField (API keys, account numbers)        │
│ config          : JSONField (operational settings)             │
│ capabilities    : MultiChoiceField (rating, shipping, etc.)    │
│ metadata        : JSONField                                    │
│ active          : BooleanField                                 │
│ test_mode       : BooleanField                                 │
│ rate_sheet      : FK(RateSheet, nullable)                      │
│ created_by      : FK(User)                                     │
│ created_at      : DateTimeField                                │
├─────────────────────────────────────────────────────────────────┤
│ Insiders Only:                                                 │
│ org             : M2M via CarrierLink                          │
└─────────────────────────────────────────────────────────────────┘

Location: modules/core/karrio/server/providers/models/carrier.py
```

### 2.2 SystemConnection (Admin Managed)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SystemConnection                             │
│                    db_table: "SystemConnection"                 │
├─────────────────────────────────────────────────────────────────┤
│ id              : CharField (car_xxx, PK)                       │
│ carrier_code    : CharField                                    │
│ carrier_id      : CharField (platform identifier)              │
│ credentials     : JSONField (admin-only, never exposed)        │
│ config          : JSONField (base config)                      │
│ capabilities    : MultiChoiceField                             │
│ metadata        : JSONField                                    │
│ is_active       : BooleanField                                 │
│ test_mode       : BooleanField                                 │
│ rate_sheet      : FK(RateSheet, nullable)                      │
│ created_by      : FK(User, nullable) - admin creator           │
│ created_at      : DateTimeField                                │
└─────────────────────────────────────────────────────────────────┘

Location: modules/core/karrio/server/providers/models/connection.py
```

### 2.3 BrokeredConnection (User Enablement)

```
┌─────────────────────────────────────────────────────────────────┐
│                    BrokeredConnection                           │
│                    db_table: "BrokeredConnection"               │
├─────────────────────────────────────────────────────────────────┤
│ id                    : CharField (car_xxx, PK)                 │
│ system_connection     : FK(SystemConnection)                    │
│ carrier_id            : CharField (nullable, override)          │
│ config_overrides      : JSONField (merged with system)          │
│ capabilities_overrides: MultiChoiceField (optional)             │
│ is_enabled            : BooleanField                           │
│ metadata              : JSONField                               │
│ created_by            : FK(User, nullable) - OSS mode           │
│ created_at            : DateTimeField                           │
├─────────────────────────────────────────────────────────────────┤
│ Computed Properties:                                            │
│ - credentials → None (always, security)                         │
│ - config → system.config + config_overrides (merged)            │
│ - capabilities → overrides or system.capabilities               │
│ - active → is_enabled AND system_connection.is_active           │
├─────────────────────────────────────────────────────────────────┤
│ Insiders Only:                                                  │
│ link: OneToOne(BrokeredConnectionLink) - org association        │
└─────────────────────────────────────────────────────────────────┘

Location: modules/core/karrio/server/providers/models/connection.py
```

### 2.4 Carrier Snapshot (JSON in Shipment/Tracking/Pickup)

```json
{
  "connection_id": "car_abc123",
  "connection_type": "account|system|brokered",
  "carrier_code": "fedex",
  "carrier_id": "my_fedex_account",
  "carrier_name": "FedEx",
  "test_mode": false
}
```

Used in: `Shipment.selected_rate.meta`, `Tracking.carrier`, `Pickup.carrier`, `Manifest.carrier`

---

## 3. API Specifications

### 3.1 REST API

**Base URL:** `/v1/connections`

#### List Connections
```http
GET /v1/connections
Authorization: Token {api_key}

Response 200:
{
  "count": 2,
  "results": [
    {
      "id": "car_abc123",
      "object_type": "carrier-connection",
      "carrier_name": "fedex",
      "display_name": "FedEx",
      "carrier_id": "my_fedex",
      "capabilities": ["rating", "shipping", "tracking"],
      "config": {},
      "metadata": {},
      "is_system": false,
      "active": true,
      "test_mode": false
      // NOTE: credentials NOT returned (write-only)
    },
    {
      "id": "car_xyz789",
      "object_type": "brokered-connection",
      "carrier_name": "ups",
      "carrier_id": "platform_ups",
      "is_system": true,
      // ...
    }
  ]
}
```

#### Create Connection
```http
POST /v1/connections
Content-Type: application/json

{
  "carrier_name": "fedex",
  "carrier_id": "my_fedex_account",
  "credentials": {
    "api_key": "xxx",
    "secret_key": "xxx",
    "account_number": "123456"
  },
  "config": {
    "label_format": "PDF"
  },
  "active": true,
  "test_mode": false
}

Response 201:
{
  "id": "car_new123",
  "carrier_name": "fedex",
  "carrier_id": "my_fedex_account",
  // ... (no credentials in response)
}
```

#### Update Connection
```http
PATCH /v1/connections/{id}
Content-Type: application/json

{
  "credentials": {
    "api_key": "new_key"
  },
  "config": {
    "label_format": "ZPL"
  }
}

Response 200:
{
  "id": "car_abc123",
  // ... (no credentials in response)
}
```

#### Delete Connection
```http
DELETE /v1/connections/{id}

Response 204 No Content
```

### 3.2 GraphQL API

**Endpoint:** `/graphql`

#### Query User Connections
```graphql
query GetUserConnections($filter: CarrierFilter) {
  user_connections(filter: $filter) {
    edges {
      node {
        id
        carrier_id
        carrier_name
        display_name
        test_mode
        active
        capabilities
        credentials  # Available in GraphQL
        metadata
        config
        rate_sheet {
          id
          name
        }
      }
    }
  }
}
```

#### Query System Connections (Available for Enablement)
```graphql
query GetSystemConnections {
  system_connections {
    edges {
      node {
        id
        carrier_id
        carrier_name
        test_mode
        active
        # NOTE: credentials NOT available
      }
    }
  }
}
```

#### Enable System Connection
```graphql
mutation EnableSystemCarrier($data: EnableSystemCarrierMutationInput!) {
  enable_system_carrier(input: $data) {
    carrier {
      id
      carrier_id
      carrier_name
    }
  }
}

# Input:
{
  "data": {
    "id": "car_system123"
  }
}
```

#### Create User Connection
```graphql
mutation CreateConnection($data: CreateCarrierConnectionMutationInput!) {
  create_carrier_connection(input: $data) {
    connection {
      id
      carrier_id
      carrier_name
      credentials
    }
  }
}

# Input:
{
  "data": {
    "carrier_name": "fedex",
    "carrier_id": "my_fedex",
    "credentials": {
      "api_key": "xxx"
    }
  }
}
```

#### Update User Connection
```graphql
mutation UpdateConnection($data: UpdateCarrierConnectionMutationInput!) {
  update_carrier_connection(input: $data) {
    connection {
      id
      carrier_id
      credentials
    }
  }
}
```

---

## 4. SDK Integration

### 4.1 Gateway Creation

All connection types implement the same interface for SDK gateway creation:

```python
# Any connection type
connection = providers.CarrierConnection.objects.get(id="car_xxx")
# or
connection = providers.BrokeredConnection.objects.get(id="car_xxx")
# or
connection = providers.SystemConnection.objects.get(id="car_xxx")

# All have .gateway property
gateway = connection.gateway  # Returns karrio.api.gateway.Gateway

# Use gateway for operations
rates = karrio.Rating.fetch(request).from_(gateway).parse()
```

### 4.2 Connection Resolution

```python
# modules/core/karrio/server/core/gateway.py

from karrio.server.core.gateway import Connections

# List all accessible connections (CarrierConnection + BrokeredConnection)
connections = Connections.list(
    context=request,
    carrier_name="fedex",
    active=True,
    test_mode=False,
)

# Get first matching connection
connection = Connections.first(
    context=request,
    carrier_id="my_fedex",  # Matches by id OR carrier_id
)
```

### 4.3 Carrier Snapshot Utility

```python
# modules/core/karrio/server/core/utils.py

from karrio.server.core.utils import create_carrier_snapshot, resolve_carrier

# Create snapshot for storage
snapshot = create_carrier_snapshot(connection)
# Returns: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}

# Resolve connection from snapshot
connection = resolve_carrier(snapshot, context=request)
# Returns: CarrierConnection or BrokeredConnection or None
```

---

## 5. Frontend Integration

### 5.1 React Hooks

```typescript
// packages/hooks/carrier-connections.ts

import { useCarrierConnections } from "@karrio/hooks/carrier-connections";

function MyComponent() {
  const {
    query: { data, isLoading },
    createConnection,
    updateConnection,
    deleteConnection,
  } = useCarrierConnections();

  // data.user_connections contains all user's connections
  // (CarrierConnection + enabled BrokeredConnection)
}
```

### 5.2 GraphQL Queries (packages/types/graphql/queries.ts)

```typescript
export const GET_USER_CONNECTIONS = gql`
  query get_user_connections($filter: CarrierFilter) {
    user_connections(filter: $filter) {
      edges {
        node {
          id
          carrier_id
          carrier_name
          display_name
          test_mode
          active
          capabilities
          credentials
          metadata
          config
        }
      }
    }
  }
`;

export const GET_SYSTEM_CONNECTIONS = gql`
  query get_system_connections {
    system_connections {
      edges {
        node {
          id
          carrier_id
          carrier_name
          test_mode
          active
        }
      }
    }
  }
`;
```

### 5.3 Connection Dialog Component

```typescript
// packages/ui/components/carrier-connection-dialog.tsx

interface CarrierConnectionDialogProps {
  open: boolean;
  selectedConnection: Connection | null;  // null for create
  onSubmit: (values: FormData) => Promise<void>;
}

// Form fields:
// - carrier_name (select from available carriers)
// - carrier_id (user-defined identifier)
// - credentials (dynamic fields based on carrier)
// - config (operational settings)
// - metadata (custom key-value pairs)
```

---

## 6. Data Flow Diagrams

### 6.1 Connection List Request

```
┌─────────┐      ┌────────────┐      ┌─────────────────┐      ┌───────────────┐
│ Frontend│      │  REST/GQL  │      │ gateway.        │      │   Database    │
│         │      │    API     │      │ Connections     │      │               │
└────┬────┘      └─────┬──────┘      └───────┬─────────┘      └───────┬───────┘
     │                 │                     │                        │
     │ GET /connections│                     │                        │
     │────────────────>│                     │                        │
     │                 │ Connections.list()  │                        │
     │                 │────────────────────>│                        │
     │                 │                     │ Query CarrierConnection│
     │                 │                     │───────────────────────>│
     │                 │                     │ Query BrokeredConnection
     │                 │                     │───────────────────────>│
     │                 │                     │<── Combined results ───│
     │                 │<─ List[Connection]──│                        │
     │                 │                     │                        │
     │                 │ Serialize           │                        │
     │                 │ (REST: no creds)    │                        │
     │                 │ (GQL: with creds)   │                        │
     │<── Response ────│                     │                        │
```

### 6.2 Shipment Creation with Carrier

```
┌─────────┐    ┌────────────┐    ┌─────────────────┐    ┌───────────┐    ┌──────────┐
│ Frontend│    │  Shipment  │    │ utils.          │    │ Connection│    │ Carrier  │
│         │    │  Serializer│    │ resolve_carrier │    │           │    │ SDK      │
└────┬────┘    └─────┬──────┘    └───────┬─────────┘    └─────┬─────┘    └────┬─────┘
     │               │                   │                    │               │
     │ POST /shipments                   │                    │               │
     │ carrier_id: "ups_account"         │                    │               │
     │──────────────>│                   │                    │               │
     │               │ resolve_carrier() │                    │               │
     │               │──────────────────>│                    │               │
     │               │                   │ Try by id          │               │
     │               │                   │───────────────────>│               │
     │               │                   │ Try by carrier_id  │               │
     │               │                   │───────────────────>│               │
     │               │                   │<── Connection ─────│               │
     │               │<── Connection ────│                    │               │
     │               │                   │                    │               │
     │               │ conn.gateway.create()                  │               │
     │               │────────────────────────────────────────────────────────>│
     │               │                   │                    │               │
     │               │ create_snapshot() │                    │               │
     │               │──────────────────>│                    │               │
     │               │<── snapshot ──────│                    │               │
     │               │                   │                    │               │
     │               │ Save shipment with selected_rate.meta  │               │
     │<── Shipment ──│                   │                    │               │
```

### 6.3 System Connection Enablement

```
┌─────────┐      ┌────────────┐      ┌─────────────────┐      ┌───────────────┐
│ Frontend│      │  GraphQL   │      │ Mutation        │      │   Database    │
│         │      │    API     │      │ Handler         │      │               │
└────┬────┘      └─────┬──────┘      └───────┬─────────┘      └───────┬───────┘
     │                 │                     │                        │
     │ enable_system_carrier               │                        │
     │ {id: "car_system123"}               │                        │
     │────────────────>│                     │                        │
     │                 │ SystemCarrierMutation.enable()              │
     │                 │────────────────────>│                        │
     │                 │                     │ Get SystemConnection   │
     │                 │                     │───────────────────────>│
     │                 │                     │<── SystemConnection ───│
     │                 │                     │                        │
     │                 │                     │ Create BrokeredConn    │
     │                 │                     │───────────────────────>│
     │                 │                     │<── BrokeredConnection ─│
     │                 │                     │                        │
     │                 │                     │ Create Link (Insiders) │
     │                 │                     │───────────────────────>│
     │                 │<── BrokeredConn ────│                        │
     │<── Response ────│                     │                        │
```

---

## 7. Access Control

### 7.1 OSS Mode

| Connection Type | Access Rule |
|-----------------|-------------|
| CarrierConnection | `created_by = current_user` |
| BrokeredConnection | `created_by = current_user` |
| SystemConnection | Requires BrokeredConnection creation |

### 7.2 Insiders Mode (Multi-Organization)

| Connection Type | Access Rule |
|-----------------|-------------|
| CarrierConnection | `link__org = current_org` |
| BrokeredConnection | `link__org = current_org` |
| SystemConnection | Requires BrokeredConnection + BrokeredConnectionLink |

### 7.3 Admin Access

| Operation | Permission |
|-----------|------------|
| Manage SystemConnection | `is_staff = True` |
| View all CarrierConnections | `is_staff = True` |
| View all BrokeredConnections | `is_staff = True` |

---

## 8. Implementation Notes

### 8.1 Deferred Features

#### REST API for Enabling System Connections (Medium Priority - Deferred)

**Status:** Not implemented in current release

The REST API currently does not expose endpoints for enabling/disabling system connections. Users must use the GraphQL API (`enable_system_carrier` mutation) to enable system connections.

**Rationale:**
- GraphQL mutation provides full functionality for all current UI use cases
- REST API expansion can be added in a future release if needed
- Reduces API surface area and maintenance burden for initial release

**Future Implementation Path:**
If REST API support is needed, add these endpoints:
```http
POST /v1/connections/enable
{
  "system_connection_id": "car_system123",
  "config_overrides": {}  # optional
}

DELETE /v1/connections/{brokered_id}
# Standard delete works for disabling (deletes BrokeredConnection)
```

---

## 9. Migration Notes

### 9.1 From Legacy Carrier Model

The migration from the old `Carrier` model with `is_system` flag:

1. **Carriers with `is_system=False`** → `CarrierConnection` (renamed, same table)
2. **Carriers with `is_system=True`** → `SystemConnection` (new table)
3. **CarrierConfig per user/org** → `BrokeredConnection.config_overrides`
4. **active_users/active_orgs M2M** → `BrokeredConnection` records
5. **Carrier FK fields** → `carrier` JSONField (snapshot)

### 9.2 Key Migrations

| Migration | Purpose |
|-----------|---------|
| providers/0092 | Add SystemConnection, BrokeredConnection models |
| providers/0093 | Migrate system carriers data |
| providers/0094 | Remove legacy fields (is_system, active_users) |
| providers/0095 | Rename Carrier → CarrierConnection |
| manager/0077 | Add carrier snapshot fields |
| manager/0078 | Populate carrier snapshots from FKs |
| manager/0079 | Remove carrier FK fields |

---

## File Locations

```
modules/
├── core/karrio/server/
│   ├── providers/
│   │   ├── models/
│   │   │   ├── carrier.py          # CarrierConnection model
│   │   │   └── connection.py       # SystemConnection, BrokeredConnection
│   │   ├── serializers/
│   │   │   └── base.py             # REST API serializers
│   │   └── views/
│   │       └── connections.py      # REST API views
│   └── core/
│       ├── gateway.py              # Connections.list(), Connections.first()
│       └── utils.py                # create_carrier_snapshot(), resolve_carrier()
├── graph/karrio/server/graph/
│   └── schemas/base/
│       ├── types.py                # GraphQL types
│       └── mutations.py            # GraphQL mutations
└── manager/karrio/server/manager/
    └── models.py                   # Shipment, Tracking, Pickup with carrier snapshot

packages/
├── hooks/
│   └── carrier-connections.ts      # React hooks
├── types/graphql/
│   └── queries.ts                  # GraphQL query definitions
└── ui/components/
    └── carrier-connection-dialog.tsx  # Connection form component
```

---

*Document generated from codebase analysis - January 2026*
