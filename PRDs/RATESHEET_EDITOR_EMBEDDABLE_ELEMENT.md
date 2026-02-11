# Embeddable RateSheet Editor Element

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-10 |
| Status | Planning |
| Owner | Engineering Team |
| Type | Architecture |
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

This PRD defines a minimal approach to ship the **RateSheet Editor** as an embeddable component that can be mounted inside third-party applications (JTL, Teleship React admin, etc.) via an iframe, reusing 100% of the existing editor code. The iframe approach provides complete CSS and JavaScript isolation, eliminating React version conflicts and Tailwind class collisions with host applications.

### Key Architecture Decisions

1. **Iframe isolation**: The editor runs inside a sandboxed iframe to guarantee zero CSS/JS conflicts with host apps regardless of their framework or styling approach.
2. **Zero modifications to existing components**: The `RateSheetEditor` and all 15+ child components remain unchanged. We only create a new entry point and a thin embed provider that replaces the `ClientProvider` + `useSyncedSession` auth chain.
3. **API key authentication**: The iframe receives an API token and host URL via `postMessage`, replacing the session-based auth flow. This reuses the existing Karrio token auth that the API already supports.
4. **Vite standalone build**: A single Vite build produces one JS bundle + one CSS file that are served as Django static files. No Rollup multi-config complexity.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| RateSheet Editor as iframe-embedded element | DevTools, Template Editor, Connection Editor elements |
| Host-side mounting script (`elements.js`) | npm package distribution / CDN hosting |
| API token authentication for the iframe | New API key scopes or permission system |
| Iframe resize + event communication | Appearance/theming API (Tailwind variables suffice) |
| Static file serving from Django | Real-time collaborative editing |
| Create and edit rate sheet flows | Rate sheet list/management view |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Iframe vs direct mount | Iframe | Host apps (JTL, Teleship) may use different React versions, Tailwind configs, or entirely different CSS frameworks. Iframe provides complete isolation. | 2026-02-10 |
| D2 | Auth mechanism | Existing API token via postMessage | Karrio API already accepts `Token <key>` auth. No need to build a new scoped API key system for v1. | 2026-02-10 |
| D3 | Build tool | Vite | Handles React, Tailwind, and CSS extraction out of the box. Simpler than Rollup multi-config. | 2026-02-10 |
| D4 | Modify existing components? | No | The hook injection pattern (`useRateSheet`, `useRateSheetMutation` as props) already decouples the editor from its data layer. We only swap the outer provider shell. | 2026-02-10 |

---

## Problem Statement

### Current State

The RateSheet Editor lives inside the Karrio Next.js dashboard and is mounted like this:

```
apps/dashboard/
  └── Next.js app
        └── ClientProvider (next-auth session → Bearer token)
              └── APIMetadataProvider (fetches /v1/references)
                    └── RateSheetEditor
                          ├── useRateSheet (injected hook)
                          └── useRateSheetMutation (injected hook)
```

The auth chain flows through `useSyncedSession` → `next-auth/react` → `getSession()` → `session.accessToken`, which requires a full Next.js + next-auth setup.

```typescript
// packages/hooks/karrio.tsx - Current auth chain (simplified)
const { query: sessionQuery } = useSyncedSession();
const session = sessionQuery.data as ExtendedSessionType;
const authHeader = session?.accessToken
  ? `Bearer ${session.accessToken}`
  : undefined;

// This interceptor is set on every request
client.axios.interceptors.request.use((config) => {
  config.headers = { ...config.headers, authorization: authHeader };
  return config;
});
```

### Desired State

Third-party apps embed the editor with ~5 lines of code:

```html
<script src="https://your-karrio.com/static/karrio/elements/elements.js"></script>
<div id="ratesheet-editor" style="height: 700px;"></div>
<script>
  KarrioElements.mount('#ratesheet-editor', {
    host: 'https://your-karrio.com',
    token: 'key_xxxxxxxxx',
    rateSheetId: 'new',          // or existing ID
    carrier: 'generic',          // optional pre-select
  });
</script>
```

The editor runs in an iframe, fully isolated from the host app's CSS and JS.

### Problems

1. **Next.js lock-in**: `ClientProvider` depends on `useSyncedSession` which depends on `next-auth/react`. The editor cannot render without a full Next.js session.
2. **No standalone distribution**: There is no built artifact that can be loaded in a third-party app. All UI packages are workspace-internal.
3. **CSS collision risk**: The editor uses Tailwind with `@karrio/ui` utility classes. Direct mounting (without iframe) in a host app that uses Tailwind or similar utility CSS would produce visual corruption.
4. **React version coupling**: Direct mounting requires the host app to provide a compatible React 18 instance. Host apps like JTL may use different React versions or frameworks entirely.

---

## Goals & Success Criteria

### Goals

1. Ship a working embedded RateSheet Editor with zero changes to existing `packages/ui/components/` code.
2. Iframe-based isolation so any host app (React, Vue, vanilla JS, any version) can embed it.
3. Simple integration: host app includes one `<script>` tag and calls `mount()`.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Existing component changes | 0 files modified in `packages/ui/` | Must-have |
| Integration code for host app | < 10 lines | Must-have |
| Editor loads in plain HTML page | Yes | Must-have |
| Editor loads in React 17 host app | Yes (iframe isolation) | Must-have |
| Editor loads alongside host Tailwind | No visual conflicts | Must-have |
| iframe bundle size (JS + CSS gzipped) | < 800KB | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] RateSheet Editor renders in iframe with API token auth
- [ ] Create new rate sheet flow works end-to-end
- [ ] Edit existing rate sheet flow works end-to-end
- [ ] Host app receives `save` and `close` events via postMessage
- [ ] Iframe auto-resizes to content height

**Nice-to-have (P1):**
- [ ] Loading skeleton while iframe initializes
- [ ] Error boundary with user-friendly message inside iframe
- [ ] `dark` / `light` theme toggle via postMessage

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: Iframe isolation** | Complete CSS/JS/React isolation; works in any host app; security via sandbox | Slightly more complex communication; resize handling needed; cross-origin nuances | **Selected** |
| B: Direct React mount (no iframe) | Simpler communication; smaller bundle (shared React) | CSS conflicts with host Tailwind; React version conflicts; global state leaks; requires host to provide React 18 | Rejected |
| C: Web Components / Shadow DOM | CSS isolation via Shadow DOM; no iframe overhead | Shadow DOM + React is fragile; Tailwind does not work inside Shadow DOM without hacks; React portals break | Rejected |
| D: Full Karrio Elements platform (original PRD) | Covers all components; theming API; scoped API keys | Over-scoped; 4-6 week effort; delays shipping a working ratesheet embed | Rejected for v1 |

### Trade-off Analysis

**Iframe** is the right choice because the primary embedding targets (JTL app, Teleship React admin) are third-party apps where we don't control the CSS or React version. Stripe, Shopify, and Plaid all use iframes for their embedded components for exactly this reason. The overhead of iframe communication is minimal for this use case since the editor is a full-page interactive component, not a small inline widget.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| RateSheet Editor + 15 child components | `packages/ui/components/rate-sheet-editor.tsx` + siblings | **Unchanged** - imported directly into iframe entry point |
| Rate sheet hooks (user) | `packages/hooks/rate-sheet.ts` | **Unchanged** - injected into editor via props |
| Rate sheet hooks (admin) | `packages/hooks/admin-rate-sheets.ts` | **Unchanged** - available for admin embed mode |
| GraphQL types + queries | `packages/types/graphql/` | **Unchanged** - imported by hooks |
| API metadata provider | `packages/hooks/api-metadata.tsx` | **Adapted** - new embed-compatible version that doesn't require session |
| Karrio client provider | `packages/hooks/karrio.tsx` | **Replaced** - new `KarrioEmbedProvider` uses token instead of session |
| shadcn/ui components | `packages/ui/components/ui/` | **Unchanged** - bundled into iframe build |
| Toast hook | `packages/ui/hooks/use-toast.ts` | **Unchanged** - bundled into iframe build |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         HOST APPLICATION                                  │
│  (JTL, Teleship, any React/Vue/vanilla app)                              │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  <script src="https://karrio/static/karrio/elements/elements.js">│  │
│  │                                                                    │  │
│  │  KarrioElements.mount('#container', {                             │  │
│  │    host: 'https://karrio-api.example.com',                        │  │
│  │    token: 'key_xxxxx',                                            │  │
│  │    rateSheetId: 'new',                                            │  │
│  │  });                                                               │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  <div id="container">                                              │  │
│  │    ┌────────────────────────────────────────────────────────────┐  │  │
│  │    │  <iframe sandbox="allow-scripts allow-same-origin">       │  │  │
│  │    │                                                            │  │  │
│  │    │    KarrioEmbedProvider (token auth, no next-auth)         │  │  │
│  │    │      └── APIMetadataEmbedProvider (fetches /v1/references)│  │  │
│  │    │            └── QueryClientProvider                        │  │  │
│  │    │                  └── Toaster                              │  │  │
│  │    │                        └── RateSheetEditor  ← UNCHANGED  │  │  │
│  │    │                              ├── useRateSheet (injected)  │  │  │
│  │    │                              └── useRateSheetMutation     │  │  │
│  │    │                                                            │  │  │
│  │    └────────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ REST + GraphQL (Token auth)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          KARRIO SERVER                                    │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  /static/karrio/elements/                                          │  │
│  │    ├── elements.js          (host-side script, ~3KB)               │  │
│  │    ├── ratesheet.html       (iframe shell)                         │  │
│  │    ├── ratesheet.js         (React app bundle)                     │  │
│  │    └── ratesheet.css        (Tailwind + component styles)          │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  API (authenticated via Token header)                               │  │
│  │    ├── /graphql     (rate_sheet queries & mutations)                │  │
│  │    └── /v1/references (carrier metadata)                           │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────────┐     ┌────────────┐     ┌────────┐
│  Host  │     │ elements.js│     │   Iframe   │     │ Karrio │
│  App   │     │  (host)    │     │ (ratesheet)│     │  API   │
└───┬────┘     └─────┬──────┘     └─────┬──────┘     └───┬────┘
    │                │                   │                │
    │  1. mount()    │                   │                │
    │───────────────>│                   │                │
    │                │                   │                │
    │                │  2. Create iframe │                │
    │                │  src=ratesheet.html                │
    │                │──────────────────>│                │
    │                │                   │                │
    │                │                   │  3. Load JS/CSS│
    │                │                   │  (from static) │
    │                │                   │                │
    │                │  4. iframe ready  │                │
    │                │  postMessage:READY│                │
    │                │<──────────────────│                │
    │                │                   │                │
    │                │  5. postMessage:  │                │
    │                │  INIT {token,host,│                │
    │                │  rateSheetId,...} │                │
    │                │──────────────────>│                │
    │                │                   │                │
    │                │                   │  6. GET        │
    │                │                   │  /v1/references│
    │                │                   │───────────────>│
    │                │                   │                │
    │                │                   │  7. GraphQL    │
    │                │                   │  GET_RATE_SHEET│
    │                │                   │───────────────>│
    │                │                   │                │
    │                │                   │  8. Render     │
    │                │                   │  editor UI     │
    │                │                   │                │
    │                │  9. RESIZE        │                │
    │                │  {height: 750}    │                │
    │                │<──────────────────│                │
    │                │                   │                │
    │                │  (auto-resize     │                │
    │                │   iframe height)  │                │
    │                │                   │                │
    │                │       ... user edits rate sheet ...│
    │                │                   │                │
    │                │                   │  10. GraphQL   │
    │                │                   │  mutations     │
    │                │                   │───────────────>│
    │                │                   │                │
    │  11. EVENT     │  11. EVENT        │                │
    │  {type:'save'} │  {type:'save'}    │                │
    │<───────────────│<──────────────────│                │
    │                │                   │                │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    INITIALIZATION FLOW                                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Host App              elements.js            Iframe                      │
│  ┌─────────┐    ┌───────────────────┐    ┌──────────────────────┐        │
│  │ mount() │───>│ Create <iframe>   │───>│ ratesheet.html loads │        │
│  │ {token, │    │ Listen for msgs   │    │ ratesheet.js boots   │        │
│  │  host,  │    │ Forward events    │    │ Sends READY msg      │        │
│  │  opts}  │    └───────────────────┘    └──────────────────────┘        │
│  └─────────┘             │                         ▲                      │
│                          │    INIT {token,host}    │                      │
│                          └─────────────────────────┘                      │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                    RUNTIME FLOW                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Iframe App                                          Karrio API           │
│  ┌──────────────────┐                                                     │
│  │ KarrioEmbedProv. │─── Token in Authorization header ──┐               │
│  │  ├─ MetadataProv. │─── GET /v1/references ────────────>│               │
│  │  │  └─ QueryClient│                                    │               │
│  │  │     └─ Editor  │─── POST /graphql ─────────────────>│               │
│  │  │        ├─ hooks │   (GET_RATE_SHEET, mutations)     │               │
│  │  │        └─ UI   │                                    │               │
│  └──────────────────┘                              ┌──────▼──────┐       │
│         │                                          │ Karrio API  │       │
│         │  postMessage: RESIZE, EVENT              │ (unchanged) │       │
│         ▼                                          └─────────────┘       │
│  ┌──────────────┐                                                        │
│  │ elements.js  │─── callback to host app                                │
│  └──────────────┘                                                        │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### New Files to Create

#### 1. Host-side script: `packages/elements/src/host/elements.ts`

This is the lightweight script (~3KB) that the host app loads. It creates the iframe and brokers communication.

```typescript
// packages/elements/src/host/elements.ts

interface MountOptions {
  host: string;            // Karrio API URL
  token: string;           // API token (existing Karrio token)
  rateSheetId?: string;    // 'new' or existing ID (default: 'new')
  carrier?: string;        // Pre-select carrier (default: 'generic')
  connectionId?: string;   // Link to carrier connection
}

interface ElementHandle {
  on: (event: string, callback: (data?: any) => void) => void;
  unmount: () => void;
  update: (options: Partial<MountOptions>) => void;
}

type MessageType = 'READY' | 'INIT' | 'RESIZE' | 'EVENT' | 'UPDATE';

interface ElementMessage {
  source: 'karrio-element';
  type: MessageType;
  payload?: any;
}

const KarrioElements = {
  mount(selector: string, options: MountOptions): ElementHandle {
    const container =
      typeof selector === 'string'
        ? document.querySelector(selector)
        : selector;

    if (!container) {
      throw new Error(`KarrioElements: container "${selector}" not found`);
    }

    const listeners: Record<string, ((data?: any) => void)[]> = {};
    const iframe = document.createElement('iframe');
    const elementId = `karrio-ratesheet-${Date.now()}`;

    iframe.src = `${options.host}/static/karrio/elements/ratesheet.html`;
    iframe.id = elementId;
    iframe.style.cssText = 'border:none;width:100%;height:100%;min-height:400px;';
    iframe.setAttribute(
      'sandbox',
      'allow-scripts allow-same-origin allow-forms',
    );

    function handleMessage(event: MessageEvent) {
      const msg = event.data as ElementMessage;
      if (msg?.source !== 'karrio-element') return;

      switch (msg.type) {
        case 'READY':
          // Iframe loaded, send config
          iframe.contentWindow?.postMessage(
            {
              source: 'karrio-host',
              type: 'INIT',
              payload: {
                host: options.host,
                token: options.token,
                rateSheetId: options.rateSheetId || 'new',
                carrier: options.carrier,
                connectionId: options.connectionId,
              },
            },
            '*',
          );
          break;

        case 'RESIZE':
          iframe.style.height = `${msg.payload.height}px`;
          break;

        case 'EVENT':
          const cbs = listeners[msg.payload.type] || [];
          cbs.forEach((cb) => cb(msg.payload.data));
          break;
      }
    }

    window.addEventListener('message', handleMessage);
    container.appendChild(iframe);

    return {
      on(event, callback) {
        if (!listeners[event]) listeners[event] = [];
        listeners[event].push(callback);
      },
      unmount() {
        window.removeEventListener('message', handleMessage);
        iframe.remove();
      },
      update(newOptions) {
        iframe.contentWindow?.postMessage(
          { source: 'karrio-host', type: 'UPDATE', payload: newOptions },
          '*',
        );
      },
    };
  },
};

// Global export for script tag usage
if (typeof window !== 'undefined') {
  (window as any).KarrioElements = KarrioElements;
}

export default KarrioElements;
```

#### 2. Embed provider: `packages/elements/src/providers/karrio-embed-provider.tsx`

Replaces `ClientProvider` + `useSyncedSession`. Provides the same `useKarrio()` interface that `packages/hooks/rate-sheet.ts` expects, but powered by a static API token instead of next-auth.

```typescript
// packages/elements/src/providers/karrio-embed-provider.tsx

import React, { createContext, useContext, useMemo } from 'react';
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';

interface EmbedConfig {
  host: string;
  token: string;
  testMode?: boolean;
  orgId?: string;
}

interface EmbedContextValue {
  host: string;
  token: string;
  headers: Record<string, string>;
  graphqlRequest: <T>(query: string, variables?: any) => Promise<T>;
}

const EmbedContext = createContext<EmbedContextValue | null>(null);
const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 5 * 60 * 1000 } },
});

export function KarrioEmbedProvider({
  config,
  children,
}: {
  config: EmbedConfig;
  children: React.ReactNode;
}) {
  const headers = useMemo(
    () => ({
      'Content-Type': 'application/json',
      Authorization: `Token ${config.token}`,
      ...(config.testMode ? { 'X-Test-Mode': 'true' } : {}),
      ...(config.orgId ? { 'X-Org-Id': config.orgId } : {}),
    }),
    [config.token, config.testMode, config.orgId],
  );

  const graphqlRequest = useMemo(
    () =>
      async <T,>(query: string, variables?: any): Promise<T> => {
        const res = await fetch(`${config.host}/graphql`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ query, variables }),
        });
        const json = await res.json();
        if (json.errors) throw new Error(json.errors[0]?.message);
        return json.data;
      },
    [config.host, headers],
  );

  const value = useMemo(
    () => ({ host: config.host, token: config.token, headers, graphqlRequest }),
    [config.host, config.token, headers, graphqlRequest],
  );

  return (
    <EmbedContext.Provider value={value}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </EmbedContext.Provider>
  );
}

export function useKarrioEmbed() {
  const ctx = useContext(EmbedContext);
  if (!ctx) throw new Error('useKarrioEmbed must be used within KarrioEmbedProvider');
  return ctx;
}
```

#### 3. Embed-compatible hooks: `packages/elements/src/hooks/embed-rate-sheet.ts`

These hooks mirror the exact signatures of `packages/hooks/rate-sheet.ts` but use the embed provider instead of `useKarrio()` / `useAuthenticatedQuery()`.

```typescript
// packages/elements/src/hooks/embed-rate-sheet.ts
//
// Mirrors the interface of packages/hooks/rate-sheet.ts
// but uses KarrioEmbedProvider instead of ClientProvider + next-auth.
//
// Imports the SAME GraphQL query strings and types from @karrio/types/graphql.
// The only difference is the data-fetching mechanism: fetch() with Token header
// instead of KarrioClient axios with Bearer session token.

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useKarrioEmbed } from '../providers/karrio-embed-provider';
import { gqlstr } from '@karrio/lib';

// Import the exact same GraphQL operations that packages/hooks/rate-sheet.ts uses
import {
  GET_RATE_SHEETS,
  GET_RATE_SHEET,
  CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET,
  DELETE_RATE_SHEET,
  DELETE_RATE_SHEET_SERVICE,
  ADD_SHARED_ZONE,
  UPDATE_SHARED_ZONE,
  DELETE_SHARED_ZONE,
  ADD_SHARED_SURCHARGE,
  UPDATE_SHARED_SURCHARGE,
  DELETE_SHARED_SURCHARGE,
  BATCH_UPDATE_SURCHARGES,
  UPDATE_SERVICE_RATE,
  BATCH_UPDATE_SERVICE_RATES,
  UPDATE_SERVICE_ZONE_IDS,
  UPDATE_SERVICE_SURCHARGE_IDS,
  ADD_WEIGHT_RANGE,
  REMOVE_WEIGHT_RANGE,
  DELETE_SERVICE_RATE,
} from '@karrio/types/graphql';

import type {
  GetRateSheets,
  GetRateSheet,
  RateSheetFilter,
} from '@karrio/types/graphql';

// ─── useRateSheet (matches packages/hooks/rate-sheet.ts signature) ───

export function useRateSheet({ id }: { id?: string } = {}) {
  const { graphqlRequest } = useKarrioEmbed();
  const [rateSheetId, setRateSheetId] = React.useState(id || '');

  const query = useQuery(
    ['rate-sheet', rateSheetId],
    () => graphqlRequest<GetRateSheet>(gqlstr(GET_RATE_SHEET), { data: { id: rateSheetId } }),
    { enabled: !!rateSheetId && rateSheetId !== 'new' },
  );

  return { query, rateSheetId, setRateSheetId };
}

// ─── useRateSheetMutation (matches packages/hooks/rate-sheet.ts signature) ───

export function useRateSheetMutation() {
  const { graphqlRequest } = useKarrioEmbed();
  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries(['rate-sheet']);

  const makeMutation = <TInput, TResult = any>(document: any) =>
    useMutation(
      (data: { id?: string; data?: TInput }) =>
        graphqlRequest<TResult>(gqlstr(document), { data }),
      { onSuccess: invalidate },
    );

  return {
    createRateSheet:           makeMutation(CREATE_RATE_SHEET),
    updateRateSheet:           makeMutation(UPDATE_RATE_SHEET),
    deleteRateSheet:           makeMutation(DELETE_RATE_SHEET),
    deleteRateSheetService:    makeMutation(DELETE_RATE_SHEET_SERVICE),
    addSharedZone:             makeMutation(ADD_SHARED_ZONE),
    updateSharedZone:          makeMutation(UPDATE_SHARED_ZONE),
    deleteSharedZone:          makeMutation(DELETE_SHARED_ZONE),
    addSharedSurcharge:        makeMutation(ADD_SHARED_SURCHARGE),
    updateSharedSurcharge:     makeMutation(UPDATE_SHARED_SURCHARGE),
    deleteSharedSurcharge:     makeMutation(DELETE_SHARED_SURCHARGE),
    batchUpdateSurcharges:     makeMutation(BATCH_UPDATE_SURCHARGES),
    updateServiceRate:         makeMutation(UPDATE_SERVICE_RATE),
    batchUpdateServiceRates:   makeMutation(BATCH_UPDATE_SERVICE_RATES),
    addWeightRange:            makeMutation(ADD_WEIGHT_RANGE),
    removeWeightRange:         makeMutation(REMOVE_WEIGHT_RANGE),
    deleteServiceRate:         makeMutation(DELETE_SERVICE_RATE),
    updateServiceZoneIds:      makeMutation(UPDATE_SERVICE_ZONE_IDS),
    updateServiceSurchargeIds: makeMutation(UPDATE_SERVICE_SURCHARGE_IDS),
  };
}
```

#### 4. Embed-compatible metadata provider: `packages/elements/src/providers/api-metadata-embed-provider.tsx`

Mirrors `packages/hooks/api-metadata.tsx` but uses the embed token for the `/v1/references` fetch.

```typescript
// packages/elements/src/providers/api-metadata-embed-provider.tsx

import React, { createContext, useContext } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useKarrioEmbed } from './karrio-embed-provider';

interface APIMetadataContextValue {
  metadata: any;
  references: any;
  getHost: () => string;
}

const APIMetadataContext = createContext<APIMetadataContextValue | null>(null);

export function APIMetadataEmbedProvider({ children }: { children: React.ReactNode }) {
  const { host, headers } = useKarrioEmbed();

  const { data: references } = useQuery(
    ['references', host],
    async () => {
      const res = await fetch(`${host}/v1/references`, { headers });
      return res.json();
    },
    { staleTime: 10 * 60 * 1000 }, // Cache for 10 minutes
  );

  const value = {
    metadata: references || {},
    references: references || {},
    getHost: () => host,
  };

  return (
    <APIMetadataContext.Provider value={value}>
      {references ? children : <LoadingSkeleton />}
    </APIMetadataContext.Provider>
  );
}

// Re-export the same hook name so existing components work unchanged
export function useAPIMetadata() {
  const ctx = useContext(APIMetadataContext);
  if (!ctx) throw new Error('useAPIMetadata must be used within APIMetadataEmbedProvider');
  return ctx;
}
```

**Key insight**: The existing `RateSheetEditor` imports `useAPIMetadata` from `@karrio/hooks/api-metadata`. The Vite build will alias this import to our embed version so the editor component code stays unchanged.

#### 5. Iframe entry point: `packages/elements/src/entries/ratesheet.tsx`

This is the React app that runs inside the iframe.

```typescript
// packages/elements/src/entries/ratesheet.tsx

import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { KarrioEmbedProvider } from '../providers/karrio-embed-provider';
import { APIMetadataEmbedProvider } from '../providers/api-metadata-embed-provider';
import { RateSheetEditor } from '@karrio/ui/components/rate-sheet-editor';
import { Toaster } from '@karrio/ui/components/ui/toaster';
import { useRateSheet, useRateSheetMutation } from '../hooks/embed-rate-sheet';

// Import Tailwind styles (bundled into ratesheet.css by Vite)
import '../styles/tailwind.css';

interface InitPayload {
  host: string;
  token: string;
  rateSheetId?: string;
  carrier?: string;
  connectionId?: string;
}

function sendToHost(type: string, payload?: any) {
  window.parent.postMessage(
    { source: 'karrio-element', type, payload },
    '*',
  );
}

// Auto-resize iframe to content height
function useAutoResize() {
  useEffect(() => {
    const observer = new ResizeObserver(() => {
      const height = document.documentElement.scrollHeight;
      sendToHost('RESIZE', { height });
    });
    observer.observe(document.body);
    return () => observer.disconnect();
  }, []);
}

function RateSheetApp({ config }: { config: InitPayload }) {
  useAutoResize();

  return (
    <KarrioEmbedProvider
      config={{ host: config.host, token: config.token }}
    >
      <APIMetadataEmbedProvider>
        <RateSheetEditor
          rateSheetId={config.rateSheetId || 'new'}
          preloadCarrier={config.carrier}
          linkConnectionId={config.connectionId}
          onClose={() => sendToHost('EVENT', { type: 'close' })}
          useRateSheet={useRateSheet}
          useRateSheetMutation={useRateSheetMutation}
        />
        <Toaster />
      </APIMetadataEmbedProvider>
    </KarrioEmbedProvider>
  );
}

function App() {
  const [config, setConfig] = useState<InitPayload | null>(null);

  useEffect(() => {
    function handleMessage(event: MessageEvent) {
      const msg = event.data;
      if (msg?.source !== 'karrio-host') return;

      if (msg.type === 'INIT') {
        setConfig(msg.payload);
      }
      if (msg.type === 'UPDATE' && config) {
        setConfig((prev) => (prev ? { ...prev, ...msg.payload } : prev));
      }
    }

    window.addEventListener('message', handleMessage);

    // Signal to host that iframe is ready to receive config
    sendToHost('READY');

    return () => window.removeEventListener('message', handleMessage);
  }, []);

  if (!config) {
    return <LoadingSkeleton />;
  }

  return <RateSheetApp config={config} />;
}

// Boot
const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

#### 6. Iframe HTML shell: `packages/elements/static/ratesheet.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Karrio RateSheet Editor</title>
  <link rel="stylesheet" href="./ratesheet.css">
  <style>
    html, body, #root {
      margin: 0;
      padding: 0;
      width: 100%;
      background: transparent;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script src="./ratesheet.js"></script>
</body>
</html>
```

#### 7. Vite config: `packages/elements/vite.config.ts`

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Redirect @karrio/hooks/api-metadata to our embed version
      // so RateSheetEditor's import works without code changes
      '@karrio/hooks/api-metadata': resolve(
        __dirname,
        'src/providers/api-metadata-embed-provider.tsx',
      ),
      // Redirect @karrio/hooks/karrio imports (if any child component uses useKarrio)
      '@karrio/hooks/karrio': resolve(
        __dirname,
        'src/providers/karrio-embed-shim.ts',
      ),
    },
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        // Host-side script (tiny, no React)
        elements: resolve(__dirname, 'src/host/elements.ts'),
        // Iframe React app (full bundle with React + Tailwind)
        ratesheet: resolve(__dirname, 'src/entries/ratesheet.tsx'),
      },
      output: {
        entryFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
      },
    },
  },
});
```

### Import Aliasing Strategy

This is the critical technique that lets us reuse existing components **without modifying them**.

The `RateSheetEditor` component imports:
```typescript
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
```

In the normal Next.js dashboard, this resolves to `packages/hooks/api-metadata.tsx` which requires `ClientProvider` + `useSyncedSession`.

In our Vite build, the alias in `vite.config.ts` redirects this import to our embed-compatible version that uses the API token instead. The component code is identical — only the module resolution changes at build time.

```
Normal dashboard build:
  @karrio/hooks/api-metadata  →  packages/hooks/api-metadata.tsx  →  needs next-auth

Elements iframe build:
  @karrio/hooks/api-metadata  →  packages/elements/src/providers/api-metadata-embed-provider.tsx  →  uses Token
```

The same approach applies to any other hook that the editor's child components might import from `@karrio/hooks/karrio`.

### New Package Structure

```
packages/elements/                    # NEW PACKAGE
├── package.json
├── vite.config.ts
├── tsconfig.json
├── src/
│   ├── host/
│   │   └── elements.ts              # Host-side mount script (no React)
│   ├── entries/
│   │   └── ratesheet.tsx             # Iframe React entry point
│   ├── providers/
│   │   ├── karrio-embed-provider.tsx # Token-based auth provider
│   │   ├── api-metadata-embed-provider.tsx  # Embed-compatible metadata
│   │   └── karrio-embed-shim.ts     # Shim for useKarrio() if needed
│   ├── hooks/
│   │   └── embed-rate-sheet.ts      # Embed-compatible rate sheet hooks
│   └── styles/
│       └── tailwind.css             # @tailwind base/components/utilities
├── static/
│   └── ratesheet.html               # Iframe shell
└── dist/                             # Build output (gitignored)
    ├── elements.js                   # Host script (~3KB)
    ├── ratesheet.html                # Copied from static/
    ├── ratesheet.js                  # Iframe bundle (React + all components)
    └── ratesheet.css                 # Tailwind + component styles
```

### Files NOT Modified

| File | Why unchanged |
|------|---------------|
| `packages/ui/components/rate-sheet-editor.tsx` | Hook injection + import aliasing means zero changes |
| `packages/ui/components/rate-sheet-table.tsx` | Pure UI component, no auth dependencies |
| `packages/ui/components/zones-tab.tsx` | Pure UI component |
| `packages/ui/components/services-tab.tsx` | Pure UI component |
| `packages/ui/components/surcharges-tab.tsx` | Pure UI component |
| `packages/ui/components/weight-rate-grid.tsx` | Pure UI component |
| All 10+ dialog/popover child components | Pure UI components |
| `packages/hooks/rate-sheet.ts` | Dashboard still uses this; embed has its own version |
| `packages/hooks/karrio.tsx` | Dashboard still uses this unchanged |
| `packages/hooks/api-metadata.tsx` | Dashboard still uses this unchanged |
| `packages/types/graphql/*` | Shared types, imported by both versions |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Invalid API token | Editor shows auth error | Iframe catches 401/403 from API, shows inline error message, sends `EVENT:{type:'error'}` to host |
| Rate sheet ID not found | Editor shows not-found state | GraphQL query returns null, editor shows "Rate sheet not found" with option to create new |
| Host app unmounts container while iframe loads | No orphaned iframes | `unmount()` removes iframe and cleans up message listener |
| Network failure mid-edit | Toast notification in iframe | Existing react-query retry + toast error handling applies unchanged |
| `/v1/references` fails to load | Editor can't show carrier list | `APIMetadataEmbedProvider` shows loading skeleton indefinitely; sends error event to host |
| Multiple elements mounted simultaneously | Each operates independently | Each iframe has unique ID, message filtering by `source` field |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Host app blocks iframe via CSP | Editor doesn't render | Document required CSP: `frame-src your-karrio.com` |
| CORS blocks API calls from iframe | All API calls fail | Karrio server already sets CORS headers for API; static files need same-origin or CORS |
| Iframe bundle too large (>2MB) | Slow initial load | Tree-shake unused exports; code-split if needed; monitor bundle size in CI |
| postMessage origin mismatch | INIT never received | Validate origin loosely in v1 (same Karrio host); tighten in v2 |

### Security Considerations

- [x] Iframe sandbox restricts navigation and popups
- [x] API token sent via postMessage, not URL (no referer leakage)
- [x] No `allow-top-navigation` in sandbox (iframe can't redirect host)
- [x] API token has same permissions as when used directly — no privilege escalation
- [ ] Future: validate `event.origin` in iframe message handler against configured host

---

## Implementation Plan

### Phase 1: Foundation (embed provider + iframe entry)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `packages/elements/` package structure | `package.json`, `tsconfig.json`, `vite.config.ts` | Pending | S |
| Implement `KarrioEmbedProvider` | `src/providers/karrio-embed-provider.tsx` | Pending | S |
| Implement `APIMetadataEmbedProvider` | `src/providers/api-metadata-embed-provider.tsx` | Pending | S |
| Implement embed rate sheet hooks | `src/hooks/embed-rate-sheet.ts` | Pending | M |
| Implement iframe entry point | `src/entries/ratesheet.tsx` | Pending | M |
| Create iframe HTML shell | `static/ratesheet.html` | Pending | S |
| Configure Vite build with import aliases | `vite.config.ts` | Pending | M |
| Verify editor renders in iframe with token auth | Manual testing | Pending | M |

### Phase 2: Host-side script + integration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Implement host-side `elements.js` | `src/host/elements.ts` | Pending | S |
| Implement postMessage protocol (READY/INIT/RESIZE/EVENT) | Host + iframe entry | Pending | M |
| Add iframe auto-resize via ResizeObserver | `src/entries/ratesheet.tsx` | Pending | S |
| Build script to copy dist → Django static files | `bin/build-elements` | Pending | S |
| Test in plain HTML page | `examples/ratesheet.html` | Pending | S |

### Phase 3: Polish + deployment

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Loading skeleton for iframe initialization | `src/entries/ratesheet.tsx` | Pending | S |
| Error boundary inside iframe | `src/entries/ratesheet.tsx` | Pending | S |
| Integration test: embed in JTL (or mock host app) | External testing | Pending | M |
| Integration test: embed in Teleship React admin | External testing | Pending | M |
| Document CSP / CORS requirements | `README.md` in elements package | Pending | S |

**Dependencies:** Phase 2 depends on Phase 1 completion. Phase 3 depends on Phase 2.

**Total estimated new code:** ~400-500 lines across 7-8 new files. Zero changes to existing files.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Host script unit tests | `packages/elements/__tests__/elements.test.ts` | Mount/unmount/messaging |
| Provider unit tests | `packages/elements/__tests__/providers.test.tsx` | Auth header injection, GraphQL requests |
| Integration test | `packages/elements/examples/ratesheet.html` | Full end-to-end in browser |
| Cross-browser test | Manual | Chrome, Firefox, Safari |

### Integration Test (Plain HTML)

```html
<!-- packages/elements/examples/ratesheet.html -->
<!DOCTYPE html>
<html>
<head>
  <title>RateSheet Editor - Integration Test</title>
  <script src="../dist/elements.js"></script>
</head>
<body>
  <h1>Embedded RateSheet Editor</h1>
  <div id="editor" style="height: 700px; border: 1px solid #ccc;"></div>

  <script>
    const handle = KarrioElements.mount('#editor', {
      host: 'http://localhost:5002',
      token: 'key_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
      rateSheetId: 'new',
    });

    handle.on('save', (data) => {
      console.log('Rate sheet saved:', data);
    });

    handle.on('close', () => {
      console.log('Editor closed');
      handle.unmount();
    });

    handle.on('error', (err) => {
      console.error('Editor error:', err);
    });
  </script>
</body>
</html>
```

### Running Tests

```bash
# Build the elements package
cd packages/elements && npm run build

# Copy to Django static
bin/build-elements

# Start Karrio server
bin/start-server

# Open test page in browser
open packages/elements/examples/ratesheet.html
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Import aliasing misses a deep dependency | Build fails or runtime error | Medium | Test thoroughly; Vite build will error on unresolved imports |
| Bundle size exceeds 2MB gzipped | Slow load on first mount | Low | Monitor with `vite-plugin-inspect`; most deps are already needed |
| `useAPIMetadata` signature mismatch | Runtime crash in editor | Low | Our embed version exports the exact same interface |
| Tailwind CSS not fully included in iframe bundle | Missing styles | Medium | Ensure `content` paths in iframe Tailwind config include all `@karrio/ui` component files |
| react-query version mismatch between hooks and provider | Runtime error | Low | Pin exact version in elements `package.json` |

---

## Migration & Rollback

### Backward Compatibility

- **Zero impact on existing dashboard**: No files in `packages/ui/`, `packages/hooks/`, or `packages/core/` are modified. The existing Next.js dashboard continues to work exactly as before.
- **Additive only**: The `packages/elements/` package is entirely new. Removing it has no effect on any existing functionality.
- **API compatibility**: The iframe uses the same GraphQL mutations and REST endpoints that the dashboard already uses. No server-side changes required.

### Rollback Procedure

1. **Identify issue**: Embedded editor not working in host app.
2. **Stop rollout**: Remove `elements.js` script tag from host app.
3. **Revert changes**: Delete `packages/elements/` directory and remove static files from Django.
4. **Verify recovery**: Dashboard rate sheet editor is unaffected (no files were changed).

---

## Appendices

### Appendix A: PostMessage Protocol Reference

| Direction | Message Type | Payload | Description |
|-----------|-------------|---------|-------------|
| Iframe → Host | `READY` | — | Iframe JS has loaded, ready to receive config |
| Host → Iframe | `INIT` | `{host, token, rateSheetId, carrier?, connectionId?}` | Initialize the editor with config |
| Iframe → Host | `RESIZE` | `{height: number}` | Request iframe height change |
| Iframe → Host | `EVENT` | `{type: 'save', data: RateSheet}` | Rate sheet saved successfully |
| Iframe → Host | `EVENT` | `{type: 'close'}` | User clicked close/cancel |
| Iframe → Host | `EVENT` | `{type: 'error', data: {message: string}}` | Unrecoverable error |
| Host → Iframe | `UPDATE` | `Partial<MountOptions>` | Update options (e.g., switch rate sheet) |

All messages include `source: 'karrio-element'` or `source: 'karrio-host'` for filtering.

### Appendix B: Host App Integration Examples

**Vanilla HTML/JS:**
```html
<script src="https://your-karrio.com/static/karrio/elements/elements.js"></script>
<div id="editor"></div>
<script>
  const handle = KarrioElements.mount('#editor', {
    host: 'https://your-karrio.com',
    token: 'key_xxx',
  });
  handle.on('save', (data) => alert('Saved!'));
</script>
```

**React (any version):**
```jsx
import { useEffect, useRef } from 'react';

function RateSheetEmbed({ apiHost, apiToken, rateSheetId }) {
  const ref = useRef(null);
  const handleRef = useRef(null);

  useEffect(() => {
    // KarrioElements loaded via <script> tag
    handleRef.current = window.KarrioElements.mount(ref.current, {
      host: apiHost,
      token: apiToken,
      rateSheetId,
    });

    handleRef.current.on('save', (data) => {
      console.log('Saved:', data);
    });

    return () => handleRef.current?.unmount();
  }, [apiHost, apiToken, rateSheetId]);

  return <div ref={ref} style={{ minHeight: 500 }} />;
}
```

**Vue 3:**
```vue
<template>
  <div ref="container" style="min-height: 500px"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps(['host', 'token', 'rateSheetId']);
const container = ref(null);
let handle = null;

onMounted(() => {
  handle = window.KarrioElements.mount(container.value, {
    host: props.host,
    token: props.token,
    rateSheetId: props.rateSheetId,
  });
});

onUnmounted(() => handle?.unmount());
</script>
```

### Appendix C: Required Server Configuration

The Karrio server must serve the static files with appropriate headers:

```
# For same-origin iframe (editor served from same Karrio domain)
# No additional configuration needed - Django static files work as-is.

# For cross-origin iframe (editor served from different domain than host app)
# Add to Django settings or reverse proxy:

X-Frame-Options: ALLOWALL
# or remove X-Frame-Options and use CSP instead:
Content-Security-Policy: frame-ancestors *;

# CORS for API calls from iframe
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Authorization, Content-Type, X-Test-Mode, X-Org-Id
```

Host applications must allow framing from the Karrio domain in their CSP:
```
Content-Security-Policy: frame-src https://your-karrio.com;
```
