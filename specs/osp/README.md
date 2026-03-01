# Open Shipping Protocol (OSP) v0.1

**An open standard for shipping operations in the age of agentic commerce.**

| Field | Value |
|-------|-------|
| Version | 0.1 (Draft) |
| License | Apache 2.0 |
| Status | Draft Specification |
| Governance | Linux Foundation-style open governance |
| Reference Implementation | [karrio](https://github.com/karrioapi/karrio) |

---

## Executive Summary

The Open Shipping Protocol (OSP) defines a unified interface for shipping operations — rating, label creation, tracking, pickups, manifests, and returns — across all carriers worldwide. OSP replaces fragmented EDI/SOAP integrations with a modern, JSON-native protocol designed for both traditional REST consumption and AI-agent interaction via the Model Context Protocol (MCP).

**For a carrier VP**: OSP is to shipping what ISO 8583 is to payments. Implement one protocol, and your services are instantly accessible to every commerce platform, ERP system, and AI agent in the ecosystem. No more maintaining bespoke integrations for each customer. No more SOAP/WSDL tooling. One clean JSON interface, eight operations, immediate interoperability.

**For a platform engineer**: OSP gives you a single integration point for 100+ carriers. Replace your spaghetti of carrier SDKs with one protocol. Get rate quotes in 3 lines of code. Ship packages in 5. Track anything with a tracking number.

### Quick Start: Get a Rate Quote in 30 Seconds

```bash
curl -X POST https://api.karrio.io/osp/v1/rates \
  -H "Authorization: Bearer osp_key_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": {
      "postal_code": "10001",
      "country_code": "US",
      "city": "New York",
      "state_code": "NY"
    },
    "recipient": {
      "postal_code": "90210",
      "country_code": "US",
      "city": "Beverly Hills",
      "state_code": "CA"
    },
    "parcels": [{
      "weight": 5.0,
      "weight_unit": "LB",
      "length": 10,
      "width": 8,
      "height": 6,
      "dimension_unit": "IN"
    }]
  }'
```

Or via MCP (for AI agents):

```json
{
  "method": "tools/call",
  "params": {
    "name": "osp/get_rates",
    "arguments": {
      "shipper": { "postal_code": "10001", "country_code": "US" },
      "recipient": { "postal_code": "90210", "country_code": "US" },
      "parcels": [{ "weight": 5.0, "weight_unit": "LB" }]
    }
  }
}
```

---

## How OSP Relates to UCP, ACP, and MCP

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC COMMERCE STACK                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  UCP (Universal Commerce Protocol)                   │   │
│  │  Product discovery, catalog, checkout, orders        │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│           ┌───────────────┼───────────────┐                │
│           ▼               ▼               ▼                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  ACP          │ │  OSP          │ │  Other        │       │
│  │  (Agent       │ │  (Open        │ │  Extensions   │       │
│  │  Commerce     │ │  Shipping     │ │               │       │
│  │  Protocol)    │ │  Protocol)    │ │               │       │
│  │              │ │              │ │               │       │
│  │  Payments    │ │  Fulfillment │ │               │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│           │               │                                 │
│           └───────┬───────┘                                │
│                   ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MCP (Model Context Protocol)                        │   │
│  │  Universal transport layer for all protocols         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Protocol | Role | Relationship to OSP |
|----------|------|---------------------|
| **MCP** | Transport layer | OSP uses MCP as its first-class transport for AI agent communication |
| **UCP** | Commerce orchestration | OSP is the fulfillment extension — UCP hands off to OSP after checkout |
| **ACP** | Payment processing | ACP handles payment, OSP handles the physical shipment that follows |
| **OSP** | Shipping operations | The standard for rates, labels, tracking, pickups, manifests, returns |

---

## Specification Documents

### Core

| Document | Description |
|----------|-------------|
| [OSP-CORE.md](./OSP-CORE.md) | **The main specification.** Data models, all 8 operations (REST + MCP), authentication, error handling, webhooks, extension model, versioning. Start here. |
| [OSP-MCP.md](./OSP-MCP.md) | Complete MCP binding. Tool input schemas, resource definitions, transport configuration, auth in MCP context. |

### Adoption Guides

| Document | Description |
|----------|-------------|
| [OSP-CARRIER-ADAPTER.md](./OSP-CARRIER-ADAPTER.md) | Guide for FedEx, UPS, DHL, Geopost, and other carriers to implement OSP. Four adoption paths, conformance matrix, field mapping. |
| [OSP-COMMERCE-INTEGRATION.md](./OSP-COMMERCE-INTEGRATION.md) | Integration patterns for Shopify, WooCommerce, MedusaJS, Saleor, Magento, and generic commerce hooks. |

### Ecosystem

| Document | Description |
|----------|-------------|
| [OSP-UCP-ACP-COMPATIBILITY.md](./OSP-UCP-ACP-COMPATIBILITY.md) | How OSP, UCP, and ACP compose. Shared types, handoff patterns, end-to-end agent workflow example. |
| [OSP-CLOUD-GATEWAY.md](./OSP-CLOUD-GATEWAY.md) | karrio Cloud as a hosted OSP gateway — the "Stripe for shipping" model. Multi-carrier management, rate optimization, label management. |

---

## Design Principles

1. **MCP-first**: Every operation is defined as both a REST endpoint and an MCP Tool. AI agents are first-class consumers, not an afterthought.
2. **Clean break from EDI/SOAP**: No XML. No WSDL. No EDI segment parsing. Pure JSON, modern auth, webhook-driven events.
3. **Stable core + extensions**: The 8 core operations and base schemas are stable. Carrier-specific and domain-specific features use the `x_` extension prefix.
4. **Domestic and international**: First-class support for customs declarations, duties, HS codes, and cross-border compliance alongside domestic shipping.
5. **Bottom-up adoption**: Commerce platforms (Shopify, WooCommerce, Medusa) adopt first. Carriers follow as demand grows. No top-down mandate required.

## Reference Implementation

[karrio](https://github.com/karrioapi/karrio) is the canonical reference implementation of the Open Shipping Protocol. karrio supports 100+ carriers and provides both self-hosted and cloud-hosted deployment options.

- **Self-hosted**: Run the full OSP-compliant server on your infrastructure
- **karrio Cloud**: Managed OSP gateway at [karrio.io](https://karrio.io) — like Stripe for shipping

## License

This specification is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

The "Open Shipping Protocol" and "OSP" names are trademarks of the OSP project. The "karrio" name and logo are trademarks of karrio. Use of these marks is subject to the respective trademark policies.

## Contributing

This specification is developed in the open. Contributions are welcome via pull requests to the [karrio repository](https://github.com/karrioapi/karrio).

To propose changes:
1. Open an issue describing the problem or enhancement
2. Reference the relevant spec section
3. Submit a PR with the proposed changes
4. Changes to core schemas or operations require consensus from maintainers
