# OSP-MCP: Model Context Protocol Binding

**Version**: 0.1 (Draft)
**License**: Apache 2.0
**Prerequisite**: [OSP-CORE.md](./OSP-CORE.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [MCP Server Metadata](#2-mcp-server-metadata)
3. [Tool Definitions](#3-tool-definitions)
4. [Resource Definitions](#4-resource-definitions)
5. [Transport Configuration](#5-transport-configuration)
6. [Authentication in MCP Context](#6-authentication-in-mcp-context)
7. [Error Handling in MCP](#7-error-handling-in-mcp)
8. [Relationship to karrio MCP Server](#8-relationship-to-karrio-mcp-server)

---

## 1. Overview

MCP (Model Context Protocol) is the first-class transport for the Open Shipping Protocol. Every OSP operation defined in [OSP-CORE.md](./OSP-CORE.md) has a corresponding MCP Tool definition. Additionally, OSP exposes reference data (carrier catalogs, service catalogs) as MCP Resources.

This document provides the complete MCP binding — every Tool input schema in full JSON Schema, every Resource definition, and the transport and auth configuration required to connect an MCP client to an OSP-compliant server.

### Design Rationale

MCP is the required transport because:

1. **AI agents are primary consumers** — MCP is the standard protocol for AI agent tool use (Claude, ChatGPT, Gemini, Cursor, VS Code Copilot)
2. **Structured schemas** — MCP Tool input schemas give AI agents complete type information, reducing errors
3. **Tool annotations** — MCP metadata hints (`readOnlyHint`, `destructiveHint`) let agents make safe decisions about financial operations like label purchase
4. **Resources for context** — MCP Resources let agents reason about carrier capabilities before making API calls

### Namespace Convention

All OSP MCP Tools use the `osp/` namespace prefix:

```
osp/get_rates
osp/create_shipment
osp/track_shipment
```

This prevents collisions when an MCP client connects to multiple servers (e.g., an OSP server alongside a payment or commerce server).

---

## 2. MCP Server Metadata

An OSP-compliant MCP server MUST advertise the following metadata:

```json
{
  "name": "osp",
  "version": "0.1.0",
  "description": "Open Shipping Protocol — multi-carrier shipping operations for AI agents"
}
```

The `name` field MUST be `"osp"` for conforming implementations. Implementations MAY append a qualifier (e.g., `"osp-karrio"`, `"osp-fedex"`) if they implement only a subset of the protocol.

---

## 3. Tool Definitions

### 3.1 osp/get_rates

Fetch shipping rate quotes from one or more carriers.

**Annotations**:
```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "shipper": {
      "type": "object",
      "description": "Origin address",
      "properties": {
        "person_name": { "type": "string" },
        "company_name": { "type": "string" },
        "address_line1": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string", "description": "State or province code" },
        "postal_code": { "type": "string", "description": "ZIP or postal code" },
        "country_code": { "type": "string", "description": "ISO 3166-1 alpha-2 country code" }
      },
      "required": ["postal_code", "country_code"]
    },
    "recipient": {
      "type": "object",
      "description": "Destination address",
      "properties": {
        "person_name": { "type": "string" },
        "company_name": { "type": "string" },
        "address_line1": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string", "description": "State or province code" },
        "postal_code": { "type": "string", "description": "ZIP or postal code" },
        "country_code": { "type": "string", "description": "ISO 3166-1 alpha-2 country code" },
        "residential": { "type": "boolean", "default": false }
      },
      "required": ["postal_code", "country_code"]
    },
    "parcels": {
      "type": "array",
      "description": "Packages to ship",
      "items": {
        "type": "object",
        "properties": {
          "weight": { "type": "number", "description": "Package weight" },
          "weight_unit": { "type": "string", "enum": ["LB", "KG", "OZ", "G"], "default": "LB" },
          "length": { "type": "number", "description": "Package length" },
          "width": { "type": "number", "description": "Package width" },
          "height": { "type": "number", "description": "Package height" },
          "dimension_unit": { "type": "string", "enum": ["IN", "CM"], "default": "IN" },
          "packaging_type": { "type": "string" },
          "package_preset": { "type": "string" },
          "is_document": { "type": "boolean", "default": false },
          "description": { "type": "string" }
        },
        "required": ["weight", "weight_unit"]
      },
      "minItems": 1
    },
    "services": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Filter by specific service codes (e.g., ['fedex_ground', 'ups_ground']). Omit for all available services."
    },
    "carrier_names": {
      "type": "string",
      "description": "Comma-separated carrier slugs to filter (e.g., 'fedex,ups,dhl_express'). Omit for all connected carriers."
    },
    "max_results": {
      "type": "integer",
      "default": 10,
      "description": "Maximum number of rates to return"
    },
    "sort_by": {
      "type": "string",
      "enum": ["price", "delivery_time"],
      "default": "price",
      "description": "Sort rates by price (cheapest first) or delivery time (fastest first)"
    },
    "reference": { "type": "string", "description": "Your reference for this rate request" },
    "options": { "type": "object", "description": "Carrier-specific options" }
  },
  "required": ["shipper", "recipient", "parcels"]
}
```

---

### 3.2 osp/create_shipment

Create a shipment and purchase a shipping label. This is a billable operation.

**Annotations**:
```json
{
  "readOnlyHint": false,
  "destructiveHint": true,
  "idempotentHint": false,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "service": { "type": "string", "description": "Carrier service code (e.g., 'fedex_ground')" },
    "shipper": {
      "type": "object",
      "description": "Sender address",
      "properties": {
        "person_name": { "type": "string", "description": "Contact name" },
        "company_name": { "type": "string" },
        "address_line1": { "type": "string", "description": "Street address" },
        "address_line2": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string" },
        "postal_code": { "type": "string" },
        "country_code": { "type": "string", "description": "ISO 3166-1 alpha-2" },
        "email": { "type": "string" },
        "phone_number": { "type": "string" },
        "residential": { "type": "boolean", "default": false },
        "federal_tax_id": { "type": "string" },
        "state_tax_id": { "type": "string" }
      },
      "required": ["address_line1", "postal_code", "country_code"]
    },
    "recipient": {
      "type": "object",
      "description": "Recipient address",
      "properties": {
        "person_name": { "type": "string", "description": "Contact name" },
        "company_name": { "type": "string" },
        "address_line1": { "type": "string", "description": "Street address" },
        "address_line2": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string" },
        "postal_code": { "type": "string" },
        "country_code": { "type": "string", "description": "ISO 3166-1 alpha-2" },
        "email": { "type": "string" },
        "phone_number": { "type": "string" },
        "residential": { "type": "boolean", "default": false },
        "federal_tax_id": { "type": "string" },
        "state_tax_id": { "type": "string" }
      },
      "required": ["address_line1", "postal_code", "country_code"]
    },
    "parcels": {
      "type": "array",
      "description": "Packages to ship",
      "items": {
        "type": "object",
        "properties": {
          "weight": { "type": "number" },
          "weight_unit": { "type": "string", "enum": ["LB", "KG", "OZ", "G"], "default": "LB" },
          "length": { "type": "number" },
          "width": { "type": "number" },
          "height": { "type": "number" },
          "dimension_unit": { "type": "string", "enum": ["IN", "CM"], "default": "IN" },
          "packaging_type": { "type": "string" },
          "package_preset": { "type": "string" },
          "is_document": { "type": "boolean", "default": false },
          "description": { "type": "string" },
          "content": { "type": "string" },
          "reference_number": { "type": "string" },
          "items": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "title": { "type": "string" },
                "sku": { "type": "string" },
                "quantity": { "type": "integer", "default": 1 },
                "weight": { "type": "number" },
                "weight_unit": { "type": "string", "enum": ["LB", "KG", "OZ", "G"] },
                "value_amount": { "type": "number" },
                "value_currency": { "type": "string" },
                "hs_code": { "type": "string" },
                "origin_country": { "type": "string" }
              },
              "required": ["title", "quantity"]
            }
          }
        },
        "required": ["weight", "weight_unit"]
      },
      "minItems": 1
    },
    "customs": {
      "type": "object",
      "description": "Customs declaration (required for international shipments)",
      "properties": {
        "commodities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "quantity": { "type": "integer" },
              "weight": { "type": "number" },
              "weight_unit": { "type": "string", "enum": ["LB", "KG", "OZ", "G"] },
              "value_amount": { "type": "number" },
              "value_currency": { "type": "string" },
              "hs_code": { "type": "string" },
              "origin_country": { "type": "string" }
            },
            "required": ["title", "quantity"]
          }
        },
        "content_type": { "type": "string", "enum": ["merchandise", "documents", "gift", "sample", "return_merchandise", "other"] },
        "incoterm": { "type": "string", "enum": ["DDP", "DDU", "DAP", "CFR", "CIF", "CPT", "CIP", "EXW", "FCA", "FAS", "FOB"] },
        "invoice": { "type": "string" },
        "certify": { "type": "boolean" },
        "signer": { "type": "string" },
        "duty": {
          "type": "object",
          "properties": {
            "paid_by": { "type": "string", "enum": ["sender", "recipient", "third_party"], "default": "sender" },
            "currency": { "type": "string" },
            "account_number": { "type": "string" },
            "declared_value": { "type": "number" }
          }
        }
      },
      "required": ["commodities"]
    },
    "payment": {
      "type": "object",
      "properties": {
        "paid_by": { "type": "string", "enum": ["sender", "recipient", "third_party"], "default": "sender" },
        "currency": { "type": "string" },
        "account_number": { "type": "string" }
      }
    },
    "label_type": { "type": "string", "enum": ["PDF", "ZPL", "PNG"], "default": "PDF" },
    "reference": { "type": "string", "description": "Your reference (e.g., order number)" },
    "options": { "type": "object", "description": "Carrier-specific options (signature, insurance, etc.)" },
    "metadata": { "type": "object", "description": "Arbitrary key-value metadata to store with the shipment" }
  },
  "required": ["service", "shipper", "recipient", "parcels"]
}
```

---

### 3.3 osp/get_shipment

Retrieve details of an existing shipment by ID.

**Annotations**:
```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": false
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "shipment_id": { "type": "string", "description": "OSP shipment identifier (e.g., 'shp_abc123')" }
  },
  "required": ["shipment_id"]
}
```

---

### 3.4 osp/cancel_shipment

Cancel a shipment and void its label. This operation may not be reversible.

**Annotations**:
```json
{
  "readOnlyHint": false,
  "destructiveHint": true,
  "idempotentHint": true,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "shipment_id": { "type": "string", "description": "OSP shipment identifier to cancel" }
  },
  "required": ["shipment_id"]
}
```

---

### 3.5 osp/track_shipment

Track a package by tracking number with full event history.

**Annotations**:
```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "tracking_number": { "type": "string", "description": "Carrier tracking number" },
    "carrier_name": { "type": "string", "description": "Carrier slug (e.g., 'fedex', 'ups', 'dhl_express'). Optional if the server can auto-detect the carrier." }
  },
  "required": ["tracking_number"]
}
```

---

### 3.6 osp/schedule_pickup

Schedule a carrier pickup for one or more shipments.

**Annotations**:
```json
{
  "readOnlyHint": false,
  "destructiveHint": true,
  "idempotentHint": false,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "carrier_name": { "type": "string", "description": "Carrier slug (e.g., 'fedex', 'ups')" },
    "pickup_date": { "type": "string", "description": "Pickup date (YYYY-MM-DD)" },
    "ready_time": { "type": "string", "description": "Earliest pickup time (HH:MM)" },
    "closing_time": { "type": "string", "description": "Latest pickup time (HH:MM)" },
    "address": {
      "type": "object",
      "description": "Pickup address",
      "properties": {
        "person_name": { "type": "string" },
        "company_name": { "type": "string" },
        "address_line1": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string" },
        "postal_code": { "type": "string" },
        "country_code": { "type": "string" },
        "phone_number": { "type": "string" }
      },
      "required": ["address_line1", "postal_code", "country_code"]
    },
    "shipment_identifiers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Tracking numbers or shipment identifiers to include in the pickup"
    },
    "instruction": { "type": "string", "description": "Special instructions for the driver" },
    "package_location": { "type": "string", "description": "Where to find packages (e.g., 'Front Desk', 'Loading Dock')" },
    "parcels_count": { "type": "integer", "description": "Total number of parcels for pickup" }
  },
  "required": ["carrier_name", "pickup_date", "ready_time", "closing_time", "address"]
}
```

---

### 3.7 osp/create_manifest

Create an end-of-day manifest (SCAN form) for a batch of shipments.

**Annotations**:
```json
{
  "readOnlyHint": false,
  "destructiveHint": true,
  "idempotentHint": false,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "carrier_name": { "type": "string", "description": "Carrier slug" },
    "shipment_identifiers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of shipment identifiers to include in the manifest"
    },
    "address": {
      "type": "object",
      "description": "Pickup/origin address for the manifest",
      "properties": {
        "company_name": { "type": "string" },
        "address_line1": { "type": "string" },
        "city": { "type": "string" },
        "state_code": { "type": "string" },
        "postal_code": { "type": "string" },
        "country_code": { "type": "string" }
      },
      "required": ["address_line1", "postal_code", "country_code"]
    },
    "reference": { "type": "string", "description": "Your reference for this manifest" },
    "options": { "type": "object" }
  },
  "required": ["carrier_name", "shipment_identifiers", "address"]
}
```

---

### 3.8 osp/create_return

Create a return shipment label for an existing shipment.

**Annotations**:
```json
{
  "readOnlyHint": false,
  "destructiveHint": true,
  "idempotentHint": false,
  "openWorldHint": true
}
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "shipment_id": { "type": "string", "description": "OSP shipment identifier of the original outbound shipment" },
    "label_type": { "type": "string", "enum": ["PDF", "ZPL", "PNG"], "default": "PDF" },
    "reference": { "type": "string", "description": "Your reference for the return" },
    "options": { "type": "object", "description": "Carrier-specific return options" }
  },
  "required": ["shipment_id"]
}
```

---

## 4. Resource Definitions

MCP Resources provide read-only reference data that AI agents can access without making tool calls. This is a key differentiator for OSP — agents can reason about carrier capabilities and service options before making any billable API calls.

### 4.1 Carrier Catalog

**URI**: `osp://carriers`
**MIME Type**: `application/json`
**Description**: Complete catalog of connected carriers with their capabilities.

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "carriers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "carrier_name": { "type": "string", "description": "Carrier slug identifier" },
          "display_name": { "type": "string", "description": "Human-readable carrier name" },
          "carrier_id": { "type": "string", "description": "Carrier account identifier" },
          "active": { "type": "boolean" },
          "test_mode": { "type": "boolean" },
          "capabilities": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["rating", "shipping", "tracking", "pickup", "manifest", "returns"]
            },
            "description": "Operations this carrier supports"
          }
        }
      }
    }
  }
}
```

**Example**:
```json
{
  "carriers": [
    {
      "carrier_name": "fedex",
      "display_name": "FedEx",
      "carrier_id": "fedex-production",
      "active": true,
      "test_mode": false,
      "capabilities": ["rating", "shipping", "tracking", "pickup", "manifest", "returns"]
    },
    {
      "carrier_name": "ups",
      "display_name": "UPS",
      "carrier_id": "ups-production",
      "active": true,
      "test_mode": false,
      "capabilities": ["rating", "shipping", "tracking", "pickup", "manifest"]
    }
  ]
}
```

### 4.2 Carrier Details

**URI Template**: `osp://carriers/{carrier_name}`
**MIME Type**: `application/json`
**Description**: Detailed information for a specific carrier, including available services and supported options.

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "carrier_name": { "type": "string" },
    "display_name": { "type": "string" },
    "carrier_id": { "type": "string" },
    "active": { "type": "boolean" },
    "test_mode": { "type": "boolean" },
    "capabilities": { "type": "array", "items": { "type": "string" } },
    "services": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "service_code": { "type": "string" },
          "service_name": { "type": "string" },
          "description": { "type": "string" },
          "domestic": { "type": "boolean" },
          "international": { "type": "boolean" }
        }
      },
      "description": "Available shipping services"
    },
    "supported_options": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Supported shipping options (e.g., 'signature_required', 'saturday_delivery')"
    }
  }
}
```

### 4.3 Service Catalog

**URI**: `osp://services`
**MIME Type**: `application/json`
**Description**: Complete catalog of all available shipping services across all connected carriers.

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "services": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "carrier_name": { "type": "string" },
          "service_code": { "type": "string" },
          "service_name": { "type": "string" },
          "domestic": { "type": "boolean" },
          "international": { "type": "boolean" },
          "max_weight": { "type": "number" },
          "weight_unit": { "type": "string" }
        }
      }
    }
  }
}
```

### 4.4 Resource Fallback

Not all MCP clients support Resources (Cursor and ChatGPT do not as of this writing). OSP implementations SHOULD also expose a `osp/list_carriers` tool as a fallback:

```json
{
  "name": "osp/list_carriers",
  "description": "List all connected carriers and their capabilities. Use this to discover available carriers before shipping.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "annotations": {
    "readOnlyHint": true,
    "destructiveHint": false,
    "idempotentHint": true,
    "openWorldHint": false
  }
}
```

---

## 5. Transport Configuration

OSP MCP servers MUST support at least one of the following transports. Supporting both is RECOMMENDED.

### 5.1 stdio Transport

For local development and single-user scenarios. The MCP client launches the OSP server as a subprocess.

**Claude Desktop configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "osp": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://api.karrio.io",
        "KARRIO_API_KEY": "osp_key_xxxxxxxxxxxx"
      }
    }
  }
}
```

**Claude Code configuration** (`.claude/settings.json`):
```json
{
  "mcpServers": {
    "osp": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://api.karrio.io",
        "KARRIO_API_KEY": "osp_key_xxxxxxxxxxxx"
      }
    }
  }
}
```

**Cursor configuration** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "osp": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://api.karrio.io",
        "KARRIO_API_KEY": "osp_key_xxxxxxxxxxxx"
      }
    }
  }
}
```

### 5.2 Streamable HTTP Transport

For remote, multi-session access. The server runs as a persistent HTTP service.

**Endpoints**:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/mcp` | Create a new session or send requests |
| `GET` | `/mcp` | SSE streaming for an existing session |
| `DELETE` | `/mcp` | Terminate a session |
| `GET` | `/.well-known/mcp` | Server metadata and capability discovery |

**Session management**:
- Sessions are identified by the `mcp-session-id` header
- Session IDs are UUIDs generated by the server
- Each session maintains its own transport state

**Starting the server**:
```bash
npx @karrio/mcp --http --port 3100
```

**Server discovery** (`GET /.well-known/mcp`):
```json
{
  "name": "osp",
  "version": "0.1.0",
  "description": "Open Shipping Protocol MCP server",
  "transports": ["stdio", "streamable-http"],
  "capabilities": {
    "tools": true,
    "resources": true
  }
}
```

---

## 6. Authentication in MCP Context

### 6.1 stdio Transport

For stdio transport, authentication is provided via environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `KARRIO_API_KEY` or `OSP_API_KEY` | Yes | API key for authentication |
| `KARRIO_API_URL` or `OSP_API_URL` | Yes | Base URL of the OSP-compliant server |

The MCP server uses the API key to authenticate all requests to the backend OSP service.

### 6.2 Streamable HTTP Transport

For HTTP transport, the MCP client includes authentication in the initial HTTP request:

**API Key**:
```http
POST /mcp HTTP/1.1
Authorization: Bearer osp_key_xxxxxxxxxxxx
Content-Type: application/json
```

**OAuth 2.0**:
```http
POST /mcp HTTP/1.1
Authorization: Bearer osp_at_xxxxxxxxxxxx
Content-Type: application/json
```

The server validates the token on session creation. Subsequent requests within the same session are authenticated by the session ID.

### 6.3 Token Format

| Prefix | Type | Usage |
|--------|------|-------|
| `osp_key_` | API Key | Long-lived key for server-to-server |
| `osp_at_` | Access Token | Short-lived OAuth 2.0 access token |
| `osp_rt_` | Refresh Token | Long-lived OAuth 2.0 refresh token |

Implementations MUST accept both `Token <key>` and `Bearer <key>` authorization header formats for backward compatibility with existing karrio deployments.

---

## 7. Error Handling in MCP

MCP tool errors are returned as text content with the `isError` flag set:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"errors\": [{\"code\": \"invalid_address\", \"message\": \"The recipient postal code is not valid.\", \"field\": \"recipient.postal_code\"}]}"
    }
  ],
  "isError": true
}
```

**Error response format**: The `text` field contains a JSON string conforming to the error envelope defined in [OSP-CORE.md Section 8](./OSP-CORE.md#8-error-handling).

**Successful responses**: Returned as formatted JSON text content:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"rates\": [\n    {\n      \"carrier_name\": \"fedex\",\n      ...\n    }\n  ]\n}"
    }
  ]
}
```

---

## 8. Relationship to karrio MCP Server

The existing `@karrio/mcp` package is the reference implementation of the OSP MCP binding. The following table maps karrio's current MCP tools to the OSP-standardized names:

| karrio MCP Tool | OSP MCP Tool | Notes |
|----------------|--------------|-------|
| `get_shipping_rates` | `osp/get_rates` | Namespaced, simplified name |
| `create_shipment` | `osp/create_shipment` | Namespaced |
| `get_shipment` | `osp/get_shipment` | Namespaced |
| `list_shipments` | *(no OSP equivalent)* | karrio-specific list operation |
| `cancel_shipment` | `osp/cancel_shipment` | Namespaced |
| `track_package` | `osp/track_shipment` | Renamed for consistency |
| `list_carriers` | `osp/list_carriers` | Resource fallback tool |
| `schedule_pickup` | `osp/schedule_pickup` | Namespaced |
| `create_manifest` | `osp/create_manifest` | Namespaced |

| karrio MCP Resource | OSP MCP Resource | Notes |
|---------------------|------------------|-------|
| `karrio://carriers` | `osp://carriers` | OSP namespace |
| `karrio://carriers/{id}` | `osp://carriers/{carrier_name}` | Keyed by carrier_name |

### Migration Path

Implementations transitioning from karrio MCP tools to OSP-compliant tools SHOULD:

1. Support both namespaced (`osp/get_rates`) and legacy (`get_shipping_rates`) tool names during a transition period
2. Emit deprecation notices in responses when legacy tool names are used
3. Remove legacy tool names in the next major version

### Extensions Beyond Core OSP

karrio's MCP server includes tools beyond the 8 core OSP operations (e.g., `list_shipments`). These are valid as extensions and SHOULD use the `karrio/` namespace prefix:

```
karrio/list_shipments    → karrio-specific extension
karrio/list_orders       → karrio-specific extension
osp/get_rates            → OSP standard tool
```
