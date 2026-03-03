# OSP-UCP-ACP-COMPATIBILITY: Protocol Composition

**Version**: 0.1 (Draft)
**License**: Apache 2.0
**Prerequisite**: [OSP-CORE.md](./OSP-CORE.md)

---

## Table of Contents

1. [Protocol Landscape](#1-protocol-landscape)
2. [How OSP, UCP, and ACP Compose](#2-how-osp-ucp-and-acp-compose)
3. [OSP as UCP Fulfillment Extension](#3-osp-as-ucp-fulfillment-extension)
4. [ACP to OSP Handoff](#4-acp-to-osp-handoff)
5. [Shared Types](#5-shared-types)
6. [End-to-End Integration Example](#6-end-to-end-integration-example)

---

## 1. Protocol Landscape

The agentic commerce stack is composed of three complementary protocols, each handling a distinct domain. All three use MCP as their transport layer.

```
┌───────────────────────────────────────────────────────────────────┐
│                     AI AGENT (Claude, etc.)                       │
│                                                                   │
│  "Buy a blue widget, pay with my card, ship it overnight"        │
│                                                                   │
└────────────┬──────────────────┬──────────────────┬────────────────┘
             │                  │                  │
             ▼                  ▼                  ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │     UCP      │  │     ACP      │  │     OSP      │
     │  Universal   │  │    Agent     │  │    Open      │
     │  Commerce    │  │  Commerce    │  │  Shipping    │
     │  Protocol    │  │  Protocol    │  │  Protocol    │
     │              │  │              │  │              │
     │  Discovery   │  │  Payments    │  │  Rating      │
     │  Catalog     │  │  Checkout    │  │  Shipping    │
     │  Cart        │  │  Invoicing   │  │  Tracking    │
     │  Orders      │  │  Refunds     │  │  Returns     │
     └──────────────┘  └──────────────┘  └──────────────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │         MCP           │
                    │  Model Context        │
                    │  Protocol             │
                    │                       │
                    │  JSON-RPC transport   │
                    │  Tool definitions     │
                    │  Resource access      │
                    └───────────────────────┘
```

| Protocol | Domain | Maintained By | Relationship to OSP |
|----------|--------|---------------|---------------------|
| **UCP** | Product discovery, catalog, cart, checkout, orders | Google / Shopify | OSP is the fulfillment extension of UCP |
| **ACP** | Payments, checkout sessions, invoicing, refunds | OpenAI / Stripe | ACP handles payment; OSP handles the physical shipment that follows |
| **OSP** | Rating, labels, tracking, pickups, manifests, returns | karrio / Open governance | The shipping/fulfillment protocol |
| **MCP** | Agent-to-tool communication transport | Anthropic | The wire protocol all three use |

---

## 2. How OSP, UCP, and ACP Compose

The three protocols compose along the natural boundaries of a commerce transaction:

```
Customer Journey           Protocol Boundary          Data Flow
─────────────────         ──────────────────         ──────────────

1. Browse products         ───── UCP ─────────>      ucp/search_products
                                                     ucp/get_product

2. Add to cart             ───── UCP ─────────>      ucp/add_to_cart
                                                     ucp/get_cart

3. Get shipping options    ───── UCP → OSP ───>      osp/get_rates
   (UCP calls OSP)                                   (returns to UCP cart)

4. Select shipping         ───── UCP ─────────>      ucp/update_cart
                                                     (stores OSP service code)

5. Checkout & pay          ───── UCP → ACP ───>      acp/create_checkout
                                                     acp/process_payment

6. Create shipment         ───── OSP ─────────>      osp/create_shipment
   (payment confirmed)                               (uses service from step 4)

7. Track package           ───── OSP ─────────>      osp/track_shipment

8. Return item             ───── OSP ─────────>      osp/create_return
                           ───── ACP ─────────>      acp/create_refund
```

### Composition Rules

1. **UCP orchestrates**: UCP is the top-level orchestrator. It calls OSP for shipping rates during checkout and triggers OSP shipment creation after order confirmation.
2. **ACP is independent**: ACP handles payment without knowing about shipping. The agent coordinates: payment confirmation triggers shipment creation.
3. **OSP is stateless**: OSP does not need to know about UCP orders or ACP payments. It receives shipping requests and returns shipping responses. Correlation is done via `reference` and `metadata` fields.
4. **MCP is the glue**: All three protocols communicate via MCP Tools. An AI agent with access to all three MCP servers can execute a complete commerce transaction.

---

## 3. OSP as UCP Fulfillment Extension

### 3.1 UCP Checkout Shipping Step

When a UCP checkout flow needs shipping rates, it calls OSP. The UCP server acts as an OSP client:

```
UCP Server                           OSP Server
──────────                           ──────────
ucp/get_cart
  → cart includes items
  → cart has shipping_address
  → cart needs shipping_options
                    │
                    ▼
              osp/get_rates ────────────────────>  OSP processes
              {                                    rate request
                shipper: merchant_address,          against all
                recipient: cart.shipping_address,   connected
                parcels: cart_items_to_parcels(),    carriers
              }                                         │
                    ◄──────────────────────────────────┘
                    rates: [
                      { service: "ups_ground", total_charge: 8.99 },
                      { service: "fedex_express", total_charge: 24.50 },
                    ]
                    │
                    ▼
ucp/update_cart
  → shipping_method: "ups_ground"
  → shipping_cost: 8.99
```

### 3.2 UCP Order to OSP Shipment

After a UCP order is placed and payment is confirmed (via ACP), the fulfillment step creates an OSP shipment:

```json
// UCP order object (simplified)
{
  "id": "ucp_order_abc123",
  "status": "confirmed",
  "items": [
    { "product_id": "prod_1", "title": "Blue Widget", "quantity": 2, "price": 29.99 }
  ],
  "shipping_address": {
    "name": "Jane Smith",
    "address1": "456 Oak Ave",
    "city": "Beverly Hills",
    "state": "CA",
    "zip": "90210",
    "country": "US"
  },
  "shipping_method": "ups_ground",
  "shipping_cost": 8.99,
  "payment_id": "acp_pay_xyz789"
}
```

The agent creates an OSP shipment:

```json
// osp/create_shipment call
{
  "service": "ups_ground",
  "shipper": {
    "person_name": "Acme Store",
    "address_line1": "123 Main St",
    "city": "New York",
    "state_code": "NY",
    "postal_code": "10001",
    "country_code": "US"
  },
  "recipient": {
    "person_name": "Jane Smith",
    "address_line1": "456 Oak Ave",
    "city": "Beverly Hills",
    "state_code": "CA",
    "postal_code": "90210",
    "country_code": "US"
  },
  "parcels": [{
    "weight": 2.5,
    "weight_unit": "LB",
    "items": [{
      "title": "Blue Widget",
      "quantity": 2,
      "value_amount": 29.99,
      "value_currency": "USD"
    }]
  }],
  "reference": "ucp_order_abc123",
  "metadata": {
    "ucp_order_id": "ucp_order_abc123",
    "acp_payment_id": "acp_pay_xyz789"
  }
}
```

### 3.3 Fulfillment Status Feedback

OSP tracking updates flow back to UCP to update order status:

| OSP TrackingStatus | UCP Order Status |
|--------------------|------------------|
| `info_received` | `processing` |
| `in_transit` | `shipped` |
| `out_for_delivery` | `shipped` |
| `delivered` | `delivered` |
| `delivery_failed` | `needs_attention` |
| `returned` | `returned` |

This mapping is implemented either by the agent polling OSP tracking or by an OSP webhook handler updating the UCP order.

---

## 4. ACP to OSP Handoff

### 4.1 Payment Confirmation Triggers Shipment

The ACP-to-OSP handoff is event-driven. When ACP confirms a payment, the agent (or an automated workflow) creates the corresponding OSP shipment.

```
ACP Server                  Agent                    OSP Server
──────────                  ─────                    ──────────

acp/process_payment ─────>
  payment_id: pay_xyz789
  amount: 68.97
  status: "succeeded"
                            │
                            │ Payment confirmed.
                            │ Now create shipment.
                            │
                            ├─────────────────────>  osp/create_shipment
                            │                         service: "ups_ground"
                            │                         metadata: {
                            │                           acp_payment_id: "pay_xyz789"
                            │                         }
                            │
                            │◄─────────────────────  shipment created
                            │                         tracking: "1Z999AA10..."
                            │
                            ▼
  Agent stores tracking number
  on the UCP order for customer
  visibility.
```

### 4.2 Refund on Return

When a customer returns a package (OSP), the agent triggers a refund (ACP):

```
OSP: osp/create_return
  → tracking.delivered (return received)

Agent: "Return received. Process refund."

ACP: acp/create_refund
  → payment_id: "pay_xyz789"
  → amount: 59.98
  → reason: "returned"
  → metadata: { osp_return_id: "shp_ret_abc123" }
```

---

## 5. Shared Types

OSP, UCP, and ACP share several data types. This section defines the canonical mapping between them.

### 5.1 Address

| OSP Field | UCP Equivalent | ACP Equivalent |
|-----------|---------------|----------------|
| `person_name` | `name` | `name` |
| `company_name` | `company` | `company` |
| `address_line1` | `address1` | `line1` |
| `address_line2` | `address2` | `line2` |
| `city` | `city` | `city` |
| `state_code` | `state` / `province` | `state` |
| `postal_code` | `zip` / `postal_code` | `postal_code` |
| `country_code` | `country` | `country` |
| `email` | `email` | `email` |
| `phone_number` | `phone` | `phone` |

### 5.2 Money / Currency

| OSP | UCP | ACP |
|-----|-----|-----|
| `total_charge: 12.50` (decimal) | `price: 1250` (cents, integer) | `amount: 1250` (cents, integer) |
| `currency: "USD"` | `currency: "USD"` | `currency: "usd"` (lowercase) |

**Conversion rule**: OSP uses decimal amounts. UCP and ACP typically use integer amounts in the smallest currency unit (cents). Integrations must convert between representations.

```typescript
// OSP → ACP/UCP
const amountInCents = Math.round(ospRate.total_charge * 100);

// ACP/UCP → OSP
const amountInDecimal = acpPayment.amount / 100;
```

### 5.3 Line Items / Products

| OSP Commodity | UCP Line Item | ACP Line Item |
|--------------|---------------|---------------|
| `title` | `title` / `name` | `description` |
| `sku` | `sku` | `sku` |
| `quantity` | `quantity` | `quantity` |
| `value_amount` | `price` | `amount` |
| `value_currency` | `currency` | `currency` |
| `hs_code` | *(n/a)* | *(n/a)* |
| `origin_country` | *(n/a)* | *(n/a)* |
| `weight` | `weight` | *(n/a)* |

### 5.4 Identifiers

The `metadata` field is the standard mechanism for cross-protocol identifier correlation:

```json
// On an OSP shipment
{
  "metadata": {
    "ucp_order_id": "ucp_order_abc123",
    "acp_payment_id": "acp_pay_xyz789"
  }
}

// On an ACP refund
{
  "metadata": {
    "ucp_order_id": "ucp_order_abc123",
    "osp_return_id": "shp_ret_abc123"
  }
}
```

---

## 6. End-to-End Integration Example

This example shows a complete agentic commerce transaction where an AI agent uses UCP to browse and buy, ACP to pay, and OSP to ship.

### 6.1 Agent Prompt

> "Find a blue widget under $50, ship it to Jane Smith at 456 Oak Ave, Beverly Hills CA 90210. Use the cheapest shipping option. Pay with my default card."

### 6.2 Agent Execution Flow

```
Step  Protocol  MCP Tool Call                    Result
────  ────────  ─────────────────────────────    ──────────────────────────────────
 1    UCP       ucp/search_products              Found: Blue Widget, $29.99
                { query: "blue widget",
                  max_price: 50.00 }

 2    UCP       ucp/add_to_cart                  Cart: 1× Blue Widget = $29.99
                { product_id: "prod_1",
                  quantity: 1 }

 3    OSP       osp/get_rates                    Rates:
                { shipper: merchant_addr,          - ups_ground: $8.99 (5 days)
                  recipient: jane_addr,            - fedex_ground: $9.50 (4 days)
                  parcels: [{ weight: 1.2,         - usps_priority: $12.30 (3 days)
                    weight_unit: "LB" }] }

 4    UCP       ucp/update_cart                  Cart updated:
                { shipping_method: "ups_ground",   Subtotal: $29.99
                  shipping_cost: 8.99 }            Shipping: $8.99
                                                   Total: $38.98

 5    ACP       acp/create_checkout              Checkout session created
                { amount: 3898,
                  currency: "usd",
                  payment_method: "default" }

 6    ACP       acp/confirm_payment              Payment confirmed
                { checkout_id: "cs_abc" }          payment_id: "pay_xyz789"

 7    UCP       ucp/place_order                  Order confirmed
                { cart_id: "cart_123",             order_id: "ucp_order_abc123"
                  payment_id: "pay_xyz789" }

 8    OSP       osp/create_shipment              Shipment created
                { service: "ups_ground",           tracking: "1Z999AA10..."
                  shipper: merchant_addr,           label: (base64 PDF)
                  recipient: jane_addr,
                  parcels: [...],
                  reference: "ucp_order_abc123",
                  metadata: {
                    ucp_order_id: "ucp_order_abc123",
                    acp_payment_id: "pay_xyz789"
                  } }

 9    OSP       osp/track_shipment               Status: in_transit
                { tracking_number:                 ETA: March 7, 2026
                  "1Z999AA10..." }
```

### 6.3 Agent Response to User

> "Done! I ordered your Blue Widget ($29.99) and shipped it via UPS Ground ($8.99) to 456 Oak Ave, Beverly Hills, CA 90210. Your tracking number is 1Z999AA10... and it should arrive by March 7th. Total charged to your card: $38.98."

### 6.4 Subsequent Interactions

**Tracking update** (agent checks proactively or user asks):
```
Agent → osp/track_shipment { tracking_number: "1Z999AA10..." }
OSP   → { status: "out_for_delivery", events: [...] }
Agent → "Your Blue Widget is out for delivery today!"
```

**Return request**:
```
Agent → osp/create_return { shipment_id: "shp_abc123" }
OSP   → { tracking_number: "1Z999AA20...", label_url: "..." }
Agent → "I've created a return label. Print it here: [label_url]. Once we receive the return, I'll process your refund."

(Later, after return delivered)
Agent → acp/create_refund { payment_id: "pay_xyz789", amount: 2999 }
ACP   → { refund_id: "re_abc", status: "succeeded" }
Agent → "Your refund of $29.99 has been processed. It should appear in 3-5 business days."
```

---

## Appendix: Protocol Version Compatibility

| OSP Version | UCP Compatibility | ACP Compatibility | MCP Version |
|-------------|-------------------|-------------------|-------------|
| 0.1 (this spec) | UCP v1 (draft) | ACP v1 (draft) | MCP 2025-06-18+ |

All three protocols are in active development. This compatibility document will be updated as the protocols stabilize. The composition patterns described here are designed to be resilient to minor version changes in any individual protocol.
