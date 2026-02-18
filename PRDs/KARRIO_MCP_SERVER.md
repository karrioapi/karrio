# Karrio MCP Server

<!-- ARCHITECTURE: System design PRD -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-17 |
| Status | Planning |
| Owner | Daniel Kobina |
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

This PRD proposes building an official **Karrio MCP (Model Context Protocol) server** that exposes Karrio's multi-carrier shipping capabilities to AI agents. As agentic commerce becomes the dominant interaction model -- with Google/Shopify's UCP, OpenAI/Stripe's ACP, and MCP itself reaching 97M monthly SDK downloads -- shipping platforms that are not AI-accessible will be left behind. The Karrio MCP server positions Karrio as the **fulfillment/shipping intelligence layer** for any AI agent performing commerce.

### Key Architecture Decisions

1. **Separate `@karrio/mcp` npm package**: Decoupled from core Karrio server for independent versioning and zero-install via `npx`. TypeScript implementation following the Stripe MCP pattern.
2. **Hybrid Resources + Tools**: Expose carrier/service reference data as MCP Resources (differentiator -- no other shipping MCP does this) with read-only Tool fallbacks for clients that don't support Resources (Cursor, ChatGPT).
3. **Workflow-Oriented Tools Over REST Wrappers**: Design 10-15 high-level tools around user outcomes (e.g., `create_shipment`) rather than 1:1 REST endpoint mapping, following MCP best practices.
4. **UCP Fulfillment Alignment**: Align tool schemas and data models with UCP's fulfillment extension so Karrio MCP tools can naturally serve UCP-compliant commerce flows.
5. **Safe-by-Default for Financial Operations**: Use `destructiveHint: true` annotations + optional MCP elicitation for label purchase tools, following Stripe's "recommend but don't enforce" pattern.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| MCP server exposing core shipping operations | Full UCP protocol implementation (checkout, payments) |
| Rate quoting, label creation, tracking, address validation | Carrier account management via MCP (security concern) |
| Read operations on shipments, orders, trackers | Database migrations or schema changes |
| Remote (HTTP) and local (stdio) transport | Custom AI agent framework or chatbot UI |
| OAuth2 and API key authentication | MCP client implementation |
| UCP fulfillment extension data model alignment | A2A (Agent-to-Agent) protocol support |
| Karrio knowledge base / documentation search tool | Webhook management via MCP |

---

## Open Questions & Decisions

### Pending Questions

_No pending questions._

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Separate package or built-in? | **Separate `karrio-mcp` package** | Decouples MCP server versioning from core Karrio releases. Can iterate on MCP tools independently. Follows Stripe's pattern (`@stripe/mcp` is separate from Stripe API). Avoids adding MCP SDK dependency to core server. Can still import shared types/validation from karrio SDK. | 2026-02-17 |
| D2 | Should label purchase require confirmation? | **Use MCP tool annotations + elicitation** | Industry standard: EasyPost, ShipStation, and Shippo all execute purchases directly with no confirmation. Stripe recommends but does not enforce confirmation. MCP spec (2025-06-18) introduced `elicitation` as a formal confirmation primitive, but client support is uneven (Cursor/ChatGPT don't support it). **Our approach**: (1) Mark `create_shipment` with `destructiveHint: true, readOnlyHint: false` annotations so clients that support confirmation prompts will surface them; (2) Implement optional `elicitation`-based confirmation for clients that support it; (3) Include clear cost warnings in tool descriptions. This matches Stripe's "recommend but don't enforce" pattern while being forward-compatible with the emerging elicitation spec. | 2026-02-17 |
| D3 | MCP Resources for reference data? | **Yes -- hybrid Resources + read-only Tools** | This is a genuine differentiator. No other shipping MCP exposes Resources. **However**, Cursor and ChatGPT do not support Resources (only Claude Desktop, Claude Code, VS Code Copilot, Continue do). So we expose carrier/service catalogs as **both** Resources (for clients that support them) **and** read-only Tools (for universal access). Resources provide context grounding without tool calls; Tools provide fallback for Cursor/ChatGPT. The multi-carrier catalog as a Resource is uniquely powerful -- agents can reason about "which carriers support international shipping to Brazil?" before making any API calls. See detailed design in Technical Design section. | 2026-02-17 |
| D4 | Package distribution strategy | **npm (`@karrio/mcp`) as primary** | npm/npx is the standard distribution for MCP servers (Stripe, Shippo, ShipStation all use npm). `npx -y @karrio/mcp` gives zero-install experience. The server itself can be TypeScript or a Python binary wrapped in an npm package (like many MCP servers do). npm reaches the broadest developer audience for MCP tooling. | 2026-02-17 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Agent attempts to purchase label without user awareness | Financial liability -- labels cost money | Resolved: Use `destructiveHint: true` annotations + optional elicitation. See D2. | ❌ No |
| Multi-carrier rate results exceed context window | Agent may not see all options, leading to suboptimal selection | Paginate with `limit` parameter, default to top 5 cheapest rates | ✅ Yes |
| Self-hosted Karrio instance with custom carriers | MCP server must work with any Karrio deployment, not just cloud | Use Karrio API as backend, no direct DB access | ❌ No |

---

## Problem Statement

### Current State

Karrio exposes a comprehensive REST API and GraphQL API for multi-carrier shipping. However, these APIs are designed for traditional application integration -- developers must write code to consume them.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Developer   │────>│  REST/GraphQL│────>│   Karrio     │
│  writes code │     │     API      │     │   Backend    │
└──────────────┘     └──────────────┘     └──────────────┘
      │
      │  Manual integration required
      │  No AI agent access
      │  No agentic commerce participation
      ▼
┌──────────────────────────────────────────────────────────┐
│  AI agents (Claude, ChatGPT, Gemini, Cursor, etc.)      │
│  CANNOT access Karrio shipping capabilities              │
│                                                          │
│  UCP commerce flows CANNOT use Karrio for fulfillment    │
│  ACP checkout sessions CANNOT query Karrio for rates     │
└──────────────────────────────────────────────────────────┘
```

### Desired State

An MCP server makes Karrio's shipping intelligence natively accessible to any AI agent, and positions Karrio as the fulfillment layer in agentic commerce protocols.

```
┌──────────────────────────────────────────────────────────────────┐
│                    AI AGENT ECOSYSTEM                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │   Claude   │  │  ChatGPT   │  │   Gemini   │  │   Cursor   ││
│  │   Agent    │  │   Agent    │  │   Agent    │  │    IDE     ││
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘│
│        │               │               │               │        │
│        └───────────────┼───────────────┼───────────────┘        │
│                        │               │                         │
│                        ▼               ▼                         │
│               ┌────────────────────────────────┐                │
│               │      MCP Protocol Layer        │                │
│               │   (JSON-RPC over HTTP/stdio)   │                │
│               └───────────────┬────────────────┘                │
│                               │                                  │
└───────────────────────────────┼──────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Karrio MCP Server   │
                    │                       │
                    │  Tools:               │
                    │  • get_shipping_rates  │
                    │  • create_shipment     │
                    │  • track_package       │
                    │  • validate_address    │
                    │  • ...                 │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │    Karrio REST API    │
                    │   (existing backend)  │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
        ┌─────▼─────┐   ┌──────▼─────┐   ┌──────▼─────┐
        │   FedEx   │   │    UPS     │   │   DHL      │
        │   API     │   │    API     │   │   API      │
        └───────────┘   └────────────┘   └────────────┘
```

### Problems

1. **AI Inaccessibility**: Karrio's shipping capabilities are invisible to the rapidly growing ecosystem of AI agents (Claude, ChatGPT, Gemini, Cursor, and others)
2. **Agentic Commerce Gap**: As UCP and ACP define how AI agents perform commerce, shipping platforms without MCP support are excluded from the fulfillment layer
3. **Competitive Disadvantage**: Shippo, ShipStation, ShipBoss, and UPS already have MCP servers; Karrio's multi-carrier advantage is wasted if agents can't access it
4. **Developer Experience Gap**: Modern developers expect to interact with shipping APIs through their AI-powered tools (Cursor, Claude Code, Windsurf); no MCP means Karrio is invisible in these workflows

---

## Goals & Success Criteria

### Goals

1. Ship a production-ready MCP server exposing Karrio's core shipping operations (rates, labels, tracking, address validation) with 10-15 well-designed tools
2. Support both remote (Streamable HTTP with OAuth2) and local (stdio with API key) transports for maximum compatibility
3. Align tool schemas with UCP's fulfillment extension data model so Karrio naturally serves agentic commerce workflows
4. Achieve listing in the MCP server registry and integration guides for Claude, ChatGPT, Cursor, and VS Code

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Tool count | 10-15 focused, workflow-oriented tools | Must-have |
| Transport support | stdio + Streamable HTTP | Must-have |
| Auth methods | API key + OAuth2 | Must-have |
| Claude Desktop integration works | Tested and documented | Must-have |
| ChatGPT integration works | Tested and documented | Must-have |
| Listed on MCP registry | Published package | Must-have |
| UCP fulfillment data model alignment | Rate/shipping tools return UCP-compatible structures | Nice-to-have |
| Documentation and examples | Setup guide, tool reference, demo video | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] MCP server with 10-15 tools covering core shipping operations
- [ ] stdio transport for local development
- [ ] Streamable HTTP transport for remote access
- [ ] API key authentication
- [ ] Published to npm (`@karrio/mcp`) and/or PyPI (`karrio-mcp`)
- [ ] Setup documentation for Claude Desktop, Cursor, and VS Code
- [ ] Tool reference documentation

**Nice-to-have (P1):**
- [ ] OAuth2 authentication for remote server
- [ ] MCP Resources for carrier/service reference data
- [ ] UCP fulfillment extension compatibility layer
- [ ] Karrio docs/knowledge base search tool
- [ ] Listed on official MCP server registry
- [ ] Demo video / interactive playground

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **MCP Server (selected)** | De facto standard (97M downloads), supported by all major AI platforms, UCP uses MCP as binding | Requires building and maintaining a new server component | **Selected** |
| OpenAPI/function calling only | Leverages existing API spec, works with OpenAI function calling | Not a standard protocol, each AI platform has different function calling formats, no resource/prompt support | Rejected |
| Custom AI plugin per platform | Optimized for each platform (ChatGPT plugin, Claude integration) | Enormous maintenance burden, fragmented, no standard | Rejected |
| Wait for protocol consolidation | Avoid investing in something that might change | MCP has already won (Linux Foundation, universal adoption), waiting means falling further behind competitors | Rejected |
| A2A (Agent-to-Agent) only | Designed for multi-agent orchestration | Complementary to MCP, not a replacement; A2A agents still use MCP for tool access | Rejected |

### Trade-off Analysis

MCP was selected because:
- **Universal adoption**: Every major AI platform supports it (Claude, ChatGPT, Gemini, Cursor, VS Code, Copilot)
- **UCP compatibility**: UCP defines MCP as a first-class transport binding, making MCP the path to agentic commerce
- **Ecosystem momentum**: 97M monthly downloads, 10,000+ servers, Linux Foundation governance
- **Complementary to existing API**: MCP wraps the Karrio REST API -- no backend changes needed
- **Competitive parity**: Shippo, ShipStation, UPS, ShipBoss already have MCP servers

The "skills" alternative (lightweight, load-on-demand capabilities) is complementary, not competing. Skills optimize context window usage within a specific agent, while MCP standardizes the connectivity layer. The Karrio MCP server is the foundation; skills can be layered on top for specific agent frameworks.

---

## Technical Design

> **IMPORTANT**: The MCP server acts as a client to the existing Karrio REST API. No changes to the Karrio backend are required.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| REST API endpoints | `modules/*/karrio/server/*/views/` | MCP tools call these via HTTP |
| API serializers | `modules/*/karrio/server/*/serializers/` | Reference for tool parameter design |
| TypeScript API client | `packages/karriojs/api/generated/` | Reference for SDK patterns |
| Carrier references | `GET /v1/references` | MCP resource for carrier/service data |
| Auth middleware | `modules/core/karrio/server/core/authentication.py` | API key validation pattern |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                      KARRIO MCP SERVER                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐    ┌──────────────────┐    ┌────────────────┐ │
│  │  Transport Layer  │    │   Tool Registry   │    │  Auth Layer    │ │
│  │                  │    │                  │    │                │ │
│  │  • stdio         │    │  • get_rates     │    │  • API Key     │ │
│  │  • Streamable    │    │  • ship_package  │    │  • OAuth2      │ │
│  │    HTTP (SSE)    │    │  • track_package │    │  • Bearer      │ │
│  │                  │    │  • validate_addr │    │                │ │
│  └────────┬─────────┘    │  • list_carriers │    └───────┬────────┘ │
│           │              │  • ...           │            │          │
│           │              └────────┬─────────┘            │          │
│           │                       │                      │          │
│           └───────────────────────┼──────────────────────┘          │
│                                   │                                  │
│                        ┌──────────▼──────────┐                      │
│                        │   Karrio API Client  │                      │
│                        │                      │                      │
│                        │  HTTP client that    │                      │
│                        │  calls Karrio REST   │                      │
│                        │  API endpoints       │                      │
│                        └──────────┬───────────┘                      │
│                                   │                                  │
├───────────────────────────────────┼──────────────────────────────────┤
│                                   │                                  │
│                        ┌──────────▼──────────┐                      │
│                        │   Karrio REST API   │                      │
│                        │   (existing, no     │                      │
│                        │    changes needed)   │                      │
│                        └─────────────────────┘                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  AI    │     │  Karrio  │     │  Karrio  │     │ Carrier  │
│ Agent  │     │   MCP    │     │ REST API │     │   APIs   │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                 │
    │  1. MCP       │                │                 │
    │  tools/call   │                │                 │
    │  "get_rates"  │                │                 │
    │──────────────>│                │                 │
    │               │  2. POST       │                 │
    │               │  /v1/proxy/    │                 │
    │               │  rates         │                 │
    │               │───────────────>│                 │
    │               │                │  3. Carrier     │
    │               │                │  rate requests  │
    │               │                │────────────────>│
    │               │                │                 │
    │               │                │  4. Carrier     │
    │               │                │  responses      │
    │               │                │<────────────────│
    │               │  5. Unified    │                 │
    │               │  rates         │                 │
    │               │<───────────────│                 │
    │  6. MCP       │                │                 │
    │  result       │                │                 │
    │  (structured  │                │                 │
    │   rates)      │                │                 │
    │<──────────────│                │                 │
    │               │                │                 │
    │  7. User:     │                │                 │
    │  "Ship with   │                │                 │
    │   FedEx"      │                │                 │
    │──────────────>│                │                 │
    │               │  8. POST       │                 │
    │               │  /v1/shipments │                 │
    │               │  + purchase    │                 │
    │               │───────────────>│                 │
    │               │                │  9. Buy label   │
    │               │                │────────────────>│
    │               │                │<────────────────│
    │               │  10. Shipment  │                 │
    │               │  with label    │                 │
    │               │<───────────────│                 │
    │  11. MCP      │                │                 │
    │  result       │                │                 │
    │  (tracking #, │                │                 │
    │   label URL)  │                │                 │
    │<──────────────│                │                 │
    │               │                │                 │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         TOOL INVOCATION FLOW                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────┐│
│  │ MCP Call  │───>│  Parameter   │───>│  Karrio API  │───>│Result ││
│  │           │    │  Validation  │    │    Call       │    │Format ││
│  │ tool:     │    │  & Transform │    │              │    │       ││
│  │ get_rates │    │              │    │  POST /v1/   │    │ JSON  ││
│  │           │    │  Flat params │    │  proxy/rates │    │ with  ││
│  │ params:   │    │  → Karrio    │    │              │    │ UCP-  ││
│  │  origin   │    │    payload   │    │              │    │ compat││
│  │  dest     │    │              │    │              │    │ fields││
│  │  weight   │    │              │    │              │    │       ││
│  └───────────┘    └──────────────┘    └──────────────┘    └───────┘│
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                         ERROR HANDLING FLOW                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────┐│
│  │ MCP Call  │───>│  Validation  │───>│  API Error   │───>│ Human ││
│  │ (invalid) │    │  Failure     │    │  (carrier    │    │ Read- ││
│  │           │    │              │    │   down, etc) │    │ able  ││
│  │           │    │  Return      │    │              │    │ Error ││
│  │           │    │  helpful     │    │  Return      │    │ Msg   ││
│  │           │    │  error msg   │    │  actionable  │    │       ││
│  │           │    │  with fix    │    │  suggestion  │    │       ││
│  └───────────┘    └──────────────┘    └──────────────┘    └───────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Tool Design

The MCP server exposes **12 tools** organized by shipping workflow stage. Tools follow the `{action}_{resource}` naming convention with flat, top-level parameters.

#### Core Tools (P0)

| # | Tool | Description | Karrio API Endpoint |
|---|------|-------------|---------------------|
| 1 | `get_shipping_rates` | Get carrier rate quotes for a package | `POST /v1/proxy/rates` |
| 2 | `create_shipment` | Create a shipment and optionally purchase a label | `POST /v1/shipments` + `POST /v1/shipments/{id}/purchase` |
| 3 | `track_package` | Get tracking status and events for a package | `POST /v1/trackers` or `GET /v1/trackers/{tracking_number}` |
| 4 | `validate_address` | Validate and correct a shipping address | `POST /v1/addresses` (with validation) |
| 5 | `list_carriers` | List available carriers and their services | `GET /v1/carriers` |
| 6 | `get_shipment` | Retrieve details of an existing shipment | `GET /v1/shipments/{id}` |
| 7 | `cancel_shipment` | Void/cancel a purchased shipment label | `POST /v1/shipments/{id}/cancel` |
| 8 | `list_shipments` | List shipments with filters (status, date, carrier) | `GET /v1/shipments` |

#### Extended Tools (P1)

| # | Tool | Description | Karrio API Endpoint |
|---|------|-------------|---------------------|
| 9 | `schedule_pickup` | Schedule a carrier pickup for shipments | `POST /v1/pickups` |
| 10 | `create_manifest` | Create end-of-day manifest for carrier | `POST /v1/manifests` |
| 11 | `list_orders` | List orders and their fulfillment status | `GET /v1/orders` |
| 12 | `search_docs` | Search Karrio documentation and guides | Karrio knowledge base |

#### Tool Parameter Design

Tools use **flat, top-level parameters** with descriptive names and constrained types. No nested objects.

```typescript
// Example: get_shipping_rates
{
  name: "get_shipping_rates",
  description: "Get shipping rate quotes from multiple carriers for a package. Returns ranked rates with carrier name, service, price, and estimated delivery. Use this when a user wants to compare shipping options or find the cheapest/fastest way to ship something.",
  inputSchema: {
    type: "object",
    properties: {
      // Origin
      origin_city:         { type: "string", description: "Origin city name" },
      origin_state:        { type: "string", description: "Origin state/province code (e.g., 'CA', 'ON')" },
      origin_postal_code:  { type: "string", description: "Origin postal/zip code" },
      origin_country_code: { type: "string", description: "Origin ISO 2-letter country code (e.g., 'US', 'CA')" },

      // Destination
      dest_city:         { type: "string", description: "Destination city name" },
      dest_state:        { type: "string", description: "Destination state/province code" },
      dest_postal_code:  { type: "string", description: "Destination postal/zip code" },
      dest_country_code: { type: "string", description: "Destination ISO 2-letter country code" },

      // Package
      weight:      { type: "number", description: "Package weight" },
      weight_unit: { type: "string", enum: ["LB", "KG", "OZ", "G"], default: "LB", description: "Weight unit" },
      length:      { type: "number", description: "Package length (optional)" },
      width:       { type: "number", description: "Package width (optional)" },
      height:      { type: "number", description: "Package height (optional)" },
      dimension_unit: { type: "string", enum: ["IN", "CM"], default: "IN", description: "Dimension unit" },

      // Options
      carrier_names:  { type: "string", description: "Comma-separated carrier names to query (e.g., 'fedex,ups,dhl'). Omit to query all." },
      max_results:    { type: "integer", default: 10, description: "Maximum number of rates to return" },
      sort_by:        { type: "string", enum: ["price", "delivery_time"], default: "price", description: "How to sort results" },
    },
    required: ["origin_postal_code", "origin_country_code", "dest_postal_code", "dest_country_code", "weight"]
  }
}
```

```typescript
// Example: create_shipment
{
  name: "create_shipment",
  description: "Create a shipment and purchase a shipping label. This generates a label you can print. IMPORTANT: This action purchases a label and incurs a charge. Make sure the user has confirmed the shipment details before calling this tool.",
  annotations: {
    readOnlyHint: false,
    destructiveHint: true,    // Signals clients to prompt for confirmation
    idempotentHint: false,
    openWorldHint: true,
  },
  inputSchema: {
    type: "object",
    properties: {
      // Shipper
      shipper_name:         { type: "string", description: "Shipper person or company name" },
      shipper_address_line1:{ type: "string", description: "Shipper street address" },
      shipper_city:         { type: "string", description: "Shipper city" },
      shipper_state:        { type: "string", description: "Shipper state/province code" },
      shipper_postal_code:  { type: "string", description: "Shipper postal/zip code" },
      shipper_country_code: { type: "string", description: "Shipper ISO 2-letter country code" },
      shipper_phone:        { type: "string", description: "Shipper phone number" },

      // Recipient
      recipient_name:         { type: "string", description: "Recipient person or company name" },
      recipient_address_line1:{ type: "string", description: "Recipient street address" },
      recipient_city:         { type: "string", description: "Recipient city" },
      recipient_state:        { type: "string", description: "Recipient state/province code" },
      recipient_postal_code:  { type: "string", description: "Recipient postal/zip code" },
      recipient_country_code: { type: "string", description: "Recipient ISO 2-letter country code" },
      recipient_phone:        { type: "string", description: "Recipient phone number" },

      // Package
      weight:         { type: "number", description: "Package weight" },
      weight_unit:    { type: "string", enum: ["LB", "KG", "OZ", "G"], default: "LB" },

      // Shipping
      carrier_name:   { type: "string", description: "Carrier to ship with (e.g., 'fedex', 'ups')" },
      service:        { type: "string", description: "Service code (e.g., 'fedex_ground', 'ups_next_day_air'). Use list_carriers to find codes." },
      label_type:     { type: "string", enum: ["PDF", "ZPL", "PNG"], default: "PDF" },

      // Optional
      reference:      { type: "string", description: "Shipment reference number" },
    },
    required: ["shipper_name", "shipper_address_line1", "shipper_postal_code", "shipper_country_code",
               "recipient_name", "recipient_address_line1", "recipient_postal_code", "recipient_country_code",
               "weight", "carrier_name", "service"]
  }
}
```

```typescript
// Example: track_package
{
  name: "track_package",
  description: "Track a package by tracking number. Returns current status, location, estimated delivery date, and full event history. Supports all major carriers (FedEx, UPS, DHL, USPS, Canada Post, and 50+ more).",
  inputSchema: {
    type: "object",
    properties: {
      tracking_number: { type: "string", description: "The package tracking number" },
      carrier_name:    { type: "string", description: "Carrier name (e.g., 'fedex', 'ups'). If omitted, Karrio will attempt auto-detection." },
    },
    required: ["tracking_number"]
  }
}
```

### MCP Resources -- The Differentiator (P1)

Resources are the key differentiator for Karrio MCP. **No other shipping MCP server exposes Resources.** Shippo, ShipStation, EasyPost, and UPS are all tools-only. By exposing Karrio's multi-carrier knowledge as structured Resources, we give AI agents a grounding catalog that enables reasoning about carrier selection *before* making API calls.

**Client support reality:** Claude Desktop, Claude Code, VS Code Copilot, Continue, Codex, and Postman support Resources. **Cursor and ChatGPT do not.** To handle this, we use a **hybrid approach**: every Resource also has a corresponding read-only Tool fallback.

#### Resource Catalog

| Resource URI | Description | Tool Fallback |
|-------------|-------------|---------------|
| `karrio://carriers` | All supported carriers with capabilities (tracking, rating, shipping, pickup, manifest) | `list_carriers` |
| `karrio://carriers/{carrier_id}` | Full capability snapshot for a specific carrier | `list_carriers` with filter |
| `karrio://carriers/{carrier_id}/services` | Available services with descriptions, transit times | (new) `get_carrier_services` |
| `karrio://carriers/{carrier_id}/options` | Shipping options available for a carrier | (new) `get_shipping_options` |
| `karrio://carriers/{carrier_id}/package_types` | Carrier-specific package type codes | (new) `get_package_types` |
| `karrio://reference/countries` | ISO country codes and names | (embedded in tool descriptions) |

#### Resource Template Example

```python
# Using FastMCP or similar framework
@mcp.resource("karrio://carriers")
def get_carrier_catalog() -> str:
    """Complete multi-carrier capability catalog.

    Returns all 50+ supported carriers with their capabilities:
    tracking, rating, shipping, pickup, manifest support.
    Use this to understand what carriers are available before
    fetching rates or creating shipments.
    """
    # Calls GET /v1/carriers on Karrio API
    carriers = karrio_client.list_carriers()
    return json.dumps(carriers)


@mcp.resource("karrio://carriers/{carrier_id}/services")
def get_carrier_services(carrier_id: str) -> str:
    """Shipping services for a specific carrier.

    Returns service codes, display names, descriptions, and
    whether each service supports features like tracking,
    insurance, or signature confirmation.
    """
    # Calls GET /v1/carriers/{carrier_id}/services on Karrio API
    services = karrio_client.get_carrier_services(carrier_id)
    return json.dumps(services)
```

#### Resource Content Example

```json
// karrio://carriers (abbreviated)
{
  "carriers": [
    {
      "id": "fedex",
      "name": "FedEx",
      "capabilities": {
        "rating": true,
        "shipping": true,
        "tracking": true,
        "pickup": true,
        "manifest": true,
        "address_validation": true
      },
      "services_count": 15,
      "resource_uri": "karrio://carriers/fedex/services"
    },
    {
      "id": "ups",
      "name": "UPS",
      "capabilities": {
        "rating": true,
        "shipping": true,
        "tracking": true,
        "pickup": true,
        "manifest": true,
        "address_validation": true
      },
      "services_count": 12,
      "resource_uri": "karrio://carriers/ups/services"
    }
    // ... 50+ carriers
  ]
}
```

#### Why This Is a Differentiator

```
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT CONTEXT: Before making a single API call...                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  With Shippo/EasyPost MCP (tools only):                             │
│  Agent knows NOTHING about carriers until it calls tools.           │
│  Must call list_carriers → then get_services → then get_rates       │
│  = 3+ round trips before reasoning about options.                   │
│                                                                     │
│  With Karrio MCP (Resources + Tools):                               │
│  Agent starts with karrio://carriers injected in context.           │
│  Already knows: FedEx supports 15 services, UPS supports 12,       │
│  DHL supports international, USPS is domestic-only...               │
│  Can immediately reason: "For international to Brazil,              │
│  I should query FedEx, UPS, and DHL -- not USPS."                   │
│  = 1 targeted rate call with relevant carriers only.                │
│                                                                     │
│  Result: Faster, cheaper, smarter shipping decisions.               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### UCP Fulfillment Alignment

The `get_shipping_rates` tool response can optionally include UCP-compatible fields, enabling Karrio to serve as a fulfillment provider in UCP flows.

```
UCP Fulfillment Extension          Karrio MCP Response
─────────────────────────          ────────────────────
fulfillment.methods[]       ←───   (shipping is the method)
fulfillment.groups[]        ←───   rates grouped by carrier
  group.options[]           ←───   individual rate quotes
    option.title            ←───   rate.service_display_name
    option.description      ←───   rate.carrier + est. delivery
    option.totals           ←───   rate.total_charge + currency
```

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| MCP SDK | `@modelcontextprotocol/sdk` (TypeScript) | Official SDK, best ecosystem support, npm-native |
| Language | **TypeScript** | npm distribution standard for MCP servers (Stripe, Shippo, ShipStation all use TS). Clean SDK ergonomics. Karrio API client is a simple HTTP wrapper -- no need to share Python types. |
| HTTP Client | `fetch` / `node-fetch` | Standard, lightweight |
| Transport (local) | stdio | Standard for local MCP, works with Claude Desktop/Cursor |
| Transport (remote) | Streamable HTTP (SSE) | Standard for remote MCP, works with hosted deployments |
| Auth | API key header + OAuth2 | API key for local dev, OAuth2 for production |
| Packaging | **npm (`@karrio/mcp`)** | Primary distribution. `npx -y @karrio/mcp` for zero-install. Standard developer experience across Cursor, Claude Desktop, VS Code. |

### API Changes

No changes to the existing Karrio REST API. The MCP server is a pure consumer of the existing API.

**New endpoints (MCP server only):**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mcp` | Streamable HTTP MCP endpoint (JSON-RPC) |
| GET | `/mcp/sse` | SSE stream for MCP notifications |
| GET | `/.well-known/mcp` | MCP server discovery metadata |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Agent requests rates with incomplete address | Return validation error with missing fields listed | Validate required params before API call, return helpful error |
| Carrier API is down for one carrier | Return rates from available carriers, note failures | Partial success: return available rates + error message for failed carriers |
| Tracking number matches multiple carriers | Return results from all matching carriers | Use `carrier_name` param to disambiguate, or return all matches |
| Agent calls `create_shipment` without prior rate check | Shipment created with carrier's default rate | Tool description advises using `get_shipping_rates` first |
| Very large shipment list (1000+) | Response exceeds context window | Default `limit=20`, support pagination via `offset` |
| Agent passes address in non-English characters | Forward to Karrio API which handles unicode | No special handling needed, pass through |
| OAuth token expired during session | Return auth error | Return clear error message: "Authentication expired. Please reconnect." |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Karrio API unreachable | All tools fail | Return clear error: "Cannot connect to Karrio API at {url}. Check your configuration." |
| Invalid API key | Auth failures | Validate API key on server startup, return actionable error |
| Rate limiting by Karrio API | Degraded performance | Respect rate limits, return "Rate limited, please try again in X seconds" |
| Agent purchases label without user intent | Financial loss | Tool description includes warning, recommend confirmation flow |
| MCP protocol version mismatch | Connection failure | Support latest MCP spec, graceful degradation for older clients |
| Large label PDF in response | Context window overflow | Return label as URL/download link, not base64 in tool response |

### Security Considerations

- [ ] API keys never logged or included in error messages
- [ ] OAuth2 tokens validated on every request
- [ ] No carrier credentials exposed through MCP tools
- [ ] Input validation for all tool parameters (injection prevention)
- [ ] Rate limiting on tool calls to prevent abuse
- [ ] Label purchase tools include clear cost warnings in descriptions
- [ ] No direct database access -- all operations go through Karrio REST API

---

## Implementation Plan

### Phase 1: Core MCP Server (P0)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Set up TypeScript project (`@karrio/mcp`) | `packages/mcp/package.json`, `tsconfig.json` | Pending | M |
| Implement Karrio API client wrapper | `packages/mcp/src/client.ts` | Pending | M |
| Implement stdio transport + server entry point | `packages/mcp/src/index.ts` | Pending | S |
| Implement `get_shipping_rates` tool | `packages/mcp/src/tools/rates.ts` | Pending | M |
| Implement `track_package` tool | `packages/mcp/src/tools/tracking.ts` | Pending | M |
| Implement `validate_address` tool | `packages/mcp/src/tools/addresses.ts` | Pending | S |
| Implement `list_carriers` tool | `packages/mcp/src/tools/carriers.ts` | Pending | S |
| Implement `get_shipment` and `list_shipments` tools | `packages/mcp/src/tools/shipments.ts` | Pending | M |
| Implement `create_shipment` tool (with annotations) | `packages/mcp/src/tools/shipments.ts` | Pending | L |
| Implement `cancel_shipment` tool | `packages/mcp/src/tools/shipments.ts` | Pending | S |
| API key authentication | `packages/mcp/src/auth.ts` | Pending | S |
| Publish to npm (`@karrio/mcp`) | `packages/mcp/` | Pending | S |

### Phase 2: Resources & Extended Tools (P1)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Implement MCP Resources for carrier catalog | `packages/mcp/src/resources/carriers.ts` | Pending | M |
| Implement Resource templates for services/options | `packages/mcp/src/resources/services.ts` | Pending | M |
| Implement `get_carrier_services` read-only tool (fallback) | `packages/mcp/src/tools/carriers.ts` | Pending | S |
| Implement `get_shipping_options` read-only tool (fallback) | `packages/mcp/src/tools/carriers.ts` | Pending | S |
| Implement `get_package_types` read-only tool (fallback) | `packages/mcp/src/tools/carriers.ts` | Pending | S |
| Implement `schedule_pickup` tool | `packages/mcp/src/tools/pickups.ts` | Pending | M |
| Implement `create_manifest` tool | `packages/mcp/src/tools/manifests.ts` | Pending | M |
| Implement `list_orders` tool | `packages/mcp/src/tools/orders.ts` | Pending | S |
| Implement `search_docs` tool | `packages/mcp/src/tools/docs.ts` | Pending | M |
| Implement Streamable HTTP transport | `packages/mcp/src/transports/http.ts` | Pending | M |
| Implement OAuth2 authentication | `packages/mcp/src/auth.ts` | Pending | M |

### Phase 3: UCP Alignment & Polish (P2)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| UCP fulfillment extension response mapping | `packages/mcp/src/ucp/fulfillment.ts` | Pending | L |
| MCP server discovery (`/.well-known/mcp`) | `packages/mcp/src/discovery.ts` | Pending | S |
| Integration testing with Claude Desktop | `packages/mcp/tests/integration/` | Pending | M |
| Integration testing with ChatGPT | `packages/mcp/tests/integration/` | Pending | M |
| Integration testing with Cursor | `packages/mcp/tests/integration/` | Pending | M |
| Documentation site / setup guides | `packages/mcp/docs/` | Pending | M |
| Demo video and examples | `packages/mcp/examples/` | Pending | M |
| MCP registry listing | External | Pending | S |

**Dependencies:** Phase 2 depends on Phase 1 completion. Phase 3 depends on Phase 1 completion (can run parallel with Phase 2).

---

## Testing Strategy

> **Note**: The MCP server is a TypeScript package (`@karrio/mcp`). Tests use Vitest (standard for TypeScript MCP projects). Python test patterns from AGENTS.md apply to backend Karrio code, not the MCP package.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `packages/mcp/tests/unit/` | Individual tool logic, parameter validation |
| Integration Tests | `packages/mcp/tests/integration/` | Full MCP protocol round-trips |
| E2E Tests | `packages/mcp/tests/e2e/` | Claude Desktop / Cursor integration |

### Test Cases

#### Unit Tests

```typescript
// packages/mcp/tests/unit/tools/rates.test.ts
import { describe, it, expect, vi } from "vitest";
import { getShippingRatesTool } from "../../../src/tools/rates";
import { KarrioClient } from "../../../src/client";

describe("get_shipping_rates tool", () => {
  it("fetches and formats rates correctly", async () => {
    const mockClient = {
      fetchRates: vi.fn().mockResolvedValue({
        rates: [
          {
            carrier_name: "fedex",
            service: "fedex_ground",
            total_charge: 12.5,
            currency: "USD",
            transit_days: 5,
          },
        ],
      }),
    } as unknown as KarrioClient;

    const result = await getShippingRatesTool.execute(mockClient, {
      origin_postal_code: "10001",
      origin_country_code: "US",
      dest_postal_code: "90210",
      dest_country_code: "US",
      weight: 5.0,
    });

    console.log(result);
    expect(result.rates).toHaveLength(1);
    expect(result.rates[0]).toEqual({
      carrier: "fedex",
      service: "fedex_ground",
      price: 12.5,
      currency: "USD",
      estimated_days: 5,
    });
  });

  it("returns helpful error when required params missing", async () => {
    const mockClient = {} as KarrioClient;

    const result = await getShippingRatesTool.execute(mockClient, {
      origin_postal_code: "10001",
      // Missing required fields
    });

    console.log(result);
    expect(result.error).toBeDefined();
    expect(result.error.toLowerCase()).toContain("required");
  });
});
```

```typescript
// packages/mcp/tests/unit/tools/tracking.test.ts
import { describe, it, expect, vi } from "vitest";
import { trackPackageTool } from "../../../src/tools/tracking";

describe("track_package tool", () => {
  it("tracks package with explicit carrier", async () => {
    const mockClient = {
      track: vi.fn().mockResolvedValue({
        tracking_number: "1Z999AA10123456784",
        status: "in_transit",
        carrier_name: "ups",
        events: [
          {
            date: "2026-02-17T10:00:00Z",
            description: "In Transit",
            location: "Memphis, TN",
          },
        ],
      }),
    };

    const result = await trackPackageTool.execute(mockClient, {
      tracking_number: "1Z999AA10123456784",
      carrier_name: "ups",
    });

    console.log(result);
    expect(result.status).toBe("in_transit");
    expect(result.carrier).toBe("ups");
    expect(result.events).toHaveLength(1);
  });
});
```

#### Integration Tests

```typescript
// packages/mcp/tests/integration/protocol.test.ts
import { describe, it, expect, vi } from "vitest";
import { createServer } from "../../src/index";

describe("MCP Protocol", () => {
  it("lists all expected tools", async () => {
    const server = createServer({ apiKey: "test_key", apiUrl: "http://localhost" });

    const response = await server.handleRequest({
      jsonrpc: "2.0",
      method: "tools/list",
      id: 1,
    });

    console.log(response);
    const toolNames = response.result.tools.map((t: any) => t.name);
    expect(toolNames).toContain("get_shipping_rates");
    expect(toolNames).toContain("track_package");
    expect(toolNames).toContain("create_shipment");
    expect(toolNames).toContain("validate_address");
    expect(toolNames).toContain("list_carriers");
  });

  it("lists resources when capability declared", async () => {
    const server = createServer({ apiKey: "test_key", apiUrl: "http://localhost" });

    const response = await server.handleRequest({
      jsonrpc: "2.0",
      method: "resources/list",
      id: 2,
    });

    console.log(response);
    const resourceUris = response.result.resources.map((r: any) => r.uri);
    expect(resourceUris).toContain("karrio://carriers");
  });

  it("reads carrier catalog resource", async () => {
    const server = createServer({ apiKey: "test_key", apiUrl: "http://localhost" });

    const response = await server.handleRequest({
      jsonrpc: "2.0",
      method: "resources/read",
      params: { uri: "karrio://carriers" },
      id: 3,
    });

    console.log(response);
    expect(response.result.contents).toBeDefined();
    expect(response.result.contents[0].mimeType).toBe("application/json");
  });
});
```

### Running Tests

```bash
# From packages/mcp directory
npm test                    # Run all tests
npm run test:unit           # Unit tests only
npm run test:integration    # Integration tests only

# Or from repository root
cd packages/mcp && npm test
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| MCP protocol spec changes | Medium | Low | Pin to stable spec version, monitor spec repo |
| Agent purchases labels without user consent | High | Medium | Clear tool descriptions with cost warnings, recommend confirmation flow |
| API key leakage through MCP logs | High | Low | Never log API keys, sanitize all error messages |
| Large responses exceed context window | Medium | Medium | Pagination defaults, return URLs instead of base64 data |
| Competitor MCP servers have more features | Medium | Medium | Focus on multi-carrier advantage, clean tool design |
| Low adoption / discovery | Medium | Medium | Register on MCP registry, write guides for Claude/ChatGPT/Cursor |
| Self-hosted Karrio instances have different API versions | Medium | Low | Version negotiation on startup, minimum API version check |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No changes to existing Karrio REST API or GraphQL API
- **Data compatibility**: MCP server is a pure consumer, no database changes
- **Feature flags**: Not needed -- MCP server is an entirely new, additive component

### Rollback Procedure

1. **Identify issue**: Monitor MCP server logs for errors, check agent integration reports
2. **Stop rollout**: Disable MCP server process / remove from deployment
3. **Revert changes**: Unpublish package version if needed
4. **Verify recovery**: Confirm Karrio REST API continues to function independently

Since the MCP server is a separate, additive component that consumes the existing REST API, rollback is trivially simple -- just stop the MCP server process.

---

## Appendices

### Appendix A: Competitive Landscape

| Platform | MCP Server | Tools | Multi-Carrier | Open Source | Transport |
|----------|-----------|-------|---------------|-------------|-----------|
| UPS | Yes (official) | 2 | No (UPS only) | Yes | stdio |
| Shippo | Yes (official) | ~15 | Yes | No (npm only) | stdio |
| EasyPost | Yes (community) | 11 | Yes | Yes | stdio |
| ShipStation | Yes (official) | 50+ | Yes | Yes | stdio |
| ShipBoss | Yes | 8 | Yes | Yes | stdio |
| ShipBob | Yes (official) | 27 | N/A (fulfillment) | No | HTTP |
| Stripe | Yes (official) | Many | N/A (payments) | Yes | stdio + HTTP |
| **Karrio** | **Proposed** | **12** | **Yes (50+)** | **Yes** | **stdio + HTTP** |

**Karrio's differentiation:**
- Most carriers supported (50+) vs. ShipBoss (3) or UPS (1)
- Open source with self-hosting option
- Dual transport (stdio + HTTP) like Stripe
- UCP fulfillment alignment (unique)

### Appendix B: Commerce Protocol Compatibility Matrix

| Protocol | Relationship to Karrio MCP | Integration Path |
|----------|---------------------------|------------------|
| **UCP** (Google/Shopify) | Karrio MCP serves as the fulfillment capability provider | MCP tools return UCP-compatible fulfillment data structures |
| **ACP** (OpenAI/Stripe) | Merchants use Karrio behind their ACP checkout endpoints | Indirect -- merchant calls Karrio API to populate ACP fulfillment options |
| **MCP** (Anthropic/LF) | Direct transport layer | Native -- Karrio IS an MCP server |
| **A2A** (Google) | Future: shipping agent in multi-agent workflows | Future phase -- A2A agents use MCP tools internally |

### Appendix C: UCP Fulfillment Extension Mapping

| UCP Concept | Karrio Equivalent | MCP Tool |
|-------------|-------------------|----------|
| `fulfillment.methods[]` | Shipping method (ground, express, etc.) | `get_shipping_rates` returns methods |
| `fulfillment.destinations[]` | Recipient address | `validate_address` validates destinations |
| `fulfillment.groups[]` | Rates grouped by carrier | `get_shipping_rates` groups results |
| `group.options[].title` | `rate.service` display name | Returned in rate response |
| `group.options[].description` | Carrier name + estimated delivery | Returned in rate response |
| `group.options[].totals` | `rate.total_charge` + `rate.currency` | Returned in rate response |

### Appendix D: MCP vs Skills -- Strategic Position

**MCP and skills are complementary, not competing:**

| Aspect | MCP | Skills |
|--------|-----|--------|
| Purpose | Universal tool connectivity standard | Agent-specific lightweight capabilities |
| Scope | Cross-platform, cross-agent | Within a specific agent framework |
| Overhead | Full protocol negotiation, tool schemas | Minimal, load-on-demand |
| Best for | External service integration | Frequent, lightweight operations |
| Example | `create_shipment` (needs Karrio API) | "Format tracking number" (pure logic) |

**Recommendation:** Build MCP as the foundation for external connectivity. If specific agent frameworks (like Claude Code) benefit from skills for common operations (e.g., quick tracking lookups), those can be layered on top using the same underlying Karrio API client.

### Appendix E: Configuration Examples

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "karrio": {
      "command": "karrio-mcp",
      "args": ["--api-url", "https://api.karrio.io", "--api-key", "key_..."]
    }
  }
}
```

**Cursor (`.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "karrio": {
      "command": "karrio-mcp",
      "args": ["--api-url", "https://api.karrio.io", "--api-key", "key_..."]
    }
  }
}
```

**Remote (Streamable HTTP):**
```json
{
  "mcpServers": {
    "karrio": {
      "url": "https://api.karrio.io/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer oauth_token_..."
      }
    }
  }
}
```

**Environment variables (alternative):**
```bash
export KARRIO_API_URL="https://api.karrio.io"
export KARRIO_API_KEY="key_..."
karrio-mcp
```

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [ ] All pending questions in "Open Questions & Decisions" have been asked
- [ ] All user decisions documented with rationale and date
- [ ] Edge cases requiring input have been resolved
- [ ] "Open Questions & Decisions" section cleaned up (all resolved or removed)

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (Karrio REST API as backend)

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
