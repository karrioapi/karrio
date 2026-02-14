# Developer Tools: Event Timeline & Tracing Records Enhancement

<!--
PRD TYPE: ENHANCEMENT
SCOPE: Devtools event detail timeline + dedicated tracing records tab
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-13 |
| Status | Implemented |
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

This PRD proposes two enhancements to the Developer Tools drawer:

1. **Event detail timeline**: When viewing an event in devtools, show its full activity timeline (associated API logs + tracing records) using the same `ActivityTimeline` component already used on shipment, tracker, pickup, and order detail pages. Currently the event detail view only shows raw JSON data with no timeline or associated API calls.

2. **Dedicated tracing records tab**: Add a new "Tracing Records" tab to the devtools sidebar that provides a standalone view of all carrier-level API calls (background requests, tracking polls, webhook deliveries, etc.) — including those not triggered by a user-facing REST API call. Currently, tracing records are only visible nested inside API log entries and there is no way to browse them independently.

### Key Architecture Decisions

1. **Reuse `ActivityTimeline` for event detail**: The event `data.id` field contains the entity ID (`shp_*`, `trk_*`, `pck_*`, `ord_*`) which can be passed directly to `useLogs({ entity_id })` and `useEvents({ entity_id })` — no backend changes needed.
2. **New `TracingRecords` devtools tab**: Uses the existing `GET_TRACING_RECORDS` GraphQL query and `TracingRecordFilter` — requires a new view component, a new hook, and adding the tab to the drawer sidebar.
3. **No backend schema changes**: All required GraphQL queries, filters, and resolvers already exist (`tracing_records`, `TracingRecordType`, `TracingRecordFilter`).
4. **Consistent dark-theme drawer styling**: Both new views follow the existing devtools dark theme using the scoped CSS variables and shadcn/ui components.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Event detail view with `ActivityTimeline` | Changes to the Event Django model |
| New "Tracing Records" devtools tab | New GraphQL mutations |
| `useTracingRecords` hook for tracing record list | TracingRecord model field changes |
| Tracing record detail viewer with request/response | Changes to shipment/tracker/pickup detail pages |
| Filtering by carrier, date range, keyword | New REST API endpoints |
| Entity ID cross-linking from tracing records | Changes to public tracking page |

---

## Open Questions & Decisions

### Pending Questions

_None — all questions resolved._

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Backend changes for event timeline | None needed | Event `data.id` gives entity_id; `useLogs` and `useEvents` already filter by `entity_id` | 2026-02-13 |
| D2 | GraphQL changes for tracing records tab | Frontend types added | `GET_TRACING_RECORDS` query and `TracingRecordFilter` already exist in backend schema; TS types/queries added to `packages/types/graphql/` | 2026-02-13 |
| D3 | Tracing records tab placement | After "Events" in sidebar | Natural developer workflow: Activity → API Keys → Logs → Events → Tracing Records → ... | 2026-02-13 |
| D4 | Event detail display mode | Tabbed layout: "Timeline" + "Event Data" (Timeline default) | Matches the API log detail pattern which uses tabs (API Response / API Request / Timeline) | 2026-02-13 |
| D5 | Q1: Event detail view tab vs replace | A) Replace with tabbed view (Timeline / Event Data) | Timeline is the primary debugging view; Event Data tab preserves raw JSON access | 2026-02-13 |
| D6 | Q2: Tracing records duration column | B) No, keep simple for initial release | Can be added later as P1; avoids client-side timestamp pairing complexity | 2026-02-13 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Event has no associated entity_id in data | Timeline would be empty | Show "No associated activity" message, still show raw event data | ❌ No |
| Background tracing records not linked to any API log | Records won't appear in API log timeline tab | This is the core motivation for the standalone tracing records tab | ❌ No |

---

## Problem Statement

### Current State

**Event detail view** (`packages/developers/modules/event.tsx`): Shows only event type, date, source, and raw JSON data. No timeline, no associated API logs, no tracing records.

```typescript
// Current event detail — raw JSON only, no timeline
export const EventComponent = ({ eventId }: { eventId: string }) => {
  const { query: { data: { event } = {} } } = useEvent(entity_id);
  return (
    <>
      <span>{event?.type}</span>
      <span>{formatDateTimeLong(event?.created_at)}</span>
      {/* Only raw JSON viewer — no ActivityTimeline */}
      <pre><code>{JSON.stringify(event, null, 2)}</code></pre>
    </>
  );
};
```

**Devtools drawer** (`packages/developers/components/developer-tools-drawer.tsx`): Has tabs for Activity, API Keys, Logs, Events, Apps, Webhooks, Playground, GraphiQL. No dedicated Tracing Records tab.

```typescript
// Current VIEW_CONFIG — no "tracing-records" entry
const VIEW_CONFIG = {
  activity: { ... },
  "api-keys": { ... },
  logs: { ... },
  events: { ... },
  apps: { ... },
  webhooks: { ... },
  playground: { ... },
  graphiql: { ... },
};
```

**Tracing records visibility**: Only accessible nested inside an API log entry's "Timeline" tab. Background carrier calls (tracking polls, webhook retries) that don't originate from a user REST API call are invisible.

### Desired State

```typescript
// Event detail WITH ActivityTimeline — matches shipment/tracker/pickup pattern
export const EventComponent = ({ eventId }: { eventId: string }) => {
  const { query: { data: { event } = {} } } = useEvent(entity_id);
  const entityId = event?.data?.id; // e.g. "shp_123", "trk_456"
  const { query: logs } = useLogs({ entity_id: entityId });
  const { query: events } = useEvents({ entity_id: entityId });
  return (
    <Tabs tabs={["Timeline", "Event Data"]}>
      <ActivityTimeline logs={logs} events={events} stacked />
      <pre><code>{JSON.stringify(event, null, 2)}</code></pre>
    </Tabs>
  );
};
```

```typescript
// Devtools VIEW_CONFIG WITH tracing records tab
const VIEW_CONFIG = {
  activity: { ... },
  "api-keys": { ... },
  logs: { ... },
  events: { ... },
  "tracing-records": {
    label: "Tracing Records",
    icon: Network,
    component: TracingRecordsView,
  },
  apps: { ... },
  webhooks: { ... },
  playground: { ... },
  graphiql: { ... },
};
```

### Problems

1. **No event timeline**: When debugging a webhook failure or investigating why a `shipment_purchased` event fired, developers must manually correlate the event's entity_id with API logs. The shipment/tracker/pickup detail pages already show full `ActivityTimeline` — events should too.
2. **Background tracing records invisible**: Carrier API calls from background tasks (tracking polls via Huey, webhook delivery retries) don't have a parent API log and are therefore invisible in the current devtools. The only way to see them is via Django admin.
3. **No unified carrier API call view**: Developers debugging carrier integration issues must click through individual API log entries to find their nested tracing records. A dedicated tab showing all carrier-level calls with filtering would dramatically improve debugging workflows.

---

## Goals & Success Criteria

### Goals

1. Show the full activity timeline (API logs + events + tracing records) on the event detail view using `entity_id` from event data
2. Add a standalone "Tracing Records" tab to devtools with list/detail views and filtering
3. Surface background carrier API calls (tracking polls, webhook deliveries) that are currently invisible

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Event detail shows associated API logs + tracing records | Timeline renders when event.data.id exists | Must-have |
| Tracing Records tab shows all records including background calls | Full list with pagination | Must-have |
| Tracing Records support filtering by carrier, date, keyword | Filter panel with apply/clear | Must-have |
| Tracing Records show request/response detail on selection | Split-panel or stacked detail view | Must-have |
| Consistent dark theme with other devtools tabs | Uses existing CSS variables | Must-have |
| Entity ID cross-linking from tracing records | Clickable entity_id navigates to entity detail | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Event detail view shows ActivityTimeline tab with associated API logs/events
- [ ] Event detail view preserves existing raw JSON "Event Data" tab
- [ ] New "Tracing Records" tab appears in devtools drawer sidebar
- [ ] Tracing Records list view with pagination and filtering
- [ ] Tracing Records detail view shows raw request/response data

**Nice-to-have (P1):**
- [ ] Tracing Records computed duration column (response_timestamp - request_timestamp)
- [ ] Entity ID clickable cross-links to shipment/tracker/pickup/order detail
- [ ] Tracing Records auto-refresh interval

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| A) Reuse `ActivityTimeline` for event detail + new tracing records tab | Maximum code reuse; proven component; consistent UX | Two separate pieces of work | **Selected** |
| B) Only add tracing records tab, skip event timeline | Simpler scope | Events remain without context; misses the quick-debug UX | Rejected |
| C) Embed tracing records inside existing Logs tab as sub-filter | No new tab needed | Overloads the logs tab; conceptual confusion between API logs and carrier traces | Rejected |
| D) Build custom event timeline component instead of reusing `ActivityTimeline` | Could tailor to event-specific needs | Violates DRY; `ActivityTimeline` already handles all activity types | Rejected |

### Trade-off Analysis

Option A was selected because:
- `ActivityTimeline` is already battle-tested on shipment, tracker, pickup, and order detail pages
- The `useLogs({ entity_id })` and `useEvents({ entity_id })` hooks are generic and work with any entity prefix
- Adding a tracing records tab fills a genuine visibility gap for background carrier calls
- Both features are independent and can be implemented in parallel phases

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `ActivityTimeline` component | `packages/ui/components/activity-timeline.tsx` | Direct reuse — renders logs + events + tracing records in chronological timeline |
| `useLogs` hook | `packages/hooks/log.ts` | Direct reuse — pass `entity_id` from event data |
| `useEvents` hook | `packages/hooks/event.ts` | Direct reuse — pass `entity_id` from event data |
| `useEvent` hook | `packages/hooks/event.ts` | Already used by event detail page |
| `EventComponent` (event detail) | `packages/developers/modules/event.tsx` | Modify to add tabbed layout with ActivityTimeline |
| `EventsView` (events list) | `packages/developers/components/views/events-view.tsx` | Reference for view styling patterns |
| `LogsView` (logs list) | `packages/developers/components/views/logs-view.tsx` | Reference for list + filter + detail pattern |
| `LogComponent` (log detail) | `packages/developers/modules/log.tsx` | Reference for tabbed detail with tracing records |
| `DeveloperToolsDrawer` | `packages/developers/components/developer-tools-drawer.tsx` | Modify VIEW_CONFIG to add tracing records tab |
| `TracingRecordType` (GraphQL) | `modules/graph/karrio/server/graph/schemas/base/types.py` | Already exposes `tracing_records` query |
| `TracingRecordFilter` | `modules/core/karrio/server/core/filters.py` | Already supports `key`, `request_log_id`, `date_after/before`, `keyword` |
| `TracingRecord` model | `modules/core/karrio/server/tracing/models.py` | Read-only — fields: `id`, `key`, `record` (JSON), `timestamp`, `meta` (JSON), `test_mode` |
| `GET_TRACING_RECORDS` query | `packages/types/graphql/queries.ts` | Already exists — needs to be verified and used by new hook |
| Devtools dark theme CSS | `packages/developers/components/developer-tools-drawer.tsx` | Scoped CSS variables (`.devtools-theme.dark`) — new views inherit automatically |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Developer Tools Drawer                      │
├───────────┬──────────────────────────────────────────────────┤
│  Sidebar  │  Content Area                                     │
│           │                                                   │
│ Activity  │  ┌──────────────────────────────────────────┐    │
│ API Keys  │  │  Events View (existing)                   │    │
│ Logs      │  │  ┌────────────────────────────┐          │    │
│ Events ◄──┼──┤  │ Event Detail (ENHANCED)    │          │    │
│ Tracing ◄─┼──┤  │ ┌──────────┬─────────────┐│          │    │
│ Records   │  │  │ │ Timeline │ Event Data  ││          │    │
│ (NEW)     │  │  │ │  (NEW)   │ (existing)  ││          │    │
│ Apps      │  │  │ └──────────┴─────────────┘│          │    │
│ Webhooks  │  │  └────────────────────────────┘          │    │
│ Playground│  │                                           │    │
│ GraphiQL  │  │  ┌──────────────────────────────────┐    │    │
│           │  │  │ Tracing Records View (NEW)        │    │    │
│           │  │  │ ┌──────────┬───────────────────┐ │    │    │
│           │  │  │ │ List +   │ Request/Response  │ │    │    │
│           │  │  │ │ Filters  │ Detail Viewer     │ │    │    │
│           │  │  │ └──────────┴───────────────────┘ │    │    │
│           │  │  └──────────────────────────────────┘    │    │
│           │  └──────────────────────────────────────────┘    │
└───────────┴──────────────────────────────────────────────────┘
```

### Sequence Diagram

#### Feature 1: Event Detail Timeline

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌────────┐
│  User  │     │EventComp │     │  Hooks   │     │GraphQL │
└───┬────┘     └────┬─────┘     └────┬─────┘     └───┬────┘
    │               │                │                │
    │ 1. Click event│                │                │
    │──────────────>│                │                │
    │               │ 2. useEvent()  │                │
    │               │───────────────>│ GET_EVENT      │
    │               │                │───────────────>│
    │               │                │  event.data.id │
    │               │                │<───────────────│
    │               │ 3. Extract     │                │
    │               │ entity_id from │                │
    │               │ event.data.id  │                │
    │               │                │                │
    │               │ 4. useLogs({   │                │
    │               │    entity_id}) │ GET_LOGS       │
    │               │───────────────>│───────────────>│
    │               │                │<───────────────│
    │               │ 5. useEvents({ │                │
    │               │    entity_id}) │ GET_EVENTS     │
    │               │───────────────>│───────────────>│
    │               │                │<───────────────│
    │               │                │                │
    │ 6. Render     │                │                │
    │ ActivityTimeline               │                │
    │<──────────────│                │                │
    │               │                │                │
```

#### Feature 2: Tracing Records Tab

```
┌────────┐     ┌──────────┐     ┌──────────────┐     ┌────────┐
│  User  │     │TracingVw │     │useTracingRecs│     │GraphQL │
└───┬────┘     └────┬─────┘     └──────┬───────┘     └───┬────┘
    │               │                   │                  │
    │ 1. Click tab  │                   │                  │
    │──────────────>│                   │                  │
    │               │ 2. useTracingRecs │                  │
    │               │──────────────────>│GET_TRACING_RECS  │
    │               │                   │─────────────────>│
    │               │                   │ records + paging │
    │               │                   │<─────────────────│
    │               │                   │                  │
    │ 3. Show list  │                   │                  │
    │<──────────────│                   │                  │
    │               │                   │                  │
    │ 4. Click      │                   │                  │
    │ record        │                   │                  │
    │──────────────>│                   │                  │
    │               │ 5. Show detail    │                  │
    │ 6. Request/   │ panel with raw    │                  │
    │ Response view │ carrier data      │                  │
    │<──────────────│                   │                  │
    │               │                   │                  │
    │ 7. Apply      │                   │                  │
    │ filter        │                   │                  │
    │──────────────>│ 8. setFilter()    │                  │
    │               │──────────────────>│ GET_TRACING_RECS │
    │               │                   │ + filter params  │
    │               │                   │─────────────────>│
    │               │                   │<─────────────────│
    │<──────────────│                   │                  │
    │               │                   │                  │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    FEATURE 1: EVENT TIMELINE                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────────────┐  │
│  │ useEvent │───>│ event.data.id │───>│ entity_id extraction │  │
│  │ (existing)│   │ "shp_abc123"  │    │ e.g. "shp_abc123"    │  │
│  └──────────┘    └───────────────┘    └──────────┬───────────┘  │
│                                                    │              │
│                                       ┌────────────┼────────┐    │
│                                       │            │        │    │
│                                       ▼            ▼        │    │
│                              ┌──────────┐  ┌──────────┐     │    │
│                              │ useLogs  │  │useEvents │     │    │
│                              │({entity_ │  │({entity_ │     │    │
│                              │  id})    │  │  id})    │     │    │
│                              └────┬─────┘  └────┬─────┘     │    │
│                                   │             │            │    │
│                                   └──────┬──────┘            │    │
│                                          ▼                   │    │
│                              ┌───────────────────┐           │    │
│                              │ ActivityTimeline  │           │    │
│                              │ (existing component)          │    │
│                              └───────────────────┘           │    │
│                                                               │    │
├──────────────────────────────────────────────────────────────────┤
│                 FEATURE 2: TRACING RECORDS TAB                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │ TracingRecords│───>│ useTracingRecords │───>│ GraphQL      │  │
│  │ View (NEW)    │    │ Hook (NEW)        │    │ tracing_     │  │
│  │               │    │                   │    │ records query│  │
│  └───────┬───────┘    └──────────────────┘    └──────────────┘  │
│          │                                                       │
│  ┌───────▼───────┐    ┌──────────────────┐                      │
│  │ List Panel    │───>│ Detail Panel     │                      │
│  │ (filterable)  │    │ (request/response│                      │
│  │               │    │  raw viewer)     │                      │
│  └───────────────┘    └──────────────────┘                      │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Models

No new backend models. Existing models used:

```python
# TracingRecord (modules/core/karrio/server/tracing/models.py)
# Fields used by the new views:
class TracingRecord(OwnedEntity):
    id = CharField(pk, default="trace_*")
    key = CharField(max_length=50)          # "request" or "response"
    record = JSONField()                     # { url, data, response, error, format, request_id }
    timestamp = FloatField()                 # Unix timestamp
    meta = JSONField()                       # { request_log_id, carrier_name, carrier_id, object_id, carrier_account_id }
    test_mode = BooleanField()
    created_at = DateTimeField(auto)

# Event (modules/events/karrio/server/events/models.py)
# Existing — data.id used for entity_id extraction:
class Event(OwnedEntity):
    id = CharField(pk, default="evt_*")
    type = CharField()                       # e.g. "shipment_purchased"
    data = JSONField()                       # { id: "shp_abc123", ... } ← entity data snapshot
    test_mode = BooleanField()
    pending_webhooks = IntegerField()
```

### New TypeScript Types

```typescript
// packages/types/graphql/types.ts — already auto-generated, verify existence:
export interface TracingRecordFilter {
  offset?: number | null;
  first?: number | null;
  key?: string | null;
  request_log_id?: number | null;
  date_after?: any | null;
  date_before?: any | null;
  keyword?: string | null;
}
```

### New Hook: `useTracingRecords`

```typescript
// packages/hooks/tracing-record.ts (NEW)
import {
  TracingRecordFilter,
  get_tracing_records,
  GET_TRACING_RECORDS,
} from "@karrio/types";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useQueryClient } from "@tanstack/react-query";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = TracingRecordFilter & {
  setVariablesToURL?: boolean;
  preloadNextPage?: boolean;
};

export function useTracingRecords({
  setVariablesToURL = false,
  preloadNextPage = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<TracingRecordFilter>({
    ...PAGINATION,
    ...initialData,
  });
  const fetch = (variables: { filter: TracingRecordFilter }) =>
    karrio.graphql.request<get_tracing_records>(
      gqlstr(GET_TRACING_RECORDS), { variables }
    );

  const query = useAuthenticatedQuery({
    queryKey: ["tracing_records", filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: TracingRecordFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      return isNoneOrEmpty(options[key as keyof TracingRecordFilter])
        ? acc
        : {
          ...acc,
          [key]: ["offset", "first"].includes(key)
            ? parseInt(options[key as keyof TracingRecordFilter] as string)
            : options[key as keyof TracingRecordFilter],
        };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);
    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.tracing_records.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + PAGE_SIZE };
      queryClient.prefetchQuery(["tracing_records", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}
```

### Modified Components

#### 1. Enhanced Event Detail (`packages/developers/modules/event.tsx`)

Add tabbed layout with ActivityTimeline + raw JSON:

```typescript
// Key changes to EventComponent:
import { useLogs } from "@karrio/hooks/log";
import { useEvents } from "@karrio/hooks/event";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";

export const EventComponent = ({ eventId, isPreview }: { ... }) => {
  const { query: { data: { event } = {} } } = useEvent(entity_id);

  // Extract entity_id from event data for timeline
  const entityId = event?.data?.id as string | undefined;
  const { query: logs } = useLogs({ entity_id: entityId });
  const { query: events } = useEvents({ entity_id: entityId });

  return (
    <>
      {/* Header: type + date + copy (existing) */}
      <TabStateProvider tabs={["Timeline", "Event Data"]}>
        <Tabs>
          {/* Tab 1: ActivityTimeline (NEW) */}
          <div>
            {entityId ? (
              <ActivityTimeline logs={logs} events={events} stacked />
            ) : (
              <div>No associated entity activity</div>
            )}
          </div>
          {/* Tab 2: Raw JSON (existing, moved into tab) */}
          <div>
            <pre><code>{JSON.stringify(event, null, 2)}</code></pre>
          </div>
        </Tabs>
      </TabStateProvider>
    </>
  );
};
```

#### 2. New Tracing Records View (`packages/developers/components/views/tracing-records-view.tsx`)

Follow the pattern of `logs-view.tsx` — split-panel list + detail with filter sidebar:

```typescript
// Skeleton structure — follows LogsView pattern
export function TracingRecordsView() {
  const { query, filter, setFilter } = useTracingRecords({ setVariablesToURL: false });
  const [selectedRecord, setSelectedRecord] = useState<TracingRecordType | null>(null);

  return (
    <div className="h-full flex flex-col">
      {/* Header with filter toggle */}
      {/* Filter panel: key, date_after, date_before, keyword */}
      {/* Split panel: list (left) + detail (right) */}
      <div className="flex flex-1">
        {/* Left: record list with carrier, URL, timestamp, test_mode badge */}
        {/* Right: raw request/response viewer using CodeMirror */}
      </div>
      {/* Pagination */}
    </div>
  );
}
```

#### 3. Updated Drawer Config (`packages/developers/components/developer-tools-drawer.tsx`)

```typescript
import { TracingRecordsView } from "@karrio/developers/components/views/tracing-records-view";
import { Network } from "lucide-react"; // or Globe, Workflow

const VIEW_CONFIG = {
  activity: { label: "Activity", icon: Activity, component: ActivityView },
  "api-keys": { label: "API Keys", icon: Key, component: ApiKeysView },
  logs: { label: "Logs", icon: FileText, component: LogsView },
  events: { label: "Events", icon: Calendar, component: EventsView },
  "tracing-records": {
    label: "Tracing Records",
    icon: Network,
    component: TracingRecordsView,
  },
  apps: { label: "Apps", icon: Settings, component: AppsView },
  webhooks: { label: "Webhooks", icon: Webhook, component: WebhooksView },
  playground: { label: "Playground", icon: Code2, component: PlaygroundView },
  graphiql: { label: "GraphiQL", icon: Database, component: GraphiQLView },
};
```

#### 4. Updated DeveloperView Type (`packages/developers/context/developer-tools-context.tsx`)

```typescript
export type DeveloperView =
  | "activity"
  | "api-keys"
  | "logs"
  | "events"
  | "tracing-records"   // NEW
  | "apps"
  | "webhooks"
  | "playground"
  | "graphiql";
```

### Field Reference

#### Tracing Record List Columns

| Field | Source | Description |
|-------|--------|-------------|
| Carrier | `meta.carrier_name` | Carrier integration name (e.g., "fedex", "ups") |
| Connection | `meta.carrier_id` | Carrier connection ID |
| Key | `key` | "request" or "response" |
| URL | `record.url` | Carrier API endpoint URL |
| Timestamp | `timestamp` | Unix timestamp → formatted datetime |
| Test Mode | `test_mode` | Badge indicator |
| Request ID | `record.request_id` | UUID grouping request/response pairs |

#### Tracing Record Filter Fields

| Filter | GraphQL Field | Description |
|--------|---------------|-------------|
| Key | `key` | Filter by "request" or "response" |
| Date After | `date_after` | Start date range |
| Date Before | `date_before` | End date range |
| Keyword | `keyword` | Search in key and meta fields |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Event data has no `id` field (e.g., batch events) | Timeline tab shows empty state message | Check `event?.data?.id` before calling `useLogs`/`useEvents`; show "No associated entity activity" |
| Event entity_id references deleted shipment/tracker | Timeline shows logs/events that existed before deletion | Logs/events are independent records — they persist after entity deletion |
| Tracing record with empty `record` JSON | Detail viewer shows empty state | `RawContentViewer` already handles null/empty content gracefully |
| Tracing record without `meta.carrier_name` | List item shows "Unknown" carrier | Fallback to "Unknown" or hide carrier column for that row |
| Very large tracing record payload (>1MB base64 label) | Slow rendering in CodeMirror | Truncate display to first 100KB with "Show full content" toggle |
| User navigates to event detail before event data loads | Entity_id is undefined, hooks don't fire | `useLogs`/`useEvents` hooks skip fetch when `entity_id` is falsy |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| `GET_TRACING_RECORDS` returns error | Tracing Records tab shows error state | Use `onError` handler from `@karrio/lib`; show retry button |
| GraphQL schema doesn't have `tracing_records` query | Hook fails to fetch | Verify query exists in schema before shipping; graceful fallback |
| Tracing records volume is very high (10K+ per day) | Slow list rendering | Pagination (20 per page); date range filter defaults to last 24h |

### Security Considerations

- [ ] Tracing records filtered by org context (existing `ControlledAccessModel` handles this)
- [ ] System connection tracing records excluded for non-staff users (existing resolver logic)
- [ ] No secrets exposed in tracing record display (carrier credentials stripped by Tracer)
- [ ] Event data does not expose sensitive fields beyond what the user already has access to

---

## Implementation Plan

### Phase 1: Event Detail Timeline Enhancement

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Verify `GET_TRACING_RECORDS` query exists in `queries.ts` | `packages/types/graphql/queries.ts` | Pending | S |
| Add `ActivityTimeline` + tabbed layout to `EventComponent` | `packages/developers/modules/event.tsx` | Pending | M |
| Update `EventsView` event detail panel to show timeline when event selected | `packages/developers/components/views/events-view.tsx` | Pending | M |
| Test event detail timeline with different event types (shipment, tracker, order, pickup) | Manual testing | Pending | S |

### Phase 2: Tracing Records Devtools Tab

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `useTracingRecords` hook | `packages/hooks/tracing-record.ts` | Pending | M |
| Create `TracingRecordsView` component | `packages/developers/components/views/tracing-records-view.tsx` | Pending | L |
| Add "Tracing Records" to `VIEW_CONFIG` in drawer | `packages/developers/components/developer-tools-drawer.tsx` | Pending | S |
| Update `DeveloperView` type union | `packages/developers/context/developer-tools-context.tsx` | Pending | S |
| Add filter panel (key, date range, keyword) | `packages/developers/components/views/tracing-records-view.tsx` | Pending | M |
| Add request/response detail viewer panel | `packages/developers/components/views/tracing-records-view.tsx` | Pending | M |
| Add pagination | `packages/developers/components/views/tracing-records-view.tsx` | Pending | S |
| Export new hook from hooks package | `packages/hooks/index.ts` | Pending | S |

**Dependencies:** Phase 1 and Phase 2 are independent and can be implemented in parallel.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly as the original authors.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Manual UI Tests | Dashboard devtools | All new views render correctly |
| Hook Tests | `packages/hooks/` | `useTracingRecords` hook functions |
| Component Tests | `packages/developers/` | Event detail with timeline renders |

### Test Cases

#### Manual Test: Event Detail Timeline

1. Navigate to Devtools → Events
2. Click on a `shipment_purchased` event
3. Verify "Timeline" tab is shown and selected by default
4. Verify ActivityTimeline renders associated API logs and tracing records for that shipment
5. Click "Event Data" tab — verify raw JSON is still displayed
6. Click on a `batch_completed` event (no entity_id) — verify "No associated entity activity" message

#### Manual Test: Tracing Records Tab

1. Navigate to Devtools → Tracing Records
2. Verify list of tracing records is displayed with pagination
3. Click a record — verify split-panel detail shows request/response data
4. Apply keyword filter — verify list updates
5. Apply date range filter — verify list updates
6. Clear filters — verify full list returns
7. Verify background carrier calls (no parent API log) are visible

#### Django Test: Verify Tracing Records GraphQL Query

```python
"""Verify tracing_records query returns filtered results."""

import unittest
from unittest.mock import patch, ANY

class TestTracingRecordsQuery(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_tracing_records_query_with_keyword_filter(self):
        """Verify tracing_records query supports keyword filtering."""
        # This test verifies the existing GraphQL resolver
        # handles the filter correctly
        response = self.client.post('/graphql', data={
            'query': '''
                query {
                    tracing_records(filter: { keyword: "fedex" }) {
                        page_info { count has_next_page }
                        edges { node { id key meta record timestamp } }
                    }
                }
            '''
        })
        # print(response)
        self.assertResponseNoErrors(response)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run server tests for tracing module
karrio test --failfast karrio.server.tracing.tests

# Manual testing
npm run dev -w @karrio/dashboard
# Navigate to localhost:3002 → Developer Tools
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| `GET_TRACING_RECORDS` query not available in schema | High | Low | Verify query exists before implementation; it's registered in `base/__init__.py` lines 69-74 |
| ActivityTimeline performance with many tracing records | Medium | Medium | Existing pagination + condensed mode; limit initial fetch to 20 items |
| Event data.id field format varies across event types | Medium | Low | Extract entity_id with null-safe access; handle missing gracefully |
| Dark theme inconsistency in new views | Low | Low | Use existing shadcn/ui components with scoped `.devtools-theme.dark` CSS |
| Breaking existing devtools layout with new tab | Medium | Low | New tab is additive; no existing tabs modified |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No backend changes — all GraphQL queries and filters already exist
- **Data compatibility**: No database migrations — existing `TracingRecord` and `Event` models unchanged
- **Feature flags**: Not needed — changes are purely additive frontend enhancements
- **Existing functionality**: Event detail raw JSON view preserved as second tab; all existing devtools tabs unchanged

### Rollback Procedure

1. **Identify issue**: Devtools drawer crashes or tracing records tab fails to load
2. **Stop rollout**: Revert the frontend commit (single PR expected)
3. **Revert changes**: `git revert <commit-sha>` — all changes are in `packages/developers/`, `packages/hooks/`, and `packages/ui/`
4. **Verify recovery**: Confirm devtools drawer loads with original tab set; confirm event detail shows raw JSON without timeline

---

## Appendices

### Appendix A: Files to Create

| File | Description |
|------|-------------|
| `packages/hooks/tracing-record.ts` | `useTracingRecords` hook |
| `packages/developers/components/views/tracing-records-view.tsx` | Tracing Records tab view component |

### Appendix B: Files to Modify

| File | Change |
|------|--------|
| `packages/developers/modules/event.tsx` | Add tabbed layout with ActivityTimeline |
| `packages/developers/components/views/events-view.tsx` | Update event detail panel to show timeline |
| `packages/developers/components/developer-tools-drawer.tsx` | Add "tracing-records" to VIEW_CONFIG |
| `packages/developers/context/developer-tools-context.tsx` | Add "tracing-records" to DeveloperView type |
| `packages/hooks/index.ts` | Export `useTracingRecords` hook |

### Appendix C: Existing GraphQL Queries Reference

```graphql
# Already exists in packages/types/graphql/queries.ts
query get_tracing_records($filter: TracingRecordFilter) {
  tracing_records(filter: $filter) {
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
        key
        timestamp
        test_mode
        created_at
        meta
        record
      }
    }
  }
}

# Event query — data.id used for entity_id extraction
query get_event($id: String!) {
  event(id: $id) {
    id
    type
    data           # ← data.id contains entity_id (e.g., "shp_abc123")
    test_mode
    pending_webhooks
    created_at
  }
}
```

### Appendix D: Component Reuse Map

```
Existing Components Used:
─────────────────────────
ActivityTimeline        ← packages/ui/components/activity-timeline.tsx
  └─ Used by: shipment.tsx, tracker.tsx, pickup.tsx, order.tsx
  └─ NEW: event.tsx (event detail timeline)

RawContentViewer        ← (inside activity-timeline.tsx)
  └─ Handles: JSON, XML, form-data, URL-encoded content
  └─ Reused by: tracing-records-view.tsx (detail panel)

CodeMirror              ← @uiw/react-codemirror
  └─ Used by: events-view.tsx, activity-timeline.tsx
  └─ Reused by: tracing-records-view.tsx

useLogs({entity_id})    ← packages/hooks/log.ts
  └─ Used by: shipment.tsx, tracker.tsx, pickup.tsx, order.tsx
  └─ NEW: event.tsx (with entity_id from event.data.id)

useEvents({entity_id})  ← packages/hooks/event.ts
  └─ Used by: shipment.tsx, tracker.tsx, pickup.tsx, order.tsx
  └─ NEW: event.tsx (with entity_id from event.data.id)
```
