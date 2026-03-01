# OSP-CLOUD-GATEWAY: karrio Cloud as Hosted OSP Gateway

**Version**: 0.1 (Draft)
**License**: Apache 2.0
**Prerequisite**: [OSP-CORE.md](./OSP-CORE.md)

---

## Table of Contents

1. [The Stripe Analogy](#1-the-stripe-analogy)
2. [Architecture](#2-architecture)
3. [Multi-Carrier Management](#3-multi-carrier-management)
4. [Rate Optimization](#4-rate-optimization)
5. [Label Management](#5-label-management)
6. [Webhook Aggregation](#6-webhook-aggregation)
7. [MCP Gateway](#7-mcp-gateway)
8. [Pricing Model](#8-pricing-model)

---

## 1. The Stripe Analogy

Stripe made payments simple: one API, hundreds of payment methods, no bank integrations to maintain. **karrio Cloud does the same for shipping**: one API (OSP), 100+ carriers, no carrier integrations to maintain.

```
Payments (Stripe)                    Shipping (karrio Cloud)
─────────────────                    ──────────────────────

One API                              One API (OSP)
    ↓                                    ↓
Stripe handles:                      karrio Cloud handles:
  • Payment method routing             • Carrier routing
  • PCI compliance                     • Label generation
  • Fraud detection                    • Rate optimization
  • Multi-currency                     • Multi-carrier tracking
  • Webhook delivery                   • Webhook aggregation
  • Dashboard & analytics              • Dashboard & analytics
    ↓                                    ↓
100+ payment methods                 100+ carriers
  Visa, Mastercard,                    FedEx, UPS, DHL,
  Apple Pay, ACH, SEPA...             USPS, Canada Post, Geopost...
```

| Stripe Concept | karrio Cloud Equivalent |
|---------------|------------------------|
| Payment Methods | Carrier Connections |
| Charges | Shipments |
| Payment Intents | Rate Quotes |
| Disputes | Delivery Exceptions |
| Webhooks | Tracking Events |
| Connect (multi-merchant) | Multi-tenant Organizations |
| Stripe Dashboard | karrio Dashboard |
| `pk_live_xxx` / `sk_live_xxx` | `osp_key_xxx` |

### Why a Hosted Gateway?

| Self-Hosted OSP | karrio Cloud OSP Gateway |
|----------------|--------------------------|
| You manage carrier credentials | karrio manages carrier connections |
| You handle carrier API changes | karrio handles API version migrations |
| You build rate optimization | Built-in intelligent rate shopping |
| You aggregate tracking webhooks | Unified webhook stream |
| You monitor carrier uptime | karrio monitors and fails over |
| You scale infrastructure | Auto-scaling, globally distributed |

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        karrio Cloud                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    OSP Gateway Layer                        │  │
│  │                                                            │  │
│  │  REST: /osp/v1/*          MCP: osp/* tools                │  │
│  │  Auth: API keys + OAuth   Transport: stdio + HTTP          │  │
│  └─────────────┬──────────────────────┬───────────────────────┘  │
│                │                      │                          │
│  ┌─────────────▼──────────────────────▼───────────────────────┐  │
│  │                   Core Services                             │  │
│  │                                                             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │  │
│  │  │  Rating  │ │ Shipping │ │ Tracking │ │   Webhooks   │  │  │
│  │  │  Engine  │ │  Engine  │ │  Engine  │ │  Dispatcher  │  │  │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘  │  │
│  │       │             │            │               │          │  │
│  │  ┌────▼─────────────▼────────────▼───────────────▼───────┐ │  │
│  │  │              Carrier Abstraction Layer                 │ │  │
│  │  │     (karrio SDK — 100+ carrier connectors)             │ │  │
│  │  └────┬──────────┬──────────┬──────────┬─────────────────┘ │  │
│  │       │          │          │          │                    │  │
│  └───────┼──────────┼──────────┼──────────┼────────────────────┘  │
│          │          │          │          │                        │
└──────────┼──────────┼──────────┼──────────┼────────────────────────┘
           │          │          │          │
     ┌─────▼──┐ ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐
     │ FedEx  │ │  UPS   │ │  DHL   │ │ 97+    │
     │  API   │ │  API   │ │  API   │ │ others │
     └────────┘ └────────┘ └────────┘ └────────┘
```

### Request Flow

1. Client sends an OSP request (REST or MCP)
2. Gateway authenticates and routes to the appropriate service
3. Service translates the OSP request to carrier-specific format(s)
4. Carrier responses are translated back to OSP format
5. Response is returned to the client

### Multi-Tenancy

karrio Cloud supports multi-tenant organizations. Each organization has:

- Isolated carrier connections (their own FedEx/UPS/DHL accounts)
- Separate API keys and webhook subscriptions
- Independent rate sheets and shipping rules
- Organization-scoped data (no cross-tenant data leakage)

---

## 3. Multi-Carrier Management

### 3.1 Carrier Connection

Merchants connect their carrier accounts through the karrio Dashboard or API:

```json
// Connect a FedEx account
POST /api/v1/carriers
{
  "carrier_name": "fedex",
  "display_name": "My FedEx Production",
  "credentials": {
    "api_key": "...",
    "secret_key": "...",
    "account_number": "..."
  },
  "test_mode": false
}
```

Once connected, all OSP operations automatically route to the appropriate carrier based on the service code.

### 3.2 Carrier Routing

When an OSP operation specifies a service code (e.g., `fedex_ground`), the gateway:

1. Identifies the carrier from the service code prefix (`fedex`)
2. Looks up the merchant's active connection for that carrier
3. Routes the request using those credentials
4. Returns the response in OSP format

### 3.3 Multi-Carrier Rate Shopping

When `osp/get_rates` is called without a specific carrier filter, the gateway queries all connected carriers in parallel:

```
osp/get_rates request
       │
       ├──── FedEx API (parallel) ──── FedEx rates
       ├──── UPS API (parallel)   ──── UPS rates
       ├──── DHL API (parallel)   ──── DHL rates
       └──── USPS API (parallel)  ──── USPS rates
                                         │
                                         ▼
                                  Merge, sort, return
                                  unified OSP rates
```

This is a key advantage of the hosted gateway — a single `osp/get_rates` call returns rates from all carriers, eliminating the need for the client to make multiple API calls.

---

## 4. Rate Optimization

### 4.1 Intelligent Rate Shopping

Beyond simple multi-carrier queries, karrio Cloud provides optimization features:

| Feature | Description |
|---------|-------------|
| **Rate caching** | Cache rates for identical origin/destination/weight combinations (configurable TTL) |
| **Rate sheets** | Define custom rates, zones, and surcharges for white-label or negotiated pricing |
| **Service filtering** | Auto-exclude services that don't meet delivery requirements |
| **Carrier failover** | If a carrier API is down, transparently route to alternatives |

### 4.2 Custom Rate Sheets

Merchants can define custom rate sheets that override or supplement carrier rates:

```json
{
  "name": "My Custom Rates",
  "carrier_name": "custom_carrier",
  "services": [
    {
      "service_name": "Standard Shipping",
      "service_code": "custom_standard",
      "currency": "USD",
      "zones": [
        {
          "label": "Domestic",
          "country_codes": ["US"],
          "rate": 9.99,
          "transit_days": 5
        },
        {
          "label": "Canada",
          "country_codes": ["CA"],
          "rate": 14.99,
          "transit_days": 7
        }
      ]
    }
  ]
}
```

These custom rates appear alongside carrier rates in `osp/get_rates` responses, providing merchants with complete flexibility.

### 4.3 Shipping Rules

Automated rules that optimize carrier selection:

```json
{
  "rules": [
    {
      "name": "Heavy packages via freight",
      "condition": { "parcel_weight_gt": 150, "weight_unit": "LB" },
      "action": { "prefer_carriers": ["freightquote", "tforce_freight"] }
    },
    {
      "name": "International always DHL",
      "condition": { "destination_country_not": "US" },
      "action": { "prefer_carriers": ["dhl_express"] }
    },
    {
      "name": "Economy for low-value orders",
      "condition": { "order_value_lt": 25.00 },
      "action": { "prefer_services": ["*_ground", "*_economy"] }
    }
  ]
}
```

---

## 5. Label Management

### 5.1 Label Generation

karrio Cloud generates shipping labels in multiple formats:

| Format | Use Case |
|--------|----------|
| **PDF** | Standard desktop/laser printing |
| **ZPL** | Thermal label printers (Zebra) |
| **PNG** | Web display and mobile |

Labels are returned as base64-encoded strings in the OSP response and are also accessible via a persistent URL:

```
GET /osp/v1/shipments/{id}/label
```

### 5.2 Label Storage

All generated labels are stored by karrio Cloud for the retention period (configurable, default 90 days). Labels can be re-downloaded at any time during the retention period.

### 5.3 Batch Label Generation

For high-volume shippers, karrio Cloud supports batch shipment creation:

```json
POST /api/v1/shipments/batch
{
  "shipments": [
    { "service": "ups_ground", "shipper": {...}, "recipient": {...}, "parcels": [...] },
    { "service": "ups_ground", "shipper": {...}, "recipient": {...}, "parcels": [...] },
    { "service": "fedex_express", "shipper": {...}, "recipient": {...}, "parcels": [...] }
  ]
}
```

Batch operations are processed in parallel and return individual results for each shipment.

### 5.4 Document Management

Beyond labels, karrio Cloud manages:

| Document | Description |
|----------|-------------|
| Commercial invoices | Auto-generated for international shipments |
| Customs forms | CN22/CN23 forms where required |
| Manifests | End-of-day SCAN forms |
| Packing slips | Generated from parcel item data |

---

## 6. Webhook Aggregation

### 6.1 Unified Event Stream

Instead of managing webhook subscriptions with each carrier individually, karrio Cloud provides a single webhook stream that aggregates events from all carriers:

```
FedEx tracking update ──┐
UPS tracking update   ──┤
DHL tracking update   ──┼──> karrio Cloud ──> Your webhook endpoint
USPS tracking update  ──┤    (normalized     (single URL, single
Carrier N update      ──┘     OSP events)      HMAC secret)
```

### 6.2 Event Normalization

Carrier-specific events are normalized to OSP webhook events (see [OSP-CORE.md Section 7](./OSP-CORE.md#7-webhooks)):

- All tracking statuses mapped to `TrackingStatus` enum
- All timestamps converted to ISO 8601
- All carrier-specific codes translated to OSP codes
- Consistent event envelope with HMAC signing

### 6.3 Webhook Configuration

Configure webhooks via the karrio Dashboard or API:

```json
POST /api/v1/webhooks
{
  "url": "https://your-app.example.com/webhooks/osp",
  "enabled_events": [
    "tracking.updated",
    "tracking.delivered",
    "tracking.exception",
    "shipment.created",
    "shipment.cancelled"
  ],
  "description": "Production tracking updates"
}
```

Response includes the signing secret:

```json
{
  "id": "wh_abc123",
  "url": "https://your-app.example.com/webhooks/osp",
  "secret": "whsec_xxxxxxxxxxxxxxxxxxxx",
  "enabled_events": ["tracking.updated", "tracking.delivered", "..."],
  "active": true
}
```

### 6.4 Automatic Tracking Polling

karrio Cloud automatically polls carriers for tracking updates at configurable intervals. Merchants don't need to implement their own polling — they just subscribe to webhook events and receive push notifications.

| Tracking Age | Poll Frequency |
|-------------|----------------|
| < 24 hours | Every 2 hours |
| 1-7 days | Every 4 hours |
| 7-30 days | Every 12 hours |
| > 30 days | Daily |
| Delivered | Stop polling |

---

## 7. MCP Gateway

### 7.1 Hosted MCP Endpoint

karrio Cloud provides a hosted MCP server endpoint, eliminating the need for merchants to run their own MCP server:

```
MCP Client (Claude, ChatGPT, etc.)
       │
       ▼
  Streamable HTTP
  POST https://mcp.karrio.io/osp
  Authorization: Bearer osp_key_xxx
       │
       ▼
  karrio Cloud MCP Server
  (processes osp/* tool calls)
       │
       ▼
  karrio Backend
  (routes to carriers)
```

### 7.2 Configuration

**Claude Desktop** (remote MCP):
```json
{
  "mcpServers": {
    "osp": {
      "url": "https://mcp.karrio.io/osp",
      "headers": {
        "Authorization": "Bearer osp_key_xxxxxxxxxxxx"
      }
    }
  }
}
```

**Claude Code** (remote MCP):
```json
{
  "mcpServers": {
    "osp": {
      "url": "https://mcp.karrio.io/osp",
      "headers": {
        "Authorization": "Bearer osp_key_xxxxxxxxxxxx"
      }
    }
  }
}
```

### 7.3 Self-Hosted MCP Alternative

For merchants who prefer self-hosted infrastructure, the `@karrio/mcp` package can be pointed at any karrio instance (cloud or self-hosted):

```bash
# Self-hosted karrio instance
KARRIO_API_URL=https://your-karrio.example.com KARRIO_API_KEY=key_xxx npx @karrio/mcp

# karrio Cloud
KARRIO_API_URL=https://api.karrio.io KARRIO_API_KEY=osp_key_xxx npx @karrio/mcp
```

---

## 8. Pricing Model

### 8.1 Concept

karrio Cloud follows the Stripe pricing philosophy: **charge per transaction, not per carrier**.

| Component | Model |
|-----------|-------|
| **Label transactions** | Per-label fee (e.g., $0.05/label) |
| **Rate queries** | Free (encourages rate shopping) |
| **Tracking** | Free (included with labels) |
| **API calls** | Rate-limited by plan, not metered |
| **MCP access** | Included in all plans |

### 8.2 Plan Tiers (Conceptual)

| Tier | Labels/month | Rate Queries | Carriers | MCP Access | Support |
|------|-------------|-------------|----------|------------|---------|
| **Starter** | 500 | Unlimited | 3 | Included | Community |
| **Growth** | 5,000 | Unlimited | 10 | Included | Email |
| **Business** | 50,000 | Unlimited | Unlimited | Included | Priority |
| **Enterprise** | Unlimited | Unlimited | Unlimited | Included | Dedicated |

### 8.3 Self-Hosted Option

karrio is open-source (Apache 2.0). Merchants can self-host the complete stack at no per-transaction cost. karrio Cloud is the managed convenience layer — pay for infrastructure, support, and carrier connection management rather than building it yourself.

| Self-Hosted | karrio Cloud |
|-------------|-------------|
| Free (Apache 2.0) | Per-label pricing |
| You manage infrastructure | Managed infrastructure |
| You update carrier connectors | Automatic updates |
| You handle carrier API changes | Handled for you |
| Community support | Paid support tiers |

---

## Appendix: Getting Started with karrio Cloud

### Step 1: Create an Account

Sign up at [karrio.io](https://karrio.io) and create an organization.

### Step 2: Connect Carriers

In the Dashboard, go to **Carriers** → **Connect** and add your carrier accounts (FedEx, UPS, DHL, etc.).

### Step 3: Get Your API Key

Go to **Settings** → **API Keys** → **Create Key**. Your key will start with `osp_key_`.

### Step 4: Make Your First OSP Call

```bash
curl -X POST https://api.karrio.io/osp/v1/rates \
  -H "Authorization: Bearer osp_key_xxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": { "postal_code": "10001", "country_code": "US" },
    "recipient": { "postal_code": "90210", "country_code": "US" },
    "parcels": [{ "weight": 5, "weight_unit": "LB" }]
  }'
```

### Step 5: Connect to AI Agents

Add the karrio Cloud MCP endpoint to your AI agent configuration:

```json
{
  "mcpServers": {
    "osp": {
      "url": "https://mcp.karrio.io/osp",
      "headers": { "Authorization": "Bearer osp_key_xxxxxxxxxxxx" }
    }
  }
}
```

Your AI agent can now rate shop, create labels, and track packages across all your connected carriers.
