# PRD: OSS Admin GraphQL, Worker Monitoring & DevTools Admin Mode

**Status**: Planning
**Created**: 2026-02-13
**Author**: Claude Code

---

## Problem Statement

The Karrio admin GraphQL endpoint currently lives entirely in `ee/insiders/modules/admin/`, making it unavailable to OSS deployments. This means OSS users have **no admin API** for managing their instance (users, system carriers, configs, rate sheets). Meanwhile, there is no visibility into Huey background worker health, job history, or queue state anywhere in the system.

Five things need to come together:

1. **OSS Admin GraphQL** — Core admin capabilities (user management, instance config, system carriers, rate sheets) should be available to all Karrio deployments, not just insiders.
2. **Worker Monitoring** — A Huey job dashboard exposing queue state, task execution history, periodic task schedules, and worker health.
3. **DevTools Admin Mode** — The developer tools drawer should have an admin-only mode where system health and worker monitoring are exposed. This data is served by the admin GraphQL endpoint, not the base GraphQL.
4. **Frontend Admin Dashboard in OSS** — The admin dashboard pages (Console, Staff & Permissions, Carrier Network) must be enabled in OSS builds, with sidebar navigation scoped appropriately per build variant.
5. **Dynamic System Configuration** — The platform console must support ALL dynamic carrier plugin system-level configurations (auto-discovered from installed carriers), along with email, data retention, feature flags, address validation, and plugin registry settings.

---

## Architecture Overview

### Current State

```
ee/insiders/modules/admin/
└── karrio/server/admin/
    ├── schema.py               # Dynamic schema composition
    ├── schemas/base/           # ALL admin queries/mutations (36KB types, 32KB mutations)
    │   ├── types.py            # SystemUserType, InstanceConfigType, OrganizationAccountType, MarkupType, FeeType...
    │   ├── inputs.py           # UserFilter, AccountFilter, MarkupFilter...
    │   └── mutations.py        # create_user, update_configs, create_system_carrier_connection, create_organization_account...
    ├── utils.py                # staff_required, superuser_required decorators
    ├── urls.py                 # /admin/graphql/
    └── views.py                # GraphQLView with admin schema

ee/insiders/modules/orgs/
└── karrio/server/admin/schemas/orgs/    # Org-specific admin extensions (compiled .pyc only)
```

**Problems:**
- Everything is in `ee/insiders/` — OSS gets zero admin API
- OSS-applicable features (user management, instance config, system carriers, rate sheets) are bundled with insiders-only features (org management, markups, fees)
- No worker monitoring exists anywhere
- DevTools has no concept of admin vs regular mode

### Target State

```
modules/admin/                              # NEW: OSS admin module
└── karrio/server/admin/
    ├── schema.py                           # Dynamic schema composition (same pattern)
    ├── schemas/base/                       # OSS admin queries/mutations
    │   ├── types.py                        # SystemUserType, InstanceConfigType, SystemCarrierConnectionType, SystemRateSheetType, WorkerTypes...
    │   ├── inputs.py                       # UserFilter, SystemCarrierConnectionFilter...
    │   └── mutations.py                    # create_user, update_configs, system carrier CRUD, rate sheet CRUD
    ├── utils.py                            # staff_required, superuser_required decorators
    ├── urls.py                             # /admin/graphql/
    ├── views.py                            # GraphQLView with admin schema
    └── worker/                             # NEW: Huey monitoring
        ├── models.py                       # TaskExecution model
        ├── signals.py                      # Huey signal handlers
        └── management/commands/
            └── cleanup_task_history.py     # Retention cleanup

ee/insiders/modules/admin/                  # REFACTORED: Insiders admin extensions only
└── karrio/server/admin/schemas/insiders/   # Extends OSS admin via pkgutil
    ├── types.py                            # OrganizationAccountType, MarkupType, FeeType, AccountUsageType...
    ├── inputs.py                           # AccountFilter, MarkupFilter, FeeFilter...
    └── mutations.py                        # create_organization_account, create_markup, invite_organization_user...

ee/insiders/modules/orgs/
└── karrio/server/admin/schemas/orgs/       # Unchanged (already follows the pattern)
```

---

## Phase 1: Admin Module Refactor (OSS Extraction)

### 1.1 Create `modules/admin/` — OSS Admin Module

Move OSS-applicable admin features from `ee/insiders/modules/admin/` to `modules/admin/`.

**What moves to OSS (`modules/admin/schemas/base/`):**

| Feature | Queries | Mutations |
|---------|---------|-----------|
| **Current user** | `me` | — |
| **User management** | `user`, `users`, `permission_groups` | `create_user`, `update_user`, `remove_user` |
| **Instance config** | `configs` | `update_configs` |
| **System usage** | `usage` (basic, without addons) | — |
| **System carriers** | `system_carrier_connection`, `system_carrier_connections` | `create_system_carrier_connection`, `update_system_carrier_connection`, `delete_system_carrier_connection` |
| **Rate sheets** | `rate_sheet`, `rate_sheets` | Full rate sheet CRUD (create, update, delete, zones, surcharges, service rates, weight ranges) |
| **System data access** | `shipments`, `trackers`, `orders` (system-wide) | — |

**Types that move to OSS:**
- `SystemUserType`
- `PermissionGroupType`
- `InstanceConfigType`
- `SystemUsageType` (basic — without addons_charges)
- `SystemCarrierConnectionType`
- `SystemRateSheetType`
- `SystemShipmentType`, `SystemTrackerType`, `SystemOrderType`

**What stays in insiders (`ee/insiders/modules/admin/schemas/insiders/`):**

| Feature | Queries | Mutations |
|---------|---------|-----------|
| **Organization accounts** | `account`, `accounts` | `create_organization_account`, `update_organization_account`, `disable_organization_account`, `delete_organization_account`, `invite_organization_user` |
| **Markups/Pricing** | `markup`, `markups`, `fee`, `fees` | `create_markup`, `update_markup`, `delete_markup` |
| **Account carriers** | `carrier_connection`, `carrier_connections` | — |
| **Admin usage (extended)** | `usage` override with `AdminSystemUsageType` | — |

**Types that stay in insiders:**
- `OrganizationAccountType`, `OrganizationMemberType`
- `AccountUsageType`, `AdminSystemUsageType`
- `MarkupType`, `FeeType`
- `AccountCarrierConnectionType`
- `ResourceUsageType`

### 1.2 Infrastructure that moves to OSS

| File | Purpose |
|------|---------|
| `schema.py` | Dynamic schema composition via `pkgutil.iter_modules()` |
| `utils.py` | `staff_required`, `superuser_required` decorators |
| `urls.py` | `/admin/graphql/` endpoint registration |
| `views.py` | `GraphQLView` with admin schema |
| `apps.py` | `AdminConfig` Django app |
| `forms.py` | `CreateUserForm` |
| `settings/admin.py` | `INSTALLED_APPS` + `KARRIO_URLS` registration |

### 1.3 Insiders admin module becomes a schema extension

The refactored `ee/insiders/modules/admin/` becomes lightweight — it only contributes additional Query/Mutation classes via the `karrio.server.admin.schemas` namespace package (using `pkgutil.extend_path`), exactly like `ee/insiders/modules/orgs/karrio/server/admin/schemas/orgs/` already does.

**No changes needed to the schema composition logic** — `pkgutil.iter_modules()` will discover both `base` (from OSS) and `insiders` (from ee) schema modules automatically.

---

## Phase 2: Worker Monitoring Backend

### 2.1 Task Execution Model

New Django model in `modules/admin/karrio/server/admin/worker/models.py`:

```python
class TaskExecution(models.Model):
    task_id = models.CharField(max_length=100, db_index=True)       # Huey task UUID
    task_name = models.CharField(max_length=200, db_index=True)     # e.g. "background_trackers_update"
    status = models.CharField(max_length=20, db_index=True)         # executing, complete, error, retrying, revoked, expired
    queued_at = models.DateTimeField(null=True)                     # SIGNAL_ENQUEUED timestamp
    started_at = models.DateTimeField(null=True)                    # SIGNAL_EXECUTING timestamp
    completed_at = models.DateTimeField(null=True)                  # SIGNAL_COMPLETE/ERROR timestamp
    duration_ms = models.IntegerField(null=True)                    # Computed from started_at -> completed_at
    error = models.TextField(null=True, blank=True)                 # Exception traceback on SIGNAL_ERROR
    retries = models.IntegerField(default=0)                        # Retry count
    args_summary = models.TextField(null=True, blank=True)          # Truncated JSON of task args (for debugging)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["task_name", "status"]),
            models.Index(fields=["-started_at"]),
        ]
```

### 2.2 Huey Signal Handlers

In `modules/admin/karrio/server/admin/worker/signals.py`:

```python
@huey.signal()
def task_signal_handler(signal, task, exc=None):
    # Upsert TaskExecution record based on task.id
    # Map Huey signals to status updates:
    #   SIGNAL_ENQUEUED  -> create record, set queued_at
    #   SIGNAL_EXECUTING -> set started_at, status="executing"
    #   SIGNAL_COMPLETE  -> set completed_at, status="complete", compute duration
    #   SIGNAL_ERROR     -> set completed_at, status="error", store traceback
    #   SIGNAL_RETRYING  -> increment retries, status="retrying"
    #   SIGNAL_REVOKED   -> status="revoked"
    #   SIGNAL_EXPIRED   -> status="expired"
```

### 2.3 Admin GraphQL — Worker Queries

New schema module `modules/admin/karrio/server/admin/schemas/base/` (added to existing base):

**Queries:**

```graphql
# Task execution history (from DB)
type TaskExecutionType {
  id: ID!
  task_id: String!
  task_name: String!
  status: String!
  queued_at: DateTime
  started_at: DateTime
  completed_at: DateTime
  duration_ms: Int
  error: String
  retries: Int
  args_summary: String
}

# Live queue state (from Huey introspection API)
type QueueInfoType {
  pending_count: Int!
  scheduled_count: Int!
  result_count: Int!
}

# Registered periodic tasks
type PeriodicTaskType {
  name: String!
  schedule: String!           # Human-readable cron description
  last_execution: TaskExecutionType
}

# Top-level worker health
type WorkerHealthType {
  queue: QueueInfoType!
  periodic_tasks: [PeriodicTaskType!]!
  recent_errors: [TaskExecutionType!]!
  task_stats: [TaskStatsType!]!        # Per-task success/error counts
}

type Query {
  worker_health: WorkerHealthType!                                    @staff_required
  task_executions(filter: TaskExecutionFilter): TaskExecutionConnection! @staff_required
  task_execution(id: ID!): TaskExecutionType                          @staff_required
}
```

**Filter:**

```graphql
input TaskExecutionFilter {
  task_name: String
  status: String              # executing, complete, error, retrying
  date_after: DateTime
  date_before: DateTime
  offset: Int
  first: Int
}
```

### 2.4 Retention Cleanup

Management command `cleanup_task_history` and a periodic Huey task:

```python
@db_periodic_task(crontab(hour=3, minute=0))  # Daily at 3:00 AM
def cleanup_old_task_executions():
    cutoff = timezone.now() - timedelta(days=TASK_HISTORY_RETENTION_DAYS)  # Default: 7
    TaskExecution.objects.filter(completed_at__lt=cutoff).delete()
```

---

## Phase 3: DevTools Admin Mode

### 3.1 Admin Mode Context

Extend the `DeveloperToolsContext` to support admin mode:

```typescript
// developer-tools-context.tsx
export type DeveloperView =
  | "activity"
  | "api-keys"
  | "logs"
  | "events"
  | "tracing-records"
  | "apps"
  | "webhooks"
  | "playground"
  | "graphiql"
  // Admin-only views (visible only when isAdminMode=true)
  | "workers"
  | "system-health";

interface DeveloperToolsContextType {
  // ... existing fields
  isAdminMode: boolean;          // true when user is staff/superuser
}
```

Admin mode is determined by checking the user's `is_staff` flag from the session. When `isAdminMode=true`, additional tabs appear in the devtools sidebar.

### 3.2 Admin GraphQL Client

The admin-only devtools views need to query `/admin/graphql/` instead of `/graphql/`. Add a dedicated hook or client configuration:

```typescript
// hooks/admin.ts
export function useAdminQuery<T>({ queryKey, query, variables }) {
  // Same as useAuthenticatedQuery but targets /admin/graphql/ endpoint
}
```

### 3.3 Workers View (DevTools Tab)

New devtools tab: **Workers** (visible only in admin mode)

**Left Panel — Task Execution List:**
- Same split-panel pattern as Logs/Events/Tracing
- Each item shows: task name badge, status badge (complete/error/retrying), duration, timestamp
- Filter dropdown: task name, status, date range

**Right Panel — Task Detail:**
- Header: task name + status badge, Copy button top-right
- Metadata lines: task_id, queued_at, started_at, completed_at, duration, retries
- Error traceback in CodeMirror (when status=error)
- Args summary in CodeMirror

**Queue Overview Header:**
- Displayed above the list: pending count, scheduled count, result count
- Auto-refreshes every 10 seconds

### 3.4 System Health View (DevTools Tab)

New devtools tab: **System** (visible only in admin mode)

- **Periodic Tasks Table**: name, cron schedule (human-readable), last run status, last run time
- **Queue Gauges**: pending, scheduled, stored results
- **Error Rate**: recent error count / total executions (last 24h)
- **Task Breakdown**: per-task-name success/error counts

---

## Phase 4: Frontend Hooks & Types

### 4.1 GraphQL Queries

```typescript
// packages/types/graphql/queries.ts

export const GET_WORKER_HEALTH = gql`
  query get_worker_health {
    worker_health {
      queue { pending_count scheduled_count result_count }
      periodic_tasks { name schedule last_execution { status completed_at duration_ms } }
      recent_errors { id task_name error started_at }
      task_stats { task_name total_count error_count avg_duration_ms }
    }
  }
`;

export const GET_TASK_EXECUTIONS = gql`
  query get_task_executions($filter: TaskExecutionFilter) {
    task_executions(filter: $filter) {
      page_info { count has_next_page has_previous_page start_cursor end_cursor }
      edges {
        node {
          id task_id task_name status
          queued_at started_at completed_at
          duration_ms error retries args_summary
        }
      }
    }
  }
`;
```

### 4.2 Hooks

```typescript
// packages/hooks/admin/worker.ts
export function useWorkerHealth() { ... }
export function useTaskExecutions(filter) { ... }
```

These hooks use the admin GraphQL client (targeting `/admin/graphql/`).

---

## Phase 5: Frontend Admin Dashboard for OSS

### 5.1 Problem — Admin Dashboard Currently Insiders-Only

The admin dashboard frontend (`packages/admin/`) and its pages already exist but are gated behind two conditions that effectively limit them to insiders builds:

1. **`ADMIN_DASHBOARD` constance flag** — Auto-detected via `importlib.util.find_spec("karrio.server.admin")` in `apps/api/karrio/server/settings/constance.py:69`. Currently only resolves when the insiders admin module is installed.
2. **`is_staff` user flag** — Already works for any deployment.

**Navigation gating** (`packages/ui/components/sidebar.tsx:114`):
```typescript
...(metadata?.ADMIN_DASHBOARD && user?.is_staff ? [{
  title: "Platform",
  url: "/admin",
  icon: Shield,
  items: [
    { title: "Console", url: "/admin" },
    { title: "Staff & Permissions", url: "/admin/staff" },
  ],
}] : []),
```

**Server-side gating** (`apps/dashboard/src/app/(base)/(dashboard)/admin/layout.tsx:24`):
```typescript
if (!(user.user as any)?.is_staff || !metadata.metadata?.ADMIN_DASHBOARD) {
  redirect("/");
}
```

### 5.2 What "Just Works" Once `modules/admin/` Exists

Once the OSS admin module (`modules/admin/`) is created (Phase 1), the following will work **automatically with zero frontend changes**:

| Component | Why It Works |
|-----------|-------------|
| `ADMIN_DASHBOARD` flag | `find_spec("karrio.server.admin")` resolves to the new OSS module |
| Sidebar "Platform" nav group | `metadata?.ADMIN_DASHBOARD` becomes `true` |
| Admin layout permission check | Same flag + `is_staff` check passes |
| `/admin` (Console) page | `packages/admin/modules/platform/index.tsx` renders using `useConfigs()` hook |
| `/admin/staff` page | `packages/admin/modules/staff/index.tsx` renders using admin GraphQL |

### 5.3 Admin Pages Scoped for OSS

The admin sidebar navigation needs adjustment to show the right pages per build variant:

**OSS Admin Pages:**

| Page | Route | Package | Description |
|------|-------|---------|-------------|
| Console | `/admin` | `packages/admin/modules/platform/` | Platform settings, email, data retention, feature flags, address validation, **dynamic carrier system configs** |
| Staff & Permissions | `/admin/staff` | `packages/admin/modules/staff/` | User management, permission groups |
| Carrier Network | `/admin/carriers` | `packages/admin/modules/carriers/` | System carrier connections, rate sheets |

**Insiders-Only Pages (not shown in OSS):**

| Page | Route | Condition |
|------|-------|-----------|
| Shippers Overview | `/shippers/overview` | `metadata?.MULTI_ORGANIZATIONS` |
| Accounts | `/shippers/accounts` | `metadata?.MULTI_ORGANIZATIONS` |
| Markups | `/shippers/markups` | `metadata?.MULTI_ORGANIZATIONS` |

Currently the Carrier Network link is nested under the "Shippers" nav group (which requires `MULTI_ORGANIZATIONS`). For OSS, the Carrier Network page should be accessible directly under the "Platform" admin nav group.

**Required sidebar change** (`packages/ui/components/sidebar.tsx`):
```typescript
...(metadata?.ADMIN_DASHBOARD && user?.is_staff ? [{
  title: "Platform",
  url: "/admin",
  icon: Shield,
  items: [
    { title: "Console", url: "/admin" },
    { title: "Staff & Permissions", url: "/admin/staff" },
    { title: "Carrier Network", url: "/admin/carriers" },  // NEW: always visible in admin
  ],
}] : []),
```

### 5.4 Dynamic Carrier System Config in Platform Console

**Problem:** The platform console (`packages/admin/modules/platform/index.tsx`) has a **hardcoded** `ConfigData` type with a fixed set of config keys. It does NOT render dynamic carrier plugin system configs (e.g., `DHL_PARCEL_DE_USERNAME`, `TELESHIP_OAUTH_CLIENT_ID`).

**Backend already supports this.** The `CONSTANCE_CONFIG` dict (`apps/api/karrio/server/settings/constance.py:195-247`) dynamically merges:
- Email config (6 keys)
- Address validation (2 keys)
- Data retention (4 keys)
- Feature flags (dynamic, module-dependent)
- Plugin registry (dynamic, per installed carrier)
- **Plugin system configs** (`PLUGIN_SYSTEM_CONFIG`) — dynamic per-carrier config keys from `ref.SYSTEM_CONFIGS`

The `InstanceConfigType` GraphQL type (`ee/insiders/.../types.py:467-479`) is **dynamically generated** from ALL `CONSTANCE_CONFIG` keys:
```python
InstanceConfigType = strawberry.type(
    type(
        "InstanceConfigType",
        (_InstanceConfigType,),
        {
            **{k: strawberry.UNSET for k, _ in conf.settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in conf.settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)
```

So the admin GraphQL already exposes carrier plugin configs — the frontend just doesn't render them.

**Solution — New `config_fieldsets` query:**

Add a new admin GraphQL query that exposes the `CONSTANCE_CONFIG_FIELDSETS` structure, so the frontend can discover and render dynamic sections:

```graphql
type ConfigFieldsetType {
  name: String!              # e.g. "DHL Parcel DE Config"
  keys: [String!]!           # e.g. ["DHL_PARCEL_DE_USERNAME", "DHL_PARCEL_DE_PASSWORD"]
}

type ConfigSchemaType {
  key: String!               # e.g. "DHL_PARCEL_DE_USERNAME"
  description: String!       # e.g. "DHL Parcel DE account username"
  value_type: String!        # "str", "bool", "int"
  default_value: String      # JSON-encoded default
}

type Query {
  config_fieldsets: [ConfigFieldsetType!]!    @staff_required
  config_schema: [ConfigSchemaType!]!         @staff_required
}
```

**Frontend platform console changes** (`packages/admin/modules/platform/index.tsx`):

1. **Replace hardcoded `ConfigData` type** with a dynamic approach:
   - Fetch `config_fieldsets` and `config_schema` from admin GraphQL
   - Render config sections dynamically based on fieldsets
   - The existing hardcoded sections (Email, Administration, Features, Data Retention, Address Validation) can remain as "known" sections with tailored UI
   - Dynamic carrier plugin config sections (from `PLUGIN_SYSTEM_CONFIG_FIELDSETS`) are rendered as generic key-value config cards

2. **Add "Carrier Configs" section** to the platform console:
   ```typescript
   {/* Dynamic Carrier Plugin Configs */}
   {pluginFieldsets.map(fieldset => (
     <Card key={fieldset.name}>
       <CardHeader>
         <CardTitle>{fieldset.name}</CardTitle>
         <CardDescription>System-level carrier configuration</CardDescription>
       </CardHeader>
       <CardContent>
         {fieldset.keys.map(key => (
           <ConfigField key={key} configKey={key} schema={schemaMap[key]} value={configs[key]} />
         ))}
       </CardContent>
     </Card>
   ))}
   ```

3. **Update `GetConfigs` query** to request all config keys dynamically (not just the hardcoded subset):
   ```typescript
   // Instead of hardcoding fields in the query, use config_schema keys
   // to build a dynamic query or fetch configs as a JSON blob
   export const GET_CONFIGS = gql`
     query get_configs {
       configs {
         // Known fields stay explicit for type safety
         EMAIL_USE_TLS EMAIL_HOST_USER EMAIL_HOST_PASSWORD EMAIL_HOST EMAIL_PORT EMAIL_FROM_ADDRESS
         GOOGLE_CLOUD_API_KEY CANADAPOST_ADDRESS_COMPLETE_API_KEY
         ORDER_DATA_RETENTION TRACKER_DATA_RETENTION SHIPMENT_DATA_RETENTION API_LOGS_DATA_RETENTION
         ALLOW_SIGNUP ALLOW_ADMIN_APPROVED_SIGNUP ADMIN_DASHBOARD MULTI_ORGANIZATIONS
         ORDERS_MANAGEMENT APPS_MANAGEMENT DOCUMENTS_MANAGEMENT DATA_IMPORT_EXPORT
         WORKFLOW_MANAGEMENT SHIPPING_RULES PERSIST_SDK_TRACING AUDIT_LOGGING ALLOW_MULTI_ACCOUNT
       }
       config_fieldsets { name keys }
       config_schema { key description value_type default_value }
     }
   `;
   ```

   Alternatively, the `update_configs` mutation already accepts arbitrary key-value pairs — the frontend can send any config key regardless of the static type.

### 5.5 Email Configuration

Email configuration is **already fully supported** in the platform console:
- `CONSTANCE_CONFIG` has all 6 email keys (TLS, host, port, user, password, from address)
- `InstanceConfigType` exposes them via GraphQL
- `packages/admin/modules/platform/index.tsx` renders the "Email Configuration" card with edit dialog
- `update_configs` mutation accepts email config updates

**No changes needed** for email config — it works in OSS as-is once the admin module is available.

### 5.6 Plugin Registry Config

The platform console should also render the **Plugin Registry** section, showing which carrier plugins are enabled/disabled:
- Backend: `PLUGIN_REGISTRY` in `constance.py:165-179` — generates `{CARRIER_NAME}_ENABLED` boolean flags
- Frontend: Render as a toggleable list of installed carrier plugins

This is a new section in the platform console (currently not rendered).

### 5.7 Admin GraphQL Queries for Platform Console

The existing admin queries from `packages/types/graphql/admin/queries.ts` that the platform console depends on:

| Query | Purpose | OSS? |
|-------|---------|------|
| `GET_CONFIGS` | Fetch all `InstanceConfigType` fields | Yes |
| `UPDATE_CONFIGS` | Update any config key-value pairs | Yes |
| `GET_ADMIN_SYSTEM_USAGE` | Usage stats (user count, shipments, etc.) | Yes (basic) |
| `GET_ADMIN_USERS` | Staff management | Yes |
| `CREATE_USER` / `UPDATE_USER` / `REMOVE_USER` | User CRUD | Yes |
| `GET_SYSTEM_CONNECTIONS` | System carrier connections | Yes |
| `GET_ADMIN_ACCOUNTS` / org management queries | Org management | Insiders only |

---

## Migration Strategy

### Step-by-step execution order:

1. **Create `modules/admin/` package skeleton** — `pyproject.toml`, `apps.py`, `settings/admin.py`, `urls.py`, `views.py`, `schema.py`, `utils.py`
2. **Extract OSS types/inputs/mutations** — Copy applicable types from `ee/insiders/modules/admin/schemas/base/` to `modules/admin/schemas/base/`, removing org/markup/fee references
3. **Refactor insiders admin** — Remove extracted code from `ee/insiders/modules/admin/schemas/base/`, move remaining insiders-only features to `ee/insiders/modules/admin/schemas/insiders/`
4. **Verify both endpoints** — OSS admin serves base queries, insiders admin serves base + insiders queries
5. **Add `config_fieldsets` and `config_schema` queries** — Expose `CONSTANCE_CONFIG_FIELDSETS` structure via admin GraphQL for frontend dynamic rendering
6. **Add worker monitoring backend** — `TaskExecution` model, signal handlers, GraphQL schema
7. **Add devtools admin mode** — Context extension, admin GraphQL client, conditional tab rendering
8. **Build Workers view** — Split-panel list/detail with filters
9. **Build System Health view** — Overview dashboard with periodic tasks and queue state
10. **Update sidebar navigation** — Move Carrier Network link under Platform admin group, ensure OSS admin pages are visible
11. **Update platform console** — Add dynamic carrier plugin config sections, plugin registry section
12. **Update `GetConfigs` query & `ConfigData` type** — Include `config_fieldsets`, `config_schema` queries, render dynamic sections
13. **Tests** — Admin GraphQL tests for OSS, worker signal tests, platform console E2E, retention cleanup tests

### Backward Compatibility

- The `/admin/graphql/` endpoint URL does not change
- Insiders deployments get the same queries/mutations they have today (OSS base + insiders extensions)
- OSS deployments gain admin capabilities they didn't have before
- The `ADMIN_DASHBOARD` feature flag continues to work
- No database migration conflicts — `TaskExecution` is a new model

---

## Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `modules/admin/pyproject.toml` | Package definition |
| `modules/admin/karrio/server/admin/__init__.py` | Package init |
| `modules/admin/karrio/server/admin/apps.py` | Django app config |
| `modules/admin/karrio/server/admin/schema.py` | Dynamic schema composition |
| `modules/admin/karrio/server/admin/utils.py` | `staff_required`, `superuser_required` |
| `modules/admin/karrio/server/admin/urls.py` | `/admin/graphql/` |
| `modules/admin/karrio/server/admin/views.py` | GraphQL view |
| `modules/admin/karrio/server/admin/forms.py` | `CreateUserForm` |
| `modules/admin/karrio/server/admin/schemas/__init__.py` | pkgutil namespace |
| `modules/admin/karrio/server/admin/schemas/base/__init__.py` | Query + Mutation |
| `modules/admin/karrio/server/admin/schemas/base/types.py` | OSS admin types |
| `modules/admin/karrio/server/admin/schemas/base/inputs.py` | OSS admin inputs |
| `modules/admin/karrio/server/admin/schemas/base/mutations.py` | OSS admin mutations |
| `modules/admin/karrio/server/admin/worker/models.py` | `TaskExecution` model |
| `modules/admin/karrio/server/admin/worker/signals.py` | Huey signal handlers |
| `modules/admin/karrio/server/admin/worker/management/commands/cleanup_task_history.py` | Retention |
| `modules/admin/karrio/server/settings/admin.py` | Settings registration |
| `packages/hooks/admin/worker.ts` | `useWorkerHealth`, `useTaskExecutions` |
| `packages/developers/components/views/workers-view.tsx` | Workers devtools tab |
| `packages/developers/components/views/system-health-view.tsx` | System health devtools tab |

### Modified Files

| File | Change |
|------|--------|
| `ee/insiders/modules/admin/karrio/server/admin/schemas/base/` | Remove OSS-applicable code, keep only insiders features. Rename to `schemas/insiders/` |
| `ee/insiders/modules/admin/karrio/server/settings/admin.py` | Depend on OSS admin module, only add insiders extensions |
| `packages/developers/context/developer-tools-context.tsx` | Add `isAdminMode`, add `"workers"` and `"system-health"` views |
| `packages/developers/components/developer-tools-drawer.tsx` | Conditionally render admin tabs |
| `packages/types/graphql/queries.ts` | Add worker/system health queries |
| `packages/types/graphql/types.ts` | Add worker/system health types |
| `packages/types/graphql/admin/queries.ts` | Add `config_fieldsets`, `config_schema` queries |
| `packages/types/graphql/admin/types.ts` | Add `ConfigFieldsetType`, `ConfigSchemaType` types |
| `packages/hooks/index.tsx` | Export admin hooks |
| `packages/hooks/admin-platform.ts` | Update `useConfigs` to also fetch fieldsets and schema |
| `packages/ui/components/sidebar.tsx` | Move Carrier Network link under Platform admin group for OSS visibility |
| `packages/admin/modules/platform/index.tsx` | Add dynamic carrier plugin config sections, plugin registry section, replace hardcoded `ConfigData` for dynamic keys |
| `apps/api/karrio/server/settings/base.py` | Update `ADMIN_DASHBOARD` detection for new module path |

---

## Effort Estimate

| Phase | Scope | Estimate |
|-------|-------|----------|
| Phase 1 | Admin module refactor (OSS extraction) | 3–4 days |
| Phase 2 | Worker monitoring backend (model, signals, GraphQL) | 2–3 days |
| Phase 3 | DevTools admin mode + UI views | 2–3 days |
| Phase 4 | Frontend hooks, types, integration | 1–2 days |
| Phase 5 | Frontend admin dashboard for OSS (sidebar, platform console, dynamic configs) | 2–3 days |
| Testing | Admin GraphQL, worker signals, platform console E2E | 1–2 days |
| **Total** | | **11–17 days** |

---

## Open Questions

- **Q1**: Should the worker monitoring `TaskExecution` model use the same database as the main app, or a separate DB (to avoid write contention from high-frequency signal handlers)?
- **Q2**: Should the admin GraphQL client in the frontend reuse the same auth token, or require a separate admin session?
- **Q3**: For the system health view, should we include Redis connection health / storage backend metrics? (Requires direct Redis introspection beyond Huey's API.)
- **Q4**: Should rate sheet management stay in OSS admin or move to insiders (since it's a pricing feature)?
- **Q5**: For dynamic carrier plugin configs: should the platform console use a fully dynamic rendering approach (generic key-value cards driven by `config_fieldsets`), or should we generate static TS types at build time from the installed carrier plugins?
- **Q6**: Should the `GetConfigs` query be refactored to return configs as a JSON blob (`configs_json: JSONString`) instead of individual typed fields, to avoid needing to regenerate TS types when new carrier plugins are installed?

## Resolved Design Decisions

- **Email config in OSS**: Already fully supported — the platform console has email config editing, `CONSTANCE_CONFIG` exposes all 6 email keys, `update_configs` mutation handles them. No additional work needed.
- **`ADMIN_DASHBOARD` flag auto-enablement**: `importlib.util.find_spec("karrio.server.admin")` in `constance.py:69` will automatically detect the new `modules/admin/` package. No manual flag setting needed for OSS.
- **Admin auth reuse**: The existing `KarrioClient` in `packages/types/index.ts` already has dual GraphQL clients (`karrio.graphql` for regular API, `karrio.admin` for admin API), both using the same session auth token. This pattern continues for OSS.
