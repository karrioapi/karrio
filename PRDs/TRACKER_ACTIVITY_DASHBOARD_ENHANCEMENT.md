# Tracker Activity Dashboard Enhancement

<!--
PRD TYPE: ENHANCEMENT
SCOPE: Dashboard tracker detail page augmentation with events, API logs, and tracing records
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-03 |
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

This PRD proposes augmenting the tracker dashboard detail view with system events, API logs, and tracing records — the same observability features already available on shipment and pickup detail pages. The existing backend infrastructure (`GET_LOGS`, `GET_EVENTS`, `entity_id` filtering, `ActivityTimeline` component) is fully reusable; the work is primarily frontend integration into the tracker preview sheet and a new authenticated tracker detail page.

### Key Architecture Decisions

1. **Reuse existing hooks and components**: `useLogs`, `useEvents`, and `ActivityTimeline` already work with any `entity_id` — no backend changes required for log/event filtering.
2. **New authenticated tracker detail page**: Create a `/trackers/[id]` dashboard page (client-rendered, authenticated) alongside the existing public `/tracking/[id]` server-rendered page. The detail page shows the full management view with activity timeline.
3. **Augment tracker preview sheet**: Add `ActivityTimeline` to the existing `tracking-preview-sheet.tsx` so users get a quick view of API logs and events without leaving the list page.
4. **No GraphQL schema changes**: The `GET_TRACKER` query already returns tracker data; logs and events are fetched via their own existing queries filtered by `entity_id`.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| New authenticated tracker detail page (`/trackers/[id]`) | Changes to public tracking page (`/tracking/[id]`) |
| ActivityTimeline integration in tracker detail | New GraphQL mutations for trackers |
| ActivityTimeline integration in tracker preview sheet | Backend TracingRecord model changes |
| `useLogs` and `useEvents` hook integration for trackers | Changes to log/event GraphQL queries or filters |
| Tracker detail sidebar (metadata, carrier info, shipment link) | Tracker list page redesign |
| Navigation from tracker list to detail page | Mobile app changes |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Where to render ActivityTimeline for trackers | Both preview sheet and new detail page | Matches shipment/pickup pattern where both quick-preview and full-detail views show activity | 2026-02-03 |
| D2 | Backend changes needed for log/event filtering | None | `entity_id` filter in `LogFilter` and `EventFilter` is generic — already works for tracker IDs (`trk_*`) | 2026-02-03 |
| D3 | Public tracking page modification | No changes | Public page is server-rendered and unauthenticated — logs/events require authentication, so they belong on the dashboard detail page only | 2026-02-03 |
| D4 | New GraphQL queries needed | No | Logs and events are fetched via existing `GET_LOGS` and `GET_EVENTS` queries with `entity_id` filter — same as shipments/pickups | 2026-02-03 |
| D5 | Preview sheet ActivityTimeline display mode | Condensed (last 5 items with "View all" link) | Preview sheet has limited height; full timeline would be too long and degrade the quick-preview UX | 2026-02-03 |
| D6 | Carrier tracking events vs system activity layout | Unified timeline | Mixing carrier events, API logs, tracing records, and system events into a single chronological timeline provides a complete, contextual view of tracker lifecycle without requiring users to cross-reference separate sections | 2026-02-03 |

### Pending Questions

_All questions resolved._

---

## Problem Statement

### Current State

The tracker detail view only shows carrier-provided tracking events. There is no visibility into API logs, system events, or tracing records for tracker operations:

```typescript
// Current: tracking-preview-sheet.tsx — only shows carrier tracking events
// No API logs, no system events, no tracing records

export function TrackingPreviewSheet({ trackerId }) {
  const { query: { data: { tracker } } } = useTracker(trackerId);

  return (
    <Sheet>
      {/* Carrier tracking events timeline */}
      {tracker.events.map((event) => (
        <TimelineItem key={event.date}>
          {event.description} — {event.location}
        </TimelineItem>
      ))}
      {/* No ActivityTimeline — no API logs, no system events */}
    </Sheet>
  );
}
```

```typescript
// Current: No authenticated tracker detail page exists
// /trackers page only has the list view
// /tracking/[id] is a public, unauthenticated page with no logs/events

// apps/dashboard/src/app/(base)/(dashboard)/trackers/page.tsx — list only
export { default } from "@karrio/core/modules/Trackers";

// apps/dashboard/src/app/(base)/tracking/[id]/page.tsx — public, no logs
export { default } from "@karrio/core/modules/Trackers/tracking-page";
```

### Desired State

```typescript
// Desired: New authenticated tracker detail page with full activity timeline
// packages/core/modules/Trackers/tracker.tsx

import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import { useTracker } from "@karrio/hooks/tracker";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";

export function TrackerComponent({ trackerId }) {
  const entity_id = trackerId;
  const { query: { data: { tracker } } } = useTracker(entity_id);
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });

  return (
    <>
      {/* Tracker details header, sidebar, carrier events */}
      {/* ... */}

      {/* Activity section — API logs, tracing records, system events */}
      <h2 className="text-xl font-semibold my-4">Activity</h2>
      <ActivityTimeline logs={logs} events={events} />
    </>
  );
}
```

```typescript
// Desired: Augmented preview sheet with ActivityTimeline
// packages/ui/components/tracking-preview-sheet.tsx

import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";

export function TrackingPreviewSheet({ trackerId }) {
  const entity_id = trackerId;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });

  return (
    <Sheet>
      {/* Existing carrier tracking events */}
      {/* ... */}

      {/* NEW: Activity timeline with API logs and system events */}
      <h2 className="text-lg font-semibold my-4">Activity</h2>
      <ActivityTimeline logs={logs} events={events} />
    </Sheet>
  );
}
```

### Problems

1. **No API log visibility for trackers**: When a tracker update fails or behaves unexpectedly, users cannot inspect the carrier API request/response payloads from the tracker detail view — they must navigate to the global logs page and manually search for the tracker ID.
2. **No system event visibility for trackers**: Tracker lifecycle events (`tracker_created`, `tracker_updated`) exist in the events system but are not displayed on the tracker detail page.
3. **No tracing record visibility for trackers**: Carrier API request/response pairs (tracing records) generated during tracker operations are not surfaced on the tracker detail view.
4. **Inconsistent UX across entity types**: Shipments and pickups both show ActivityTimeline with API logs, tracing records, and system events — trackers do not, creating a fragmented debugging experience.
5. **No dedicated authenticated tracker detail page**: The only detail view is either the public `/tracking/[id]` page (no auth, no logs) or the preview sheet (limited space, no logs).

---

## Goals & Success Criteria

### Goals

1. Add `ActivityTimeline` component with API logs, tracing records, and system events to the tracker preview sheet.
2. Create a new authenticated tracker detail page at `/trackers/[id]` following the shipment detail page pattern.
3. Achieve UX parity with shipments and pickups for tracker observability.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| ActivityTimeline renders on tracker detail page | Displays logs, traces, events filtered by tracker ID | Must-have |
| ActivityTimeline renders on tracker preview sheet | Displays logs, traces, events in scrollable view | Must-have |
| Tracker detail page loads | < 1s initial load | Must-have |
| No backend changes required | Zero new API endpoints, zero schema migrations | Must-have |
| Consistent with shipment/pickup patterns | Same component usage, same hook patterns | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] New authenticated tracker detail page (`/trackers/[id]`) with full layout
- [ ] ActivityTimeline integrated in tracker detail page with logs and events
- [ ] ActivityTimeline integrated in tracker preview sheet
- [ ] Navigation from tracker list to detail page (click row or "View details")
- [ ] Tracker detail sidebar with metadata, carrier info, and shipment link

**Nice-to-have (P1):**
- [ ] "View details" link in preview sheet header to navigate to full detail page
- [ ] Metadata editing on tracker detail page (matching shipment pattern)
- [ ] Breadcrumb navigation on detail page

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Reuse existing hooks + ActivityTimeline (no backend changes) | Zero backend work; proven pattern; fast delivery | Relies on `entity_id` filtering already working for tracker IDs | **Selected** |
| Add dedicated tracker log/event GraphQL fields to TrackerType | Strongly typed; single query | Duplicates existing log/event queries; requires backend schema changes; breaks pattern consistency | Rejected |
| Embed logs in the public tracking page | More visibility | Security risk (exposes API logs to unauthenticated users); server component incompatible with client hooks | Rejected |
| Only update preview sheet (skip dedicated detail page) | Less work | Preview sheet has limited space; no deep-dive capability; inconsistent with shipment/pickup having dedicated detail pages | Rejected |

### Trade-off Analysis

The selected approach (reuse existing hooks + ActivityTimeline) provides:
- **Zero backend risk**: No schema changes, no new resolvers, no migrations
- **Proven reliability**: The same `useLogs({ entity_id })` and `useEvents({ entity_id })` pattern works for shipments and pickups
- **Consistency**: Identical component usage across all entity detail views
- **Fast delivery**: Frontend-only changes with existing, tested infrastructure

---

## Technical Design

> **IMPORTANT**: This design reuses existing backend infrastructure entirely. All changes are frontend-only.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `useLogs` hook | `packages/hooks/log.ts` | Direct reuse — pass `entity_id` for tracker ID |
| `useEvents` hook | `packages/hooks/event.ts` | Direct reuse — pass `entity_id` for tracker ID |
| `useTracker` hook | `packages/hooks/tracker.ts` | Already exists — used in preview sheet |
| `ActivityTimeline` component | `packages/ui/components/activity-timeline.tsx` | Direct reuse — same `logs`/`events` props |
| Shipment detail page | `packages/core/modules/Shipments/shipment.tsx` | Reference pattern for tracker detail page layout |
| Pickup detail page | `packages/core/modules/Pickups/pickup.tsx` | Reference pattern for tracker detail page layout |
| Tracker preview sheet | `packages/ui/components/tracking-preview-sheet.tsx` | Augment with `useLogs`, `useEvents`, `ActivityTimeline` |
| Tracker list page | `packages/core/modules/Trackers/index.tsx` | Add navigation to detail page |
| `GET_TRACKER` query | `packages/types/graphql/queries.ts:1145-1225` | Already exists — no changes needed |
| `GET_LOGS` query | `packages/types/graphql/queries.ts:154-217` | Already exists — filter by `entity_id` |
| `GET_EVENTS` query | `packages/types/graphql/queries.ts:1768-1803` | Already exists — filter by `entity_id` |
| `LogFilter.entity_id` | `packages/types/graphql/types.ts` | Already supports filtering by any entity ID |
| `EventFilter.entity_id` | `packages/types/graphql/types.ts` | Already supports filtering by any entity ID |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    TRACKER ACTIVITY DASHBOARD SYSTEM                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────┐                                                          │
│  │  Tracker List   │─── Click row ──────────────┐                             │
│  │  /trackers      │                             │                             │
│  │  (index.tsx)    │─── Preview button ──┐       │                             │
│  └─────────────────┘                     │       │                             │
│                                          ▼       ▼                             │
│  ┌────────────────────┐    ┌─────────────────────────┐                         │
│  │  Preview Sheet     │    │  Tracker Detail Page     │                         │
│  │  (tracking-preview │    │  /trackers/[id]          │                         │
│  │   -sheet.tsx)      │    │  (tracker.tsx)           │                         │
│  │                    │    │                           │                         │
│  │  ┌──────────────┐  │    │  ┌───────────────────┐   │                         │
│  │  │ useTracker() │  │    │  │ useTracker()      │   │                         │
│  │  │ useLogs()  * │  │    │  │ useLogs()         │   │                         │
│  │  │ useEvents()* │  │    │  │ useEvents()       │   │                         │
│  │  └──────────────┘  │    │  └───────────────────┘   │                         │
│  │                    │    │                           │                         │
│  │  ┌──────────────┐  │    │  ┌───────────────────┐   │                         │
│  │  │ Carrier      │  │    │  │ Unified Timeline  │   │                         │
│  │  │ Events       │  │    │  │ (carrier events + │   │                         │
│  │  │ Timeline     │  │    │  │  API logs + traces │   │                         │
│  │  ├──────────────┤  │    │  │  + system events)  │   │                         │
│  │  │ Activity   * │  │    │  ├───────────────────┤   │                         │
│  │  │ Timeline   * │  │    │  │ Details Sidebar   │   │                         │
│  │  │ (condensed)* │  │    │  │ (ID, Carrier,     │   │                         │
│  │  │ + View all * │  │    │  │  Status, Metadata)│   │                         │
│  │  └──────────────┘  │    │  │                   │   │                         │
│  └────────────────────┘    │  └───────────────────┘   │                         │
│                             │  └───────────────────┘   │                         │
│  * = New additions          └─────────────────────────┘                         │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                         EXISTING BACKEND (NO CHANGES)                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                  │
│  │  GET_TRACKER  │     │   GET_LOGS   │     │  GET_EVENTS  │                  │
│  │  GraphQL      │     │   GraphQL    │     │   GraphQL    │                  │
│  │  Query        │     │   Query      │     │   Query      │                  │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘                  │
│         │                    │                     │                           │
│         │                    │ entity_id=          │ entity_id=                │
│         │                    │ "trk_..."           │ "trk_..."                 │
│         ▼                    ▼                     ▼                           │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                  │
│  │ Tracker Model│     │  Log Model   │     │ Event Model  │                  │
│  │ (manager)    │     │  (tracing)   │     │ (events)     │                  │
│  └──────────────┘     └──────────────┘     └──────────────┘                  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │ Tracker  │     │useTracker│     │ useLogs  │     │useEvents │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                 │                 │
    │ 1. Navigate   │                │                 │                 │
    │  /trackers/id │                │                 │                 │
    │──────────────>│                │                 │                 │
    │               │                │                 │                 │
    │               │ 2. Mount       │                 │                 │
    │               │   component    │                 │                 │
    │               │    ┌───────────┼─────────────────┼─────────────────┤
    │               │    │ Parallel   │                 │                 │
    │               │    │ queries    │                 │                 │
    │               │    │           │                 │                 │
    │               │    │ GET_TRACKER│                 │                 │
    │               │    │──────────>│                 │                 │
    │               │    │           │                 │                 │
    │               │    │ GET_LOGS(entity_id)          │                 │
    │               │    │────────────────────────────>│                 │
    │               │    │           │                 │                 │
    │               │    │ GET_EVENTS(entity_id)        │                 │
    │               │    │──────────────────────────────────────────────>│
    │               │    │           │                 │                 │
    │               │    │ 3. tracker │                 │                 │
    │               │    │<──────────│                 │                 │
    │               │    │           │                 │                 │
    │               │    │ 4. logs    │                 │                 │
    │               │    │<────────────────────────────│                 │
    │               │    │           │                 │                 │
    │               │    │ 5. events  │                 │                 │
    │               │    │<──────────────────────────────────────────────│
    │               │    └───────────┤                 │                 │
    │               │                │                 │                 │
    │ 6. Render     │                │                 │                 │
    │  - Details    │                │                 │                 │
    │  - Events     │                │                 │                 │
    │  - Activity   │                │                 │                 │
    │<──────────────│                │                 │                 │
    │               │                │                 │                 │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         TRACKER DETAIL DATA FLOW                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                    │
│  │  URL Param   │───>│  useTracker   │───>│  GET_TRACKER │                    │
│  │  [id]        │    │  (id)         │    │  GraphQL     │                    │
│  └──────────────┘    └──────────────┘    └──────┬───────┘                    │
│         │                                        │                            │
│         │            ┌──────────────┐            ▼                            │
│         │            │  useLogs     │    ┌──────────────┐                    │
│         ├───────────>│  (entity_id) │───>│  GET_LOGS    │                    │
│         │            └──────────────┘    │  + records[] │                    │
│         │                                └──────┬───────┘                    │
│         │            ┌──────────────┐           │                            │
│         │            │  useEvents   │           │                            │
│         └───────────>│  (entity_id) │───>┌──────┴───────┐                    │
│                      └──────────────┘    │  GET_EVENTS  │                    │
│                                          └──────┬───────┘                    │
│                                                  │                            │
│                                                  ▼                            │
│  ┌───────────────────────────────────────────────────────────────────┐        │
│  │                     ActivityTimeline                               │        │
│  │                                                                    │        │
│  │  logs ──> Process each log:                                        │        │
│  │           ├── No records ──> api-call activity                     │        │
│  │           └── Has records ──> Group by request_id                  │        │
│  │                               └── trace-call activity              │        │
│  │                                   (request/response pairs)         │        │
│  │                                                                    │        │
│  │  events ──> event activity (tracker_created, tracker_updated)      │        │
│  │                                                                    │        │
│  │  Combined ──> Sort by timestamp (desc) ──> Render timeline         │        │
│  └───────────────────────────────────────────────────────────────────┘        │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────┐        │
│  │                     Tracker Detail Page (Unified Timeline)         │        │
│  │                                                                    │        │
│  │  tracker ──> Header (tracking number, status, carrier)             │        │
│  │          ──> Sidebar (ID, carrier, status, metadata, shipment)     │        │
│  │                                                                    │        │
│  │  Unified ActivityTimeline ──> All activities in one chronological  │        │
│  │    - Carrier tracking events (from tracker.events)                 │        │
│  │    - API logs (request/response to Karrio API)                     │        │
│  │    - Trace calls (carrier API request/response pairs)              │        │
│  │    - System events (tracker_created, tracker_updated)              │        │
│  └───────────────────────────────────────────────────────────────────┘        │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Component Structure: Tracker Detail Page

```typescript
// packages/core/modules/Trackers/tracker.tsx (NEW FILE)
// Follows the exact pattern from shipment.tsx and pickup.tsx
// Uses UNIFIED timeline (D6) — carrier events + API logs + traces + system events

"use client";

import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import { useTracker } from "@karrio/hooks/tracker";
import { ActivityTimeline } from "@karrio/ui/components/activity-timeline";
import { StatusBadge, CarrierImage, Spinner } from "@karrio/ui";
import { formatDate, formatDateTime, isNone } from "@karrio/lib";
import { useSearchParams } from "next/navigation";

export default function TrackerComponent({
  trackerId,
}: {
  trackerId: string;
}) {
  const entity_id = trackerId;
  const {
    query: {
      data: { tracker } = {},
      ...query
    },
  } = useTracker(entity_id);
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });

  if (query.isLoading) return <Spinner />;
  if (isNone(tracker)) return <p>Tracker not found</p>;

  return (
    <>
      {/* Header: tracking number, status badge, carrier image */}
      {/* Main content: grid layout lg:grid-cols-4 */}
      {/*   Left column (lg:col-span-3): */}
      {/*     - Shipment link (if tracker.shipment exists) */}
      {/*     - Messages/errors */}
      {/*   Right sidebar (lg:col-span-1): */}
      {/*     - Details: ID, Carrier, Status, Tracking Number */}
      {/*     - Estimated Delivery */}
      {/*     - Info fields (customer_name, order_id, etc.) */}
      {/*     - Metadata */}

      {/* Unified Activity section (D6) — single chronological timeline */}
      {/* Carrier tracking events are mixed into the timeline alongside */}
      {/* API logs, tracing records, and system events */}
      <h2 className="text-xl font-semibold my-4">Activity</h2>
      <ActivityTimeline
        logs={logs}
        events={events}
        trackerEvents={tracker?.events}  // Carrier events merged into timeline
      />
    </>
  );
}
```

> **Note on unified timeline (D6)**: The `ActivityTimeline` component will need a
> new optional `trackerEvents` prop to accept carrier tracking events and merge
> them chronologically with API logs, traces, and system events. Each carrier
> event renders as a distinct activity type (e.g., `tracking-event`) alongside
> the existing `api-call`, `trace-call`, and `event` types. If extending
> `ActivityTimeline` is too invasive, an alternative is to transform
> `tracker.events` into the existing `event` activity format before passing them
> as part of the `events` prop.

### Component Structure: Augmented Preview Sheet (Condensed — D5)

```typescript
// packages/ui/components/tracking-preview-sheet.tsx (MODIFY)
// Add useLogs, useEvents, and condensed ActivityTimeline
// Condensed mode (D5): show last 5 activity items + "View all" link

// NEW imports to add:
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import { ActivityTimeline } from "./activity-timeline";
import Link from "next/link";

// Inside the component, add after existing hooks:
const entity_id = tracker?.id;
const { query: logs } = useLogs({ entity_id, first: 5 });
const { query: events } = useEvents({ entity_id, first: 5 });

// Add condensed ActivityTimeline section after existing tracking events:
// <div className="mt-4">
//   <div className="flex items-center justify-between mb-2">
//     <h2 className="text-lg font-semibold">Activity</h2>
//     <Link href={`/trackers/${tracker.id}`}
//       className="text-sm text-blue-500 hover:underline">
//       View all
//     </Link>
//   </div>
//   <ActivityTimeline logs={logs} events={events} condensed />
// </div>
```

> **Note on condensed mode (D5)**: The preview sheet fetches only the last 5
> log/event items (`first: 5`) and renders the `ActivityTimeline` in a condensed
> layout. A "View all" link navigates to the full `/trackers/[id]` detail page
> where the complete timeline is available. The `condensed` prop (new optional
> boolean) limits the timeline height and hides the split-panel content viewer,
> showing only the timeline list. If adding a `condensed` prop to
> `ActivityTimeline` is too invasive, the alternative is to simply limit the
> query to 5 items and constrain the container with `max-h-64 overflow-y-auto`.

### Dashboard Route

```typescript
// apps/dashboard/src/app/(base)/(dashboard)/trackers/[id]/page.tsx (NEW FILE)
import { dynamicMetadata } from "@karrio/core/components/metadata";
export { default } from "@karrio/core/modules/Trackers/tracker";
export const generateMetadata = dynamicMetadata("Tracker");
```

### Field Reference

No new fields are introduced. The enhancement reuses existing fields from these queries:

**From GET_TRACKER (existing):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tracker ID (`trk_*`) — used as `entity_id` |
| `tracking_number` | string | Carrier tracking number |
| `status` | string | Current tracking status |
| `carrier_name` | string | Carrier name |
| `events[]` | array | Carrier-provided tracking events |
| `shipment` | object | Related shipment (if any) |

**From GET_LOGS (existing, filtered by entity_id):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Log entry ID |
| `path` | string | API endpoint path |
| `method` | string | HTTP method |
| `status_code` | number | HTTP response status |
| `response_ms` | number | Response time in ms |
| `data` | JSON | Request payload |
| `response` | JSON | Response payload |
| `records[]` | array | Tracing records (carrier API request/response pairs) |

**From GET_EVENTS (existing, filtered by entity_id):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Event ID |
| `type` | EventTypes | Event type (`tracker_created`, `tracker_updated`) |
| `data` | JSON | Event payload |
| `pending_webhooks` | number | Pending webhook deliveries |
| `created_at` | datetime | Event timestamp |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Tracker with no API logs | ActivityTimeline shows "No activity" or empty state | ActivityTimeline already handles empty logs gracefully |
| Tracker with no system events | Events section of timeline is empty | ActivityTimeline already handles empty events gracefully |
| Tracker created via webhook (no direct API call) | Fewer log entries than manually created trackers | Expected — timeline shows whatever logs exist |
| Tracker with hundreds of log entries | Timeline paginates | `useLogs` uses PAGE_SIZE=20 with pagination |
| Tracker ID not found | 404 or empty page | `useTracker` returns null; show "Tracker not found" |
| User navigates to detail page while tracker is being updated | Stale data briefly shown | React Query stale time (5s) handles refresh |
| Preview sheet opened for tracker without entity_id yet | Hooks disabled until entity_id is set | `useLogs`/`useEvents` won't fire with falsy entity_id |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| `useLogs` query fails | Activity section shows error/empty | Error handled by `onError` callback in hook; rest of page still renders |
| `useEvents` query fails | Events missing from timeline | Error handled by `onError` callback; logs still display |
| `useTracker` query fails | Entire page fails to load | Show error state with retry option |
| Slow log query (many records) | Activity section loads slowly | Independent query — rest of page renders immediately; pagination limits response size |
| `entity_id` filter returns logs from wrong entity | Data leakage | Not possible — `entity_id` is an exact match filter on the backend |

### Security Considerations

- [x] No new API endpoints — reuses existing authenticated queries
- [x] Logs and events require authentication — not exposed on public tracking page
- [x] System connection tracing records hidden from non-staff users (existing `LogType.records()` pattern)
- [x] No new data exposed — same data already available via global logs/events pages
- [x] Access control via existing `access_by()` scoping on all queries

---

## Implementation Plan

### Phase 1: Tracker Detail Page Component

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create TrackerComponent with unified timeline layout (D6) | `packages/core/modules/Trackers/tracker.tsx` | Pending | L |
| Add dashboard route for `/trackers/[id]` | `apps/dashboard/src/app/(base)/(dashboard)/trackers/[id]/page.tsx` | Pending | S |
| Add navigation from tracker list to detail page | `packages/core/modules/Trackers/index.tsx` | Pending | S |

### Phase 2: Unified Timeline Support

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Extend `ActivityTimeline` to accept optional `trackerEvents` prop | `packages/ui/components/activity-timeline.tsx` | Pending | M |
| Add `tracking-event` activity type rendering in timeline | `packages/ui/components/activity-timeline.tsx` | Pending | M |
| Merge carrier events chronologically with logs/events | `packages/ui/components/activity-timeline.tsx` | Pending | S |

### Phase 3: Preview Sheet Augmentation (Condensed — D5)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `useLogs` and `useEvents` hooks to preview sheet | `packages/ui/components/tracking-preview-sheet.tsx` | Pending | S |
| Add condensed `ActivityTimeline` (last 5 items) | `packages/ui/components/tracking-preview-sheet.tsx` | Pending | S |
| Add "View all" link navigating to `/trackers/[id]` | `packages/ui/components/tracking-preview-sheet.tsx` | Pending | S |

### Phase 4: Polish & Consistency

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Verify breadcrumb navigation on detail page | `packages/core/modules/Trackers/tracker.tsx` | Pending | S |
| Test unified timeline rendering with mixed activity types | Manual testing | Pending | S |
| Verify condensed mode in preview sheet displays correctly | Manual testing | Pending | S |

**Dependencies:**
- Phase 2 can start in parallel with Phase 1 (ActivityTimeline changes are independent of page creation).
- Phase 3 depends on Phase 2 (condensed mode needs the ActivityTimeline changes).
- Phase 4 depends on Phase 1, 2, and 3 completion.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Component Tests | Manual verification | Key flows — detail page renders, timeline shows data |
| Integration Tests | Manual verification | Logs/events filter correctly by tracker entity_id |
| Existing Backend Tests | No changes needed | Existing log/event tests cover `entity_id` filtering |

### Test Cases

#### Manual Verification Steps

```
1. Create a tracker via API or dashboard
2. Navigate to /trackers — verify list page shows the tracker
3. Click tracker row — verify detail page loads at /trackers/[id]
4. Verify detail page shows:
   - Header with tracking number, status, carrier
   - Sidebar with tracker details (ID, carrier, status, metadata)
   - Unified Activity timeline (D6) containing ALL activity types:
     a. Carrier tracking events (e.g., "Package in transit — New York, NY")
     b. API call entries (POST /trackers, GET /trackers/[id])
     c. Trace call entries (carrier API request/response pairs)
     d. System events (tracker_created, tracker_updated)
5. Verify unified timeline sorts all activity types chronologically (newest first)
6. Verify clicking a timeline item shows request/response content in detail panel
7. Click preview button on tracker list — verify preview sheet opens
8. Verify preview sheet shows CONDENSED ActivityTimeline (D5):
   - Only last 5 activity items displayed
   - "View all" link visible, navigating to /trackers/[id]
9. Verify that logs and events are filtered to only this tracker's entity_id
```

#### Existing Backend Tests (No Changes)

The following existing tests already verify the infrastructure this enhancement depends on:

```python
# These tests verify entity_id filtering works for any entity type:
# - Log query with entity_id filter returns only matching logs
# - Event query with entity_id filter returns only matching events
# - TracingRecord.records are properly linked via meta.object_id

# Existing test locations:
# modules/graph/karrio/server/graph/tests/
# modules/core/karrio/server/tracing/tests/
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Verify existing log/event tests still pass (no backend changes)
karrio test --failfast karrio.server.graph.tests

# Frontend build verification
npm run build -w @karrio/core
npm run build -w @karrio/ui
npm run build -w @karrio/dashboard
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| `entity_id` filter doesn't match tracker IDs in logs | High — timeline shows no data | Low — same filter works for shipments/pickups with their IDs | Verify by creating a tracker and checking log entries have correct entity_id |
| ActivityTimeline performance with many tracker logs | Medium — slow timeline rendering | Low — pagination limits to 20 items per page | Same pagination as shipments; proven at scale |
| Preview sheet becomes too tall with ActivityTimeline | Low — UX concern | Medium — ActivityTimeline can be lengthy | Use scrollable container with max-height; consider collapsible section |
| Breaking existing tracker list or preview sheet | Medium — regression | Low — changes are additive | Test existing functionality before and after changes |
| Bundle size increase from new imports in preview sheet | Low — minor | Low — `useLogs`/`useEvents` are small hooks | These hooks are already in the bundle for shipments/pickups |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No backend changes — zero risk to existing APIs
- **Data compatibility**: No model changes — no migrations needed
- **URL compatibility**: New `/trackers/[id]` route is additive; existing `/trackers` and `/tracking/[id]` routes unchanged
- **Feature flags**: Not required — changes are purely additive frontend enhancements

### Rollback Procedure

1. **Identify issue**: Monitor for errors in tracker detail page or preview sheet
2. **Stop rollout**: Revert the frontend commits
3. **Revert changes**: `git revert` the commits adding tracker detail page and preview sheet changes
4. **Verify recovery**: Confirm tracker list page and existing preview sheet work as before

---

## Appendices

### Appendix A: File Change Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `packages/core/modules/Trackers/tracker.tsx` | **New** | Authenticated tracker detail page component with unified timeline |
| `apps/dashboard/src/app/(base)/(dashboard)/trackers/[id]/page.tsx` | **New** | Next.js route for tracker detail page |
| `packages/ui/components/activity-timeline.tsx` | **Modify** | Add optional `trackerEvents` prop and `tracking-event` activity type for unified timeline (D6); add optional `condensed` prop for preview sheet mode (D5) |
| `packages/ui/components/tracking-preview-sheet.tsx` | **Modify** | Add `useLogs`, `useEvents`, condensed `ActivityTimeline`, and "View all" link |
| `packages/core/modules/Trackers/index.tsx` | **Modify** | Add navigation to detail page from list rows |

### Appendix B: Pattern Comparison — Shipment vs Pickup vs Tracker (After)

```
                    Shipment              Pickup                Tracker (After)
                    ────────              ──────                ───────────────
Detail Page         shipment.tsx          pickup.tsx            tracker.tsx
Route               /shipments/[id]       /pickups/[id]         /trackers/[id]
Preview Sheet       shipment-details-     pickup-preview-       tracking-preview-
                    sheet.tsx             sheet.tsx             sheet.tsx
useEntity Hook      useShipment(id)       usePickup(id)         useTracker(id)
useLogs Hook        useLogs({entity_id})  useLogs({entity_id})  useLogs({entity_id})
useEvents Hook      useEvents({entity_id}) useEvents({entity_id}) useEvents({entity_id})
ActivityTimeline    Yes                   Yes                   Yes (unified - D6)
Preview Mode        Full                  Full                  Condensed (D5)
Carrier Events      via tracker.events    via shipment.tracker  Unified into timeline
Sidebar             Details + Metadata    Details + Metadata    Details + Metadata
```

### Appendix C: Relevant Event Types for Trackers

| Event Type | Trigger | Data Payload |
|------------|---------|--------------|
| `tracker_created` | New tracker added | Tracker details, carrier info |
| `tracker_updated` | Tracker status changes (polling or webhook) | Updated tracker details, new events |

### Appendix D: Wireframes

#### D.1: Tracker Detail Page — Unified Timeline (D6)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  < Trackers    Tracking #1Z999AA10123456784                    [... Menu]   │
│                                        Status: In Transit                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────┐  ┌──────────────────────────┐ │
│  │  Shipment                                │  │  Details                 │ │
│  │  shp_xyz789 -- Express -- Delivered      │  │                          │ │
│  │                                          │  │  ID: trk_abc123         │ │
│  │  Messages (if any)                       │  │  Carrier: UPS           │ │
│  │  ! Warning from carrier                  │  │  Status: In Transit     │ │
│  │                                          │  │  Test: No               │ │
│  └──────────────────────────────────────────┘  │  Created: Jan 27, 2026  │ │
│                                                 │                          │ │
│  Activity (Unified Timeline)                    │  Estimated Delivery     │ │
│  ┌──────────────────────────────────────────┐  │  Jan 31, 2026           │ │
│  │  ┌────────────────────┐  ┌────────────┐  │  │                          │ │
│  │  │  Timeline List     │  │  Content   │  │  │  Shipment               │ │
│  │  │                    │  │  Viewer    │  │  │  shp_xyz789 ->          │ │
│  │  │  * Tracking Event  │  │            │  │  │                          │ │
│  │  │    Package arrived │  │  Request:  │  │  │  Metadata                │ │
│  │  │    New York, NY    │  │  { ... }   │  │  │  order_id: ORD-123      │ │
│  │  │    Jan 28, 14:30   │  │            │  │  │                          │ │
│  │  │                    │  │  Response: │  │  └──────────────────────────┘ │
│  │  │  * API Call        │  │  { ... }   │  │                               │
│  │  │    POST /trackers  │  │            │  │                               │
│  │  │    200 OK -- 145ms │  │            │  │                               │
│  │  │                    │  │            │  │                               │
│  │  │  * Tracking Event  │  │            │  │                               │
│  │  │    Package in      │  │            │  │                               │
│  │  │    transit         │  │            │  │                               │
│  │  │    Newark, NJ      │  │            │  │                               │
│  │  │    Jan 28, 08:15   │  │            │  │                               │
│  │  │                    │  │            │  │                               │
│  │  │  * Trace Call      │  │            │  │                               │
│  │  │    UPS Tracking    │  │            │  │                               │
│  │  │    carrier: ups    │  │            │  │                               │
│  │  │    890ms           │  │            │  │                               │
│  │  │                    │  │            │  │                               │
│  │  │  * Tracking Event  │  │            │  │                               │
│  │  │    Shipment picked │  │            │  │                               │
│  │  │    up              │  │            │  │                               │
│  │  │    Chicago, IL     │  │            │  │                               │
│  │  │    Jan 27, 16:00   │  │            │  │                               │
│  │  │                    │  │            │  │                               │
│  │  │  * Event           │  │            │  │                               │
│  │  │    tracker_created │  │            │  │                               │
│  │  │    Jan 27, 15:55   │  │            │  │                               │
│  │  │                    │  │            │  │                               │
│  │  └────────────────────┘  └────────────┘  │                               │
│  └──────────────────────────────────────────┘                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### D.2: Preview Sheet — Condensed Timeline (D5)

```
                          ┌──────────────────────────────────┐
                          │  Tracking Details           [X]  │
                          ├──────────────────────────────────┤
                          │                                  │
                          │  [UPS Logo]                      │
                          │  1Z999AA10123456784               │
                          │  Status: In Transit              │
                          │  Est. Delivery: Jan 31, 2026     │
                          │                                  │
                          │  Tracking Timeline               │
                          │  ┌────────────────────────────┐  │
                          │  │  * Package arrived at      │  │
                          │  │    facility — New York, NY  │  │
                          │  │    Jan 28, 14:30            │  │
                          │  │                            │  │
                          │  │  * Package in transit      │  │
                          │  │    Newark, NJ — Jan 28     │  │
                          │  │                            │  │
                          │  │  * Shipment picked up      │  │
                          │  │    Chicago, IL — Jan 27    │  │
                          │  └────────────────────────────┘  │
                          │                                  │
                          │  Activity          [View all ->] │
                          │  ┌────────────────────────────┐  │
                          │  │  * API Call — POST /trackers│  │
                          │  │    200 OK — 145ms          │  │
                          │  │                            │  │
                          │  │  * Trace — UPS Tracking    │  │
                          │  │    carrier: ups — 890ms    │  │
                          │  │                            │  │
                          │  │  * Event — tracker_created │  │
                          │  │    Jan 27, 15:55           │  │
                          │  └────────────────────────────┘  │
                          │                                  │
                          │  Shipment                        │
                          │  shp_xyz789 — Express     [->]   │
                          │                                  │
                          │  Share                           │
                          │  [Copy Link] [Open Tracking ->]  │
                          └──────────────────────────────────┘
```
