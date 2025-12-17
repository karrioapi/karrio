# Product Requirements Document: Karrio Elements - Embeddable Components

**Project**: Karrio Elements - Stripe Elements-like Embeddable UI Components
**Version**: 1.0
**Date**: 2025-12-16
**Status**: Planning
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Criteria](#3-goals--success-criteria)
4. [Architecture Overview](#4-architecture-overview)
5. [Component Design](#5-component-design)
6. [Authentication Model](#6-authentication-model)
7. [Implementation Plan](#7-implementation-plan)
8. [Package Structure](#8-package-structure)
9. [API Design](#9-api-design)
10. [Build & Deployment](#10-build--deployment)
11. [Security Considerations](#11-security-considerations)
12. [Migration & Refactoring](#12-migration--refactoring)
13. [Testing Strategy](#13-testing-strategy)
14. [Rollout Plan](#14-rollout-plan)

---

## 1. Executive Summary

This document outlines the design and implementation of **Karrio Elements**, a suite of embeddable UI components inspired by Stripe Elements. These components allow developers to embed Karrio functionality (DevTools, RateSheet Editor, Document Template Editor) into their applications using simple iframe-based integration.

### Key Features

| Feature | Description |
|---------|-------------|
| **Iframe Isolation** | Each component runs in a sandboxed iframe for security and style isolation |
| **Public API Key Auth** | Simple, stateless authentication using restricted API keys |
| **Appearance API** | Customizable theming via appearance configuration object |
| **Single Package** | One `@karrio/elements` package with tree-shaking support |
| **Static Hosting** | Built artifacts served from Karrio server static files |

### Components to Ship

1. **DevTools Element** - API logs, events, webhooks, API keys management
2. **RateSheet Editor Element** - Visual rate sheet configuration interface
3. **Document Template Editor Element** - HTML template editor with live preview
4. **Carrier Connection Editor Element** - Carrier account registration and management

### Key Benefits

- **Decoupled from Next.js** - Works in any web application (React, Vue, vanilla JS)
- **Security via Isolation** - Iframe sandbox prevents XSS and style conflicts
- **Simple Integration** - Just include a script and initialize with API key
- **Consistent Experience** - Same UI components used in Karrio dashboard
- **Self-Hosted** - All assets served from user's Karrio instance

---

## 2. Problem Statement

### 2.1 Current Limitations

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CURRENT ARCHITECTURE ISSUES                              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 1: Tight Coupling with Next.js App Structure                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Current components rely on:                                                    │
│    - next-auth/react for session management                                     │
│    - Next.js routing (useRouter, useSearchParams)                              │
│    - Server-side session validation                                             │
│    - App-specific context providers                                             │
│                                                                                 │
│  This makes components unusable outside the Karrio dashboard                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 2: No Embeddable Distribution                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Current state:                                                                 │
│    - karriojs only provides REST API client                                     │
│    - No pre-built UI components for embedding                                   │
│    - Developers must rebuild entire dashboard features                          │
│    - No CDN or static distribution of components                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  PROBLEM 3: Authentication Complexity                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Current auth flow:                                                             │
│    ClientProvider → useSyncedSession → getSession (next-auth)                  │
│                   → session.accessToken → API headers                           │
│                                                                                 │
│  This requires:                                                                 │
│    - Full next-auth setup                                                       │
│    - Cookie-based session management                                            │
│    - Complex provider hierarchy                                                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 User Stories

1. **As a developer**, I want to embed Karrio DevTools in my admin dashboard to monitor shipping API activity without leaving my application.

2. **As a platform operator**, I want to provide my merchants with an embedded rate sheet editor so they can configure custom rates within my platform.

3. **As an e-commerce developer**, I want to embed a document template editor so my users can customize packing slips without accessing the full Karrio dashboard.

---

## 3. Goals & Success Criteria

### 3.1 Primary Goals

| Goal | Description | Success Metric |
|------|-------------|----------------|
| **Decoupled Components** | Remove Next.js/next-auth dependencies | Components work in vanilla HTML page |
| **Simple Integration** | < 10 lines of code to embed a component | Developer satisfaction score > 4/5 |
| **Secure Isolation** | Iframe sandbox with postMessage communication | Zero XSS vulnerabilities |
| **Themeable** | Support brand customization | All visual properties configurable |
| **Self-Contained** | Single script include, no external dependencies | Bundle size < 500KB gzipped |

### 3.2 Non-Goals (Out of Scope for v1)

- Mobile native SDKs (iOS/Android)
- Server-side rendering of embedded components
- Real-time collaborative editing
- Offline mode support

---

## 4. Architecture Overview

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           KARRIO ELEMENTS ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────┐
    │                         HOST APPLICATION                                  │
    │  ┌────────────────────────────────────────────────────────────────────┐  │
    │  │  <script src="https://api.example.com/static/karrio/elements.js"> │  │
    │  │                                                                    │  │
    │  │  const karrio = KarrioElements.init({                             │  │
    │  │    apiKey: 'pk_live_xxxxx',                                       │  │
    │  │    host: 'https://api.example.com',                               │  │
    │  │    appearance: { theme: 'light', primaryColor: '#0066FF' }        │  │
    │  │  });                                                               │  │
    │  │                                                                    │  │
    │  │  const devtools = karrio.create('devtools');                      │  │
    │  │  devtools.mount('#devtools-container');                           │  │
    │  └────────────────────────────────────────────────────────────────────┘  │
    │                                    │                                      │
    │                                    ▼                                      │
    │  ┌────────────────────────────────────────────────────────────────────┐  │
    │  │                    <div id="devtools-container">                   │  │
    │  │  ┌──────────────────────────────────────────────────────────────┐  │  │
    │  │  │                    <iframe sandbox>                          │  │  │
    │  │  │  ┌────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  │              KARRIO DEVTOOLS COMPONENT                 │  │  │  │
    │  │  │  │  ┌──────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  │  │  KarrioEmbedProvider (API key auth)              │  │  │  │  │
    │  │  │  │  │    └── QueryClientProvider                       │  │  │  │  │
    │  │  │  │  │          └── DeveloperToolsDrawer               │  │  │  │  │
    │  │  │  │  └──────────────────────────────────────────────────┘  │  │  │  │
    │  │  │  └────────────────────────────────────────────────────────┘  │  │  │
    │  │  └──────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │ postMessage + REST API
                                         ▼
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                          KARRIO SERVER                                    │
    │  ┌────────────────────────────────────────────────────────────────────┐  │
    │  │  /static/karrio/elements/                                          │  │
    │  │    ├── elements.js           (main bundle)                         │  │
    │  │    ├── elements.css          (base styles)                         │  │
    │  │    ├── devtools.html         (iframe content)                      │  │
    │  │    ├── ratesheet.html        (iframe content)                      │  │
    │  │    └── template-editor.html  (iframe content)                      │  │
    │  └────────────────────────────────────────────────────────────────────┘  │
    │  ┌────────────────────────────────────────────────────────────────────┐  │
    │  │  API Endpoints (authenticated via API key)                         │  │
    │  │    ├── /graphql (primary - all CRUD operations)                    │  │
    │  │    │     ├── logs, events queries                                  │  │
    │  │    │     ├── webhooks queries & mutations                          │  │
    │  │    │     ├── connections queries & mutations                       │  │
    │  │    │     ├── rate_sheets queries & mutations                       │  │
    │  │    │     └── document_templates queries & mutations                │  │
    │  │    ├── /v1/references (carrier metadata, connection fields)        │  │
    │  │    └── /v1/carriers (carrier capabilities, services, options)      │  │
    │  └────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Communication Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         IFRAME COMMUNICATION PROTOCOL                            │
└─────────────────────────────────────────────────────────────────────────────────┘

    Host Application                    Iframe (Element)                 Karrio API
          │                                   │                              │
          │  1. Create element instance       │                              │
          │────────────────────────────────>  │                              │
          │                                   │                              │
          │  2. Mount to container            │                              │
          │────────────────────────────────>  │                              │
          │                                   │                              │
          │  3. postMessage: INIT             │                              │
          │  { apiKey, host, appearance }     │                              │
          │────────────────────────────────>  │                              │
          │                                   │                              │
          │                                   │  4. Fetch data               │
          │                                   │  Authorization: Token xxx    │
          │                                   │─────────────────────────────>│
          │                                   │                              │
          │                                   │  5. Return data              │
          │                                   │<─────────────────────────────│
          │                                   │                              │
          │  6. postMessage: LOADED           │                              │
          │<────────────────────────────────  │                              │
          │                                   │                              │
          │  7. postMessage: RESIZE           │                              │
          │  { height: 450 }                  │                              │
          │<────────────────────────────────  │                              │
          │                                   │                              │
          │  8. User interaction              │                              │
          │                                   │  9. API mutation             │
          │                                   │─────────────────────────────>│
          │                                   │                              │
          │  10. postMessage: EVENT           │                              │
          │  { type: 'save', data: {...} }   │                              │
          │<────────────────────────────────  │                              │
          │                                   │                              │
```

---

## 5. Component Design

### 5.1 DevTools Element

**Purpose**: Provide visibility into API activity, logs, events, webhooks, and API keys.

**Features**:
- API Logs viewer with filtering
- Event stream with detail view
- Webhook management (create, edit, delete, test)
- API Keys management
- Apps/OAuth configuration

**API Strategy (GraphQL-first)**:
- **GraphQL** for all data: `logs`, `events`, `webhooks`, `api_keys` queries and webhook mutations

**Existing Code to Reuse**:
- `packages/developers/components/developer-tools-drawer.tsx`
- `packages/developers/components/views/*`
- `packages/developers/context/developer-tools-context.tsx`
- `packages/hooks/log.ts`, `packages/hooks/event.ts`, `packages/hooks/webhook.ts`

```typescript
// Usage Example
const devtools = karrio.create('devtools', {
  defaultView: 'logs',  // 'logs' | 'events' | 'webhooks' | 'api-keys' | 'apps'
  features: {
    logs: true,
    events: true,
    webhooks: true,
    apiKeys: false,  // disable for restricted access
    apps: false,
  }
});

devtools.on('webhook.created', (webhook) => {
  console.log('Webhook created:', webhook);
});

devtools.mount('#devtools');
```

### 5.2 RateSheet Editor Element

**Purpose**: Visual interface for creating and editing carrier rate sheets.

**Features**:
- Service-level configuration
- Zone-based pricing matrix
- Surcharge management
- Carrier defaults loading
- Real-time validation

**API Strategy (GraphQL-first)**:
- **GraphQL** for all CRUD: `rate_sheet`, `rate_sheets` queries and `create_rate_sheet`, `update_rate_sheet` mutations
- **REST** for metadata:
  - `/v1/references` (carriers list)
  - `/v1/carriers/{carrier_name}/services` (carrier services)
  - `/v1/carriers/{carrier_name}/options` (carrier options)

**Existing Code to Reuse**:
- `packages/ui/components/rate-sheet-editor.tsx`
- `packages/ui/components/rate-sheet-table.tsx`
- `packages/ui/components/zones-tab.tsx`
- `packages/ui/components/services-tab.tsx`
- `packages/ui/components/surcharges-tab.tsx`
- `packages/hooks/rate-sheet.ts`

```typescript
// Usage Example
const ratesheet = karrio.create('ratesheet-editor', {
  rateSheetId: 'rsh_xxxxx',  // or 'new' for creation
  carrier: 'fedex',          // pre-select carrier for new sheets
  onSave: (rateSheet) => {
    console.log('Rate sheet saved:', rateSheet);
  },
  onClose: () => {
    console.log('Editor closed');
  }
});

ratesheet.mount('#ratesheet-container');
```

### 5.3 Document Template Editor Element

**Purpose**: HTML template editor for creating custom shipping documents.

**Features**:
- Code editor with syntax highlighting
- Live preview with sample data
- Template variables reference
- Metadata configuration
- PDF generation preview

**API Strategy (GraphQL-first)**:
- **GraphQL** for all CRUD: `document_template`, `document_templates` queries and `create_document_template`, `update_document_template` mutations

**Existing Code to Reuse**:
- `packages/ui/components/template-editor.tsx`
- `packages/hooks/document-template.ts`

```typescript
// Usage Example
const templateEditor = karrio.create('template-editor', {
  templateId: 'tpl_xxxxx',  // or 'new' for creation
  relatedObject: 'shipment', // 'shipment' | 'order'
  onSave: (template) => {
    console.log('Template saved:', template);
  }
});

templateEditor.mount('#template-container');
```

### 5.4 Carrier Connection Editor Element

**Purpose**: Full-featured carrier account registration and connection management interface.

**Features**:
- Carrier selection from all supported carriers
- Dynamic credential form generation based on carrier requirements
- OAuth quick-connect for supported carriers (e.g., FedEx, UPS)
- Carrier webhook registration/deregistration
- Connection configuration (services, options, colors)
- Metadata management
- Connection activation/deactivation
- Integration status display

**API Strategy (GraphQL-first)**:
- **GraphQL** for all CRUD operations: `user_connections`, `system_carrier_connections` queries and `create_carrier_connection`, `update_carrier_connection`, `delete_mutation` mutations
- **REST** for metadata:
  - `/v1/references` (connection_fields, connection_configs, carriers list)
  - `/v1/carriers` (carrier capabilities, services, options)
  - OAuth initiation flows

**Existing Code to Reuse**:
- `packages/ui/components/carrier-connection-dialog.tsx` (newer shadcn-based)
- `packages/ui/core/modals/connect-provider-modal.tsx` (legacy Bulma-based)
- `packages/hooks/carrier-connections.ts` (OAuth, webhook hooks)
- `packages/hooks/user-connection.ts` (GraphQL queries/mutations)

```typescript
// Usage Example
const connectionEditor = karrio.create('connection-editor', {
  connectionId: 'conn_xxxxx',  // or 'new' for creation
  carrier: 'fedex',            // pre-select carrier for new connections
  mode: 'dialog',              // 'dialog' | 'inline' | 'fullscreen'
  features: {
    oauth: true,               // enable OAuth quick connect
    webhook: true,             // enable webhook management
    metadata: true,            // enable metadata editing
    config: true,              // enable advanced configuration
  },
  onSave: (connection) => {
    console.log('Connection saved:', connection);
  },
  onClose: () => {
    console.log('Editor closed');
  },
  onOAuthSuccess: (credentials) => {
    console.log('OAuth completed:', credentials);
  }
});

connectionEditor.on('connection.created', (data) => {
  console.log('New connection:', data);
});

connectionEditor.on('connection.updated', (data) => {
  console.log('Connection updated:', data);
});

connectionEditor.on('webhook.registered', (data) => {
  console.log('Webhook registered:', data);
});

connectionEditor.mount('#connection-container');
```

**Connection List Mode** (optional):
```typescript
// For displaying a list of connections with edit/delete capabilities
const connectionManager = karrio.create('connection-manager', {
  mode: 'list',                // 'list' | 'grid' | 'compact'
  allowCreate: true,           // show "Add Connection" button
  allowDelete: true,           // enable deletion
  allowEdit: true,             // enable editing
  carriers: ['fedex', 'ups', 'usps'],  // filter by carriers (optional)
  onSelect: (connection) => {
    console.log('Connection selected:', connection);
  }
});

connectionManager.mount('#connections-list');
```

---

## 6. Authentication Model

### 6.1 Public API Key Authentication

Unlike the current session-based auth, Karrio Elements uses a simpler API key model:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         API KEY AUTHENTICATION FLOW                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    Developer Dashboard                                            Embedded Component
          │                                                              │
          │  1. Create API Key with scopes:                             │
          │     - elements:read                                          │
          │     - elements:write                                         │
          │     - logs:read                                              │
          │     - rate_sheets:manage                                     │
          │     - templates:manage                                       │
          │                                                              │
          ▼                                                              │
    ┌──────────────┐                                                    │
    │ API Key:     │                                                    │
    │ pk_live_xxx  │                                                    │
    └──────────────┘                                                    │
          │                                                              │
          │  2. Pass API key to Elements                                │
          │─────────────────────────────────────────────────────────────>│
          │                                                              │
          │                                                              │
          │                                              3. All API calls│
          │                                              include header: │
          │                                              Authorization:  │
          │                                              Token pk_live_x │
          │                                                              │
```

### 6.2 API Key Scopes

| Scope | Description | Elements |
|-------|-------------|----------|
| `elements:read` | Basic read access for embedded components | All |
| `elements:write` | Write access for mutations | All |
| `logs:read` | Access to API logs | DevTools |
| `events:read` | Access to events | DevTools |
| `webhooks:manage` | Create/edit/delete webhooks | DevTools |
| `api_keys:read` | View API keys (not secrets) | DevTools |
| `rate_sheets:manage` | Full rate sheet access | RateSheet Editor |
| `templates:manage` | Full template access | Template Editor |
| `connections:read` | View carrier connections | Connection Editor |
| `connections:manage` | Create/edit/delete connections | Connection Editor |
| `oauth:initiate` | Initiate OAuth flows | Connection Editor |

### 6.3 KarrioEmbedProvider Implementation

Replaces the current `ClientProvider` + `useSyncedSession` pattern. **GraphQL is the primary API interface** for all embedded components - this provides a unified query interface, better type safety, and reduces the number of network requests through query batching.

```typescript
// packages/elements/src/providers/karrio-embed-provider.tsx

interface KarrioEmbedConfig {
  apiKey: string;
  host: string;
  testMode?: boolean;
  orgId?: string;
}

interface KarrioEmbedContextValue {
  graphql: GraphQLClient;      // Primary API interface for all CRUD operations
  rest: RestClient;            // Secondary - only for OAuth flows and references
  config: KarrioEmbedConfig;
}

const KarrioEmbedContext = React.createContext<KarrioEmbedContextValue | null>(null);

export function KarrioEmbedProvider({
  config,
  children
}: {
  config: KarrioEmbedConfig;
  children: React.ReactNode;
}) {
  const headers = useMemo(() => ({
    'Content-Type': 'application/json',
    'Authorization': `Token ${config.apiKey}`,
    ...(config.testMode ? { 'X-Test-Mode': 'true' } : {}),
    ...(config.orgId ? { 'X-Org-Id': config.orgId } : {}),
  }), [config]);

  // Primary API: GraphQL for all CRUD operations
  // - logs, events (queries)
  // - webhooks (queries & mutations)
  // - connections (queries & mutations)
  // - rate_sheets (queries & mutations)
  // - document_templates (queries & mutations)
  const graphql = useMemo(() => ({
    request: async <T,>(query: string, variables?: { variables?: any; data?: any }) => {
      const response = await fetch(`${config.host}/graphql/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ query, variables: variables?.variables || variables?.data }),
      });
      return response.json() as Promise<T>;
    }
  }), [config.host, headers]);

  // Secondary API: REST only for specific operations
  // - /v1/references (carrier metadata, connection fields)
  // - OAuth initiation flows
  const rest = useMemo(() => ({
    get: async <T,>(path: string) => {
      const response = await fetch(`${config.host}${path}`, { headers });
      return response.json() as Promise<T>;
    },
    post: async <T,>(path: string, body?: any) => {
      const response = await fetch(`${config.host}${path}`, {
        method: 'POST',
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
      return response.json() as Promise<T>;
    }
  }), [config.host, headers]);

  return (
    <KarrioEmbedContext.Provider value={{ graphql, rest, config }}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </KarrioEmbedContext.Provider>
  );
}

export function useKarrioEmbed() {
  const context = useContext(KarrioEmbedContext);
  if (!context) {
    throw new Error('useKarrioEmbed must be used within KarrioEmbedProvider');
  }
  return context;
}

// Helper hook for GraphQL queries (primary usage)
export function useGraphQL() {
  const { graphql } = useKarrioEmbed();
  return graphql;
}
```

---

## 7. Implementation Plan

### 7.1 Phase 1: Foundation (Week 1-2)

#### Task 1.1: Create `@karrio/elements` Package Structure

```
packages/elements/
├── package.json
├── tsconfig.json
├── rollup.config.js
├── src/
│   ├── index.ts                    # Main entry point
│   ├── karrio-elements.ts          # KarrioElements class
│   ├── providers/
│   │   └── karrio-embed-provider.tsx
│   ├── components/
│   │   ├── devtools/
│   │   │   ├── index.tsx
│   │   │   └── DevToolsElement.tsx
│   │   ├── ratesheet/
│   │   │   ├── index.tsx
│   │   │   └── RateSheetElement.tsx
│   │   ├── template/
│   │   │   ├── index.tsx
│   │   │   └── TemplateElement.tsx
│   │   └── connection/
│   │       ├── index.tsx
│   │       └── ConnectionElement.tsx
│   ├── iframe/
│   │   ├── host.ts                 # Host-side iframe manager
│   │   ├── client.ts               # Iframe-side message handler
│   │   └── types.ts                # Message type definitions
│   ├── appearance/
│   │   ├── types.ts
│   │   └── apply-appearance.ts
│   └── utils/
│       └── index.ts
└── static/                         # HTML files for iframes
    ├── devtools.html
    ├── ratesheet.html
    ├── template-editor.html
    └── connection-editor.html
```

#### Task 1.2: Implement Iframe Communication Layer

```typescript
// src/iframe/types.ts
export type MessageType =
  | 'INIT'
  | 'LOADED'
  | 'ERROR'
  | 'RESIZE'
  | 'EVENT'
  | 'UPDATE_APPEARANCE';

export interface ElementMessage<T = any> {
  type: MessageType;
  elementId: string;
  payload: T;
}

// src/iframe/host.ts
export class IframeHost {
  private iframe: HTMLIFrameElement;
  private elementId: string;
  private listeners: Map<string, Function[]> = new Map();

  constructor(containerId: string, iframeSrc: string, elementId: string) {
    this.elementId = elementId;
    this.iframe = document.createElement('iframe');
    this.iframe.src = iframeSrc;
    this.iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms');
    this.iframe.style.cssText = 'border: none; width: 100%;';

    const container = document.getElementById(containerId);
    if (container) {
      container.appendChild(this.iframe);
    }

    window.addEventListener('message', this.handleMessage.bind(this));
  }

  private handleMessage(event: MessageEvent<ElementMessage>) {
    if (event.data.elementId !== this.elementId) return;

    switch (event.data.type) {
      case 'LOADED':
        this.emit('ready');
        break;
      case 'RESIZE':
        this.iframe.style.height = `${event.data.payload.height}px`;
        break;
      case 'EVENT':
        this.emit(event.data.payload.type, event.data.payload.data);
        break;
    }
  }

  send(type: MessageType, payload: any) {
    this.iframe.contentWindow?.postMessage(
      { type, elementId: this.elementId, payload },
      '*'
    );
  }

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }

  private emit(event: string, data?: any) {
    this.listeners.get(event)?.forEach(cb => cb(data));
  }

  destroy() {
    window.removeEventListener('message', this.handleMessage.bind(this));
    this.iframe.remove();
  }
}
```

#### Task 1.3: Create KarrioElements Main Class

```typescript
// src/karrio-elements.ts
import { IframeHost } from './iframe/host';

export interface KarrioElementsConfig {
  apiKey: string;
  host: string;
  testMode?: boolean;
  orgId?: string;
  appearance?: AppearanceConfig;
}

export interface AppearanceConfig {
  theme?: 'light' | 'dark' | 'system';
  variables?: {
    colorPrimary?: string;
    colorBackground?: string;
    colorText?: string;
    colorBorder?: string;
    fontFamily?: string;
    borderRadius?: string;
    spacingUnit?: string;
  };
}

export class KarrioElements {
  private config: KarrioElementsConfig;
  private elements: Map<string, IframeHost> = new Map();

  constructor(config: KarrioElementsConfig) {
    this.config = config;
  }

  static init(config: KarrioElementsConfig): KarrioElements {
    return new KarrioElements(config);
  }

  create(
    elementType: 'devtools' | 'ratesheet-editor' | 'template-editor' | 'connection-editor',
    options?: Record<string, any>
  ): Element {
    const elementId = `karrio-${elementType}-${Date.now()}`;
    const iframeSrc = `${this.config.host}/static/karrio/elements/${elementType}.html`;

    return {
      mount: (containerId: string) => {
        const host = new IframeHost(containerId, iframeSrc, elementId);
        this.elements.set(elementId, host);

        // Send initialization once iframe loads
        host.on('ready', () => {
          host.send('INIT', {
            ...this.config,
            options,
          });
        });

        return host;
      },
      unmount: () => {
        const host = this.elements.get(elementId);
        if (host) {
          host.destroy();
          this.elements.delete(elementId);
        }
      },
      on: (event: string, callback: Function) => {
        const host = this.elements.get(elementId);
        host?.on(event, callback);
      },
      update: (options: Record<string, any>) => {
        const host = this.elements.get(elementId);
        host?.send('UPDATE_OPTIONS', options);
      }
    };
  }

  updateAppearance(appearance: AppearanceConfig) {
    this.config.appearance = { ...this.config.appearance, ...appearance };
    this.elements.forEach(host => {
      host.send('UPDATE_APPEARANCE', this.config.appearance);
    });
  }
}

// Global export for script tag usage
if (typeof window !== 'undefined') {
  (window as any).KarrioElements = KarrioElements;
}
```

### 7.2 Phase 2: Refactor Hooks & Components (Week 2-3)

#### Task 2.1: Create Decoupled `useKarrioEmbed` Hook

Refactor the existing `useKarrio` hook to work without next-auth:

```typescript
// packages/elements/src/hooks/use-karrio-embed.ts

import { useContext, useMemo } from 'react';
import { KarrioEmbedContext } from '../providers/karrio-embed-provider';

export function useKarrioEmbed() {
  const context = useContext(KarrioEmbedContext);

  if (!context) {
    throw new Error('useKarrioEmbed must be used within KarrioEmbedProvider');
  }

  return context;
}

// Replacement for useAuthenticatedQuery that works with API key
export function useEmbedQuery<T>(options: {
  queryKey: any[];
  queryFn: () => Promise<T>;
  enabled?: boolean;
  staleTime?: number;
}) {
  // Direct query without auth checks - API key is always present
  return useQuery({
    ...options,
    enabled: options.enabled ?? true,
  });
}
```

#### Task 2.2: Create Element-Specific Wrappers

Wrap existing components to work within iframe context:

```typescript
// packages/elements/src/components/devtools/DevToolsElement.tsx

import { KarrioEmbedProvider } from '../../providers/karrio-embed-provider';
import { DeveloperToolsProvider, DeveloperToolsDrawer } from '@karrio/developers';
import { useIframeClient } from '../../iframe/client';

interface DevToolsElementProps {
  config: KarrioEmbedConfig;
  options?: {
    defaultView?: string;
    features?: Record<string, boolean>;
  };
}

export function DevToolsElement({ config, options }: DevToolsElementProps) {
  const iframe = useIframeClient();

  // Notify parent of events
  const handleEvent = (type: string, data: any) => {
    iframe.send('EVENT', { type, data });
  };

  return (
    <KarrioEmbedProvider config={config}>
      <DeveloperToolsProvider
        defaultView={options?.defaultView}
        features={options?.features}
        onEvent={handleEvent}
      >
        <DeveloperToolsDrawer standalone />
      </DeveloperToolsProvider>
    </KarrioEmbedProvider>
  );
}
```

#### Task 2.3: Refactor Rate Sheet Editor for Embedding

```typescript
// packages/elements/src/components/ratesheet/RateSheetElement.tsx

import { KarrioEmbedProvider } from '../../providers/karrio-embed-provider';
import { RateSheetEditor } from '@karrio/ui/components/rate-sheet-editor';
import { useRateSheet, useRateSheetMutation } from '@karrio/hooks/rate-sheet';
import { useIframeClient } from '../../iframe/client';

interface RateSheetElementProps {
  config: KarrioEmbedConfig;
  options?: {
    rateSheetId?: string;
    carrier?: string;
    connectionId?: string;
  };
}

export function RateSheetElement({ config, options }: RateSheetElementProps) {
  const iframe = useIframeClient();

  const handleClose = () => {
    iframe.send('EVENT', { type: 'close' });
  };

  const handleSave = (rateSheet: any) => {
    iframe.send('EVENT', { type: 'save', data: rateSheet });
  };

  return (
    <KarrioEmbedProvider config={config}>
      <RateSheetEditor
        rateSheetId={options?.rateSheetId || 'new'}
        preloadCarrier={options?.carrier}
        linkConnectionId={options?.connectionId}
        onClose={handleClose}
        useRateSheet={useRateSheet}
        useRateSheetMutation={useRateSheetMutation}
      />
    </KarrioEmbedProvider>
  );
}
```

### 7.3 Phase 3: Build & Static Deployment (Week 3-4)

#### Task 3.1: Configure Rollup Build

```javascript
// packages/elements/rollup.config.js

import typescript from '@rollup/plugin-typescript';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import replace from '@rollup/plugin-replace';
import terser from '@rollup/plugin-terser';
import postcss from 'rollup-plugin-postcss';

const production = !process.env.ROLLUP_WATCH;

export default [
  // Main bundle (for host page)
  {
    input: 'src/index.ts',
    output: {
      file: 'dist/elements.js',
      format: 'iife',
      name: 'KarrioElements',
      sourcemap: true,
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      typescript({ tsconfig: './tsconfig.json' }),
      production && terser(),
    ],
  },
  // DevTools iframe bundle
  {
    input: 'src/components/devtools/iframe-entry.tsx',
    output: {
      file: 'dist/devtools-bundle.js',
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      typescript({ tsconfig: './tsconfig.json' }),
      postcss({ extract: 'devtools.css', minimize: production }),
      replace({
        'process.env.NODE_ENV': JSON.stringify(production ? 'production' : 'development'),
        preventAssignment: true,
      }),
      production && terser(),
    ],
  },
  // RateSheet iframe bundle
  {
    input: 'src/components/ratesheet/iframe-entry.tsx',
    output: {
      file: 'dist/ratesheet-bundle.js',
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      // ... same as devtools
    ],
  },
  // Template Editor iframe bundle
  {
    input: 'src/components/template/iframe-entry.tsx',
    output: {
      file: 'dist/template-bundle.js',
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      // ... same as devtools
    ],
  },
  // Connection Editor iframe bundle
  {
    input: 'src/components/connection/iframe-entry.tsx',
    output: {
      file: 'dist/connection-bundle.js',
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      // ... same as devtools
    ],
  },
];
```

#### Task 3.2: Create Static HTML Files for Iframes

```html
<!-- packages/elements/static/devtools.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Karrio DevTools</title>
  <link rel="stylesheet" href="./devtools.css">
  <style>
    html, body, #root {
      margin: 0;
      padding: 0;
      height: 100%;
      width: 100%;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script src="./devtools-bundle.js"></script>
</body>
</html>
```

#### Task 3.3: Update Build Script

```bash
# bin/build-elements
#!/usr/bin/env bash

source "bin/activate-env" >/dev/null 2>&1

cd "${ROOT:?}/packages/elements"

echo "Building Karrio Elements..."

# Clean previous build
rm -rf dist

# Build bundles
npm run build

# Copy static HTML files
cp -r static/* dist/

# Copy to Django static directory
mkdir -p "${ROOT:?}/apps/api/karrio/server/static/karrio/elements"
cp -r dist/* "${ROOT:?}/apps/api/karrio/server/static/karrio/elements/"

echo "Collecting static files..."
karrio collectstatic --noinput >/dev/null 2>&1

echo "✓ Karrio Elements built successfully!"
```

---

## 8. Package Structure

### 8.1 Final Directory Structure

```
packages/
├── elements/                        # NEW: Karrio Elements package
│   ├── package.json
│   ├── tsconfig.json
│   ├── rollup.config.js
│   ├── src/
│   │   ├── index.ts
│   │   ├── karrio-elements.ts
│   │   ├── providers/
│   │   │   ├── karrio-embed-provider.tsx
│   │   │   └── index.ts
│   │   ├── components/
│   │   │   ├── devtools/
│   │   │   │   ├── DevToolsElement.tsx
│   │   │   │   ├── iframe-entry.tsx
│   │   │   │   └── index.ts
│   │   │   ├── ratesheet/
│   │   │   │   ├── RateSheetElement.tsx
│   │   │   │   ├── iframe-entry.tsx
│   │   │   │   └── index.ts
│   │   │   ├── template/
│   │   │   │   ├── TemplateElement.tsx
│   │   │   │   ├── iframe-entry.tsx
│   │   │   │   └── index.ts
│   │   │   └── connection/
│   │   │       ├── ConnectionElement.tsx
│   │   │       ├── iframe-entry.tsx
│   │   │       └── index.ts
│   │   ├── iframe/
│   │   │   ├── host.ts
│   │   │   ├── client.ts
│   │   │   └── types.ts
│   │   ├── appearance/
│   │   │   ├── types.ts
│   │   │   ├── variables.ts
│   │   │   └── apply-appearance.ts
│   │   └── hooks/
│   │       ├── use-karrio-embed.ts
│   │       ├── use-embed-query.ts
│   │       └── index.ts
│   └── static/
│       ├── devtools.html
│       ├── ratesheet.html
│       ├── template-editor.html
│       └── connection-editor.html
│
├── hooks/
│   ├── karrio.tsx                   # MODIFIED: Extract reusable parts
│   └── ...
│
├── ui/
│   └── components/
│       ├── rate-sheet-editor.tsx       # MODIFIED: Accept injected hooks
│       ├── template-editor.tsx         # MODIFIED: Accept injected hooks
│       └── carrier-connection-dialog.tsx # MODIFIED: Add standalone mode
│
└── developers/
    └── components/
        └── developer-tools-drawer.tsx  # MODIFIED: Add standalone mode
```

### 8.2 Package.json

```json
{
  "name": "@karrio/elements",
  "version": "0.1.0",
  "description": "Karrio Elements - Embeddable UI Components",
  "main": "dist/elements.js",
  "module": "dist/elements.esm.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "rollup -c",
    "watch": "rollup -c -w",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@karrio/hooks": "workspace:*",
    "@karrio/ui": "workspace:*",
    "@karrio/developers": "workspace:*",
    "@karrio/types": "workspace:*",
    "@karrio/lib": "workspace:*",
    "@tanstack/react-query": "^4.36.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@rollup/plugin-commonjs": "^25.0.0",
    "@rollup/plugin-node-resolve": "^15.0.0",
    "@rollup/plugin-replace": "^5.0.0",
    "@rollup/plugin-terser": "^0.4.0",
    "@rollup/plugin-typescript": "^11.0.0",
    "rollup": "^4.0.0",
    "rollup-plugin-postcss": "^4.0.0",
    "typescript": "^5.0.0"
  },
  "peerDependencies": {
    "react": ">=18.0.0",
    "react-dom": ">=18.0.0"
  }
}
```

---

## 9. API Design

### 9.1 JavaScript API

```typescript
// Initialize KarrioElements
const karrio = KarrioElements.init({
  apiKey: 'pk_live_xxxxx',          // Required: API key with elements scopes
  host: 'https://api.example.com',   // Required: Karrio server URL
  testMode: false,                   // Optional: Use test mode
  orgId: 'org_xxxxx',               // Optional: Organization ID for multi-org
  appearance: {                      // Optional: Theming
    theme: 'light',
    variables: {
      colorPrimary: '#0066FF',
      fontFamily: 'Inter, sans-serif',
    }
  }
});

// Create DevTools element
const devtools = karrio.create('devtools', {
  defaultView: 'logs',
  features: {
    logs: true,
    events: true,
    webhooks: true,
    apiKeys: true,
    apps: true,
  }
});

// Event listeners
devtools.on('ready', () => console.log('DevTools loaded'));
devtools.on('webhook.created', (data) => console.log('Webhook created:', data));
devtools.on('error', (error) => console.error('Error:', error));

// Mount to DOM
devtools.mount('#devtools-container');

// Later: Unmount
devtools.unmount();

// Create RateSheet Editor
const ratesheet = karrio.create('ratesheet-editor', {
  rateSheetId: 'new',        // or existing ID
  carrier: 'fedex',
});

ratesheet.on('save', (data) => console.log('Saved:', data));
ratesheet.on('close', () => console.log('Closed'));
ratesheet.mount('#ratesheet-container');

// Create Template Editor
const template = karrio.create('template-editor', {
  templateId: 'new',
  relatedObject: 'shipment',
});

template.on('save', (data) => console.log('Saved:', data));
template.mount('#template-container');

// Update appearance globally
karrio.updateAppearance({
  theme: 'dark',
});
```

### 9.2 HTML/Script Tag Usage

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Shipping Dashboard</title>
  <script src="https://api.example.com/static/karrio/elements/elements.js"></script>
</head>
<body>
  <h1>Shipping DevTools</h1>
  <div id="devtools" style="height: 600px;"></div>

  <script>
    const karrio = KarrioElements.init({
      apiKey: 'pk_live_xxxxx',
      host: 'https://api.example.com',
    });

    const devtools = karrio.create('devtools');
    devtools.mount('#devtools');
  </script>
</body>
</html>
```

### 9.3 Appearance Variables

```typescript
interface AppearanceVariables {
  // Colors
  colorPrimary: string;           // Primary brand color
  colorPrimaryHover: string;      // Primary hover state
  colorBackground: string;        // Page background
  colorSurface: string;           // Card/panel background
  colorText: string;              // Primary text color
  colorTextSecondary: string;     // Secondary text color
  colorBorder: string;            // Border color
  colorError: string;             // Error state color
  colorSuccess: string;           // Success state color
  colorWarning: string;           // Warning state color

  // Typography
  fontFamily: string;             // Font family
  fontSizeBase: string;           // Base font size (default: 14px)
  fontWeightNormal: number;       // Normal weight (default: 400)
  fontWeightMedium: number;       // Medium weight (default: 500)
  fontWeightBold: number;         // Bold weight (default: 600)

  // Spacing
  spacingUnit: string;            // Base spacing unit (default: 4px)
  spacingXs: string;              // Extra small (default: 4px)
  spacingSm: string;              // Small (default: 8px)
  spacingMd: string;              // Medium (default: 16px)
  spacingLg: string;              // Large (default: 24px)
  spacingXl: string;              // Extra large (default: 32px)

  // Border & Radius
  borderRadius: string;           // Default border radius
  borderRadiusSm: string;         // Small radius
  borderRadiusLg: string;         // Large radius
  borderWidth: string;            // Border width

  // Shadows
  shadowSm: string;               // Small shadow
  shadowMd: string;               // Medium shadow
  shadowLg: string;               // Large shadow
}
```

---

## 10. Build & Deployment

### 10.1 Build Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BUILD PIPELINE                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

    Source Files                    Build Process                    Output
    ────────────                    ─────────────                    ──────

    packages/elements/
    └── src/
        ├── index.ts ─────────────► Rollup (IIFE) ──────────────► dist/elements.js
        │                                                           (host bundle)
        │
        ├── components/
        │   ├── devtools/
        │   │   └── iframe-entry.tsx ► Rollup + PostCSS ──────► dist/devtools-bundle.js
        │   │                                                   dist/devtools.css
        │   │
        │   ├── ratesheet/
        │   │   └── iframe-entry.tsx ► Rollup + PostCSS ──────► dist/ratesheet-bundle.js
        │   │                                                   dist/ratesheet.css
        │   │
        │   ├── template/
        │   │   └── iframe-entry.tsx ► Rollup + PostCSS ──────► dist/template-bundle.js
        │   │                                                   dist/template.css
        │   │
        │   └── connection/
        │       └── iframe-entry.tsx ► Rollup + PostCSS ──────► dist/connection-bundle.js
        │                                                       dist/connection.css
        │
        └── static/
            ├── devtools.html ────────────────────────────────► dist/devtools.html
            ├── ratesheet.html ───────────────────────────────► dist/ratesheet.html
            ├── template-editor.html ─────────────────────────► dist/template-editor.html
            └── connection-editor.html ───────────────────────► dist/connection-editor.html

                                         │
                                         ▼

    apps/api/karrio/server/static/karrio/elements/
    ├── elements.js              ◄── collectstatic
    ├── devtools.html
    ├── devtools-bundle.js
    ├── devtools.css
    ├── ratesheet.html
    ├── ratesheet-bundle.js
    ├── ratesheet.css
    ├── template-editor.html
    ├── template-bundle.js
    ├── template.css
    ├── connection-editor.html
    ├── connection-bundle.js
    └── connection.css
```

### 10.2 Server Configuration

Update Django settings to serve elements static files:

```python
# apps/api/karrio/server/settings/base.py

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add CORS headers for iframe embedding
CORS_ALLOWED_ORIGINS = getattr(settings, 'CORS_ALLOWED_ORIGINS', ['*'])

# CSP headers for elements
CSP_FRAME_ANCESTORS = ["'self'", "*"]  # Allow embedding from any origin
```

### 10.3 Integration with bin/server

Add to existing `bin/server` script:

```bash
elif [[ "$*" == *build:elements* ]]; then
    cd "${ROOT:?}/packages/elements"

    echo "Building Karrio Elements..."

    # Clean previous build
    rm -rf dist

    # Install dependencies if needed
    npm install

    # Build all bundles
    npm run build

    # Copy static HTML files
    cp -r static/* dist/

    # Copy to Django static directory
    mkdir -p "${ROOT:?}/apps/api/karrio/server/static/karrio/elements"
    cp -r dist/* "${ROOT:?}/apps/api/karrio/server/static/karrio/elements/"

    cd -

    # Collect static files
    karrio collectstatic --noinput >/dev/null 2>&1

    echo "✓ Karrio Elements built successfully!"
    echo ""
    echo "Files deployed to: /static/karrio/elements/"
    echo "  - elements.js (main bundle)"
    echo "  - devtools.html + devtools-bundle.js"
    echo "  - ratesheet.html + ratesheet-bundle.js"
    echo "  - template-editor.html + template-bundle.js"
    echo "  - connection-editor.html + connection-bundle.js"
```

---

## 11. Security Considerations

### 11.1 Iframe Sandbox

All embedded components run in sandboxed iframes with restricted permissions:

```html
<iframe
  src="..."
  sandbox="allow-scripts allow-same-origin allow-forms"
  referrerpolicy="strict-origin-when-cross-origin"
  allow="clipboard-write"
></iframe>
```

**Allowed capabilities**:
- `allow-scripts`: Execute JavaScript
- `allow-same-origin`: Access same-origin resources
- `allow-forms`: Submit forms

**Blocked capabilities**:
- `allow-top-navigation`: Cannot navigate parent window
- `allow-popups`: Cannot open new windows
- `allow-downloads`: Cannot initiate downloads

### 11.2 Message Validation

All postMessage communication validates origin and message structure:

```typescript
// In iframe client
window.addEventListener('message', (event) => {
  // Validate origin matches expected host
  if (!isValidOrigin(event.origin)) {
    console.warn('Rejected message from unknown origin:', event.origin);
    return;
  }

  // Validate message structure
  const message = event.data as ElementMessage;
  if (!message.type || !message.elementId) {
    console.warn('Rejected malformed message');
    return;
  }

  handleMessage(message);
});
```

### 11.3 API Key Scopes

Elements require specific API key scopes:

| Element | Required Scopes |
|---------|-----------------|
| DevTools | `logs:read`, `events:read`, `webhooks:manage` |
| RateSheet Editor | `rate_sheets:manage` |
| Template Editor | `templates:manage` |
| Connection Editor | `connections:manage`, `oauth:initiate` |

API keys without required scopes will receive 403 Forbidden errors.

### 11.4 Content Security Policy

Recommended CSP headers for pages embedding Karrio Elements:

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://your-karrio-server.com;
  frame-src https://your-karrio-server.com;
  connect-src https://your-karrio-server.com;
  style-src 'self' 'unsafe-inline';
```

---

## 12. Migration & Refactoring

### 12.1 Refactor `packages/hooks/karrio.tsx`

Extract authentication-agnostic parts:

```typescript
// packages/hooks/karrio-core.tsx (NEW)

// Core client setup without auth dependencies
export function setupKarrioClient(host: string, authHeader?: string): KarrioClient {
  const client = new KarrioClient({ basePath: url$`${host}` });

  if (authHeader) {
    client.axios.interceptors.request.use((config: any = { headers: {} }) => {
      config.headers = {
        ...config.headers,
        authorization: authHeader,
      };
      return config;
    });
  }

  return client;
}

// GraphQL request helper
export function createGraphQLClient(host: string, authHeader?: string) {
  return {
    request: async <T,>(query: string, variables?: any): Promise<T> => {
      const response = await fetch(`${host}/graphql/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authHeader ? { authorization: authHeader } : {}),
        },
        body: JSON.stringify({ query, variables }),
      });
      return response.json();
    }
  };
}
```

```typescript
// packages/hooks/karrio.tsx (MODIFIED)

import { setupKarrioClient, createGraphQLClient } from './karrio-core';

// Keep existing ClientProvider for Next.js app
export const ClientProvider = ({ children, ...pageData }: ClientProviderProps) => {
  const { getHost } = useAPIMetadata();
  const { query: sessionQuery, isAuthenticated } = useSyncedSession();
  const session = sessionQuery.data as ExtendedSessionType;

  const host = getHost?.() || KARRIO_API || "";
  const authHeader = session?.accessToken ? `Bearer ${session.accessToken}` : undefined;
  const client = setupKarrioClient(host, authHeader);

  // ... rest of implementation
};
```

### 12.2 Modify Component Props for Dependency Injection

Update components to accept hooks via props:

```typescript
// packages/ui/components/rate-sheet-editor.tsx (MODIFIED)

interface RateSheetEditorProps {
  rateSheetId: string;
  onClose: () => void;
  preloadCarrier?: string;
  linkConnectionId?: string;
  isAdmin?: boolean;
  // Injected hooks for framework independence
  useRateSheet: (args: any) => any;
  useRateSheetMutation: () => any;
}

export const RateSheetEditor = ({
  useRateSheet,
  useRateSheetMutation,
  ...props
}: RateSheetEditorProps) => {
  const { query } = useRateSheet({ id: props.rateSheetId });
  const mutations = useRateSheetMutation();
  // ... rest of implementation
};
```

### 12.3 Add Standalone Mode to DevTools

```typescript
// packages/developers/components/developer-tools-drawer.tsx (MODIFIED)

interface DeveloperToolsDrawerProps {
  standalone?: boolean;  // New prop for embedded mode
}

export function DeveloperToolsDrawer({ standalone = false }: DeveloperToolsDrawerProps) {
  // If standalone, render full page instead of drawer
  if (standalone) {
    return (
      <div className="h-full w-full overflow-auto">
        <DeveloperToolsContent />
      </div>
    );
  }

  // Existing drawer implementation
  return (
    <Sheet>
      <SheetContent>
        <DeveloperToolsContent />
      </SheetContent>
    </Sheet>
  );
}
```

---

## 13. Testing Strategy

### 13.1 Unit Tests

```typescript
// packages/elements/__tests__/karrio-elements.test.ts

describe('KarrioElements', () => {
  it('should initialize with config', () => {
    const karrio = KarrioElements.init({
      apiKey: 'pk_test_xxx',
      host: 'https://api.example.com',
    });

    expect(karrio).toBeInstanceOf(KarrioElements);
  });

  it('should create element instances', () => {
    const karrio = KarrioElements.init({ apiKey: 'pk_test_xxx', host: 'https://api.example.com' });
    const devtools = karrio.create('devtools');

    expect(devtools).toHaveProperty('mount');
    expect(devtools).toHaveProperty('unmount');
    expect(devtools).toHaveProperty('on');
  });
});
```

### 13.2 Integration Tests

```typescript
// packages/elements/__tests__/iframe-communication.test.ts

describe('Iframe Communication', () => {
  it('should send INIT message to iframe', async () => {
    const container = document.createElement('div');
    container.id = 'test-container';
    document.body.appendChild(container);

    const karrio = KarrioElements.init({
      apiKey: 'pk_test_xxx',
      host: 'http://localhost:5002',
    });

    const devtools = karrio.create('devtools');

    const readyPromise = new Promise(resolve => devtools.on('ready', resolve));
    devtools.mount('#test-container');

    await readyPromise;

    // Verify iframe was created
    const iframe = container.querySelector('iframe');
    expect(iframe).not.toBeNull();
  });
});
```

### 13.3 E2E Tests

```typescript
// packages/elements/__tests__/e2e/devtools.spec.ts

import { test, expect } from '@playwright/test';

test.describe('DevTools Element', () => {
  test('should load and display logs', async ({ page }) => {
    await page.goto('/test-page-with-elements.html');

    // Wait for iframe to load
    const iframe = page.frameLocator('#devtools-container iframe');

    // Check that logs view is visible
    await expect(iframe.locator('[data-testid="logs-view"]')).toBeVisible();

    // Check that logs are loaded
    await expect(iframe.locator('[data-testid="log-item"]')).toHaveCount.greaterThan(0);
  });
});
```

---

## 14. Rollout Plan

### 14.1 Phase 1: Alpha (Internal Testing)

**Duration**: 2 weeks

- Deploy to staging environment
- Internal team testing
- Gather feedback on API design
- Fix critical bugs

### 14.2 Phase 2: Beta (Limited Release)

**Duration**: 4 weeks

- Enable for select beta customers
- Monitor performance and errors
- Collect feedback on documentation
- Iterate on appearance API

### 14.3 Phase 3: General Availability

**Duration**: Ongoing

- Full documentation release
- Marketing announcement
- Support training
- Performance monitoring

### 14.4 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Integration Time | < 30 minutes | Developer survey |
| Bundle Size | < 500KB gzipped | Build output |
| Load Time | < 2 seconds | Lighthouse audit |
| Error Rate | < 0.1% | Sentry monitoring |
| Developer Satisfaction | > 4.0/5.0 | NPS survey |

---

## Appendix A: File Change Summary

### New Files

| File | Purpose |
|------|---------|
| `packages/elements/` | New package directory |
| `packages/elements/package.json` | Package configuration |
| `packages/elements/rollup.config.js` | Build configuration |
| `packages/elements/src/index.ts` | Main entry point |
| `packages/elements/src/karrio-elements.ts` | Main class |
| `packages/elements/src/providers/karrio-embed-provider.tsx` | Embedding provider |
| `packages/elements/src/iframe/host.ts` | Host-side iframe manager |
| `packages/elements/src/iframe/client.ts` | Iframe-side message handler |
| `packages/elements/src/components/devtools/` | DevTools element |
| `packages/elements/src/components/ratesheet/` | RateSheet element |
| `packages/elements/src/components/template/` | Template element |
| `packages/elements/src/components/connection/` | Connection element |
| `packages/elements/static/*.html` | Iframe HTML files |
| `bin/build-elements` | Build script |

### Modified Files

| File | Changes |
|------|---------|
| `packages/hooks/karrio.tsx` | Extract core client setup |
| `packages/ui/components/rate-sheet-editor.tsx` | Add hook injection props |
| `packages/ui/components/template-editor.tsx` | Add hook injection props |
| `packages/ui/components/carrier-connection-dialog.tsx` | Add standalone mode and hook injection |
| `packages/developers/components/developer-tools-drawer.tsx` | Add standalone mode |
| `bin/server` | Add `build:elements` command |

---

## Appendix B: API Key Scope Reference

```yaml
# API Key Scopes for Karrio Elements

elements:
  description: "Base scope for all embedded components"
  includes:
    - elements:read   # Read access to element configuration
    - elements:write  # Write access for mutations

devtools:
  description: "DevTools-specific scopes"
  includes:
    - logs:read       # View API logs
    - events:read     # View events
    - webhooks:read   # View webhooks
    - webhooks:write  # Create/update webhooks
    - webhooks:delete # Delete webhooks
    - api_keys:read   # View API keys (not secrets)

ratesheet:
  description: "RateSheet Editor scopes"
  includes:
    - rate_sheets:read   # View rate sheets
    - rate_sheets:write  # Create/update rate sheets
    - rate_sheets:delete # Delete rate sheets
    - carriers:read      # View carrier references

template:
  description: "Template Editor scopes"
  includes:
    - templates:read   # View document templates
    - templates:write  # Create/update templates
    - templates:delete # Delete templates
    - documents:generate # Generate document previews

connection:
  description: "Connection Editor scopes"
  includes:
    - connections:read     # View carrier connections
    - connections:write    # Create/update connections
    - connections:delete   # Delete connections
    - oauth:initiate       # Initiate OAuth authorization flows
    - carriers:read        # View carrier references and capabilities
```

---

## Appendix C: Quick Start Guide

### Installation

**Option 1: Script Tag**
```html
<script src="https://your-karrio-server.com/static/karrio/elements/elements.js"></script>
```

**Option 2: npm**
```bash
npm install @karrio/elements
```

### Basic Usage

```javascript
// Initialize
const karrio = KarrioElements.init({
  apiKey: 'pk_live_your_api_key',
  host: 'https://your-karrio-server.com',
});

// Create and mount DevTools
const devtools = karrio.create('devtools');
devtools.mount('#my-container');

// Listen for events
devtools.on('ready', () => console.log('DevTools loaded!'));

// Cleanup
devtools.unmount();
```

### React Integration

```jsx
import { useEffect, useRef } from 'react';

function KarrioDevTools({ apiKey, host }) {
  const containerRef = useRef(null);
  const elementRef = useRef(null);

  useEffect(() => {
    const karrio = KarrioElements.init({ apiKey, host });
    const devtools = karrio.create('devtools');

    devtools.mount(containerRef.current);
    elementRef.current = devtools;

    return () => devtools.unmount();
  }, [apiKey, host]);

  return <div ref={containerRef} style={{ height: '600px' }} />;
}
```

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-16 | Engineering Team | Initial draft |
| 1.1 | 2025-12-16 | Engineering Team | Added Carrier Connection Editor element |
| 1.2 | 2025-12-16 | Engineering Team | GraphQL-first API strategy, added /v1/carriers endpoint |
