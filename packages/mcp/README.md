# @karrio/mcp

Karrio MCP Server -- Multi-carrier shipping intelligence for AI agents.

Connect any AI agent (Claude, ChatGPT, Cursor, VS Code Copilot) to 50+ shipping carriers through the [Model Context Protocol](https://modelcontextprotocol.io).

## Features

- **10 shipping tools** -- rates, labels, tracking, pickups, manifests, orders, and more
- **MCP Resources** for a live carrier capability catalog -- no other shipping MCP does this
- **stdio + Streamable HTTP** transport (remote-ready)
- **Works with any Karrio instance** -- cloud or self-hosted

## Quick Start

### Prerequisites

- A Karrio instance ([cloud](https://karrio.io) or [self-hosted](https://docs.karrio.io)) with an API key
- Node.js 18+

### npx (zero install)

```bash
KARRIO_API_URL=https://your-karrio-instance.com \
KARRIO_API_KEY=your_key \
npx -y @karrio/mcp
```

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "karrio": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://your-karrio-instance.com",
        "KARRIO_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add karrio -- npx -y @karrio/mcp --api-url https://your-karrio-instance.com --api-key YOUR_KEY
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "karrio": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://your-karrio-instance.com",
        "KARRIO_API_KEY": "your_api_key"
      }
    }
  }
}
```

### VS Code / Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "karrio": {
      "command": "npx",
      "args": ["-y", "@karrio/mcp"],
      "env": {
        "KARRIO_API_URL": "https://your-karrio-instance.com",
        "KARRIO_API_KEY": "your_api_key"
      }
    }
  }
}
```

### HTTP Transport (Remote)

Start the server with Streamable HTTP transport for remote or multi-session use:

```bash
karrio-mcp --api-key YOUR_KEY --http --port 3100
```

The server exposes:

- `POST /mcp` -- MCP message endpoint (auto-creates sessions)
- `GET /mcp` -- SSE streaming for active sessions
- `DELETE /mcp` -- Session teardown
- `GET /.well-known/mcp` -- Server discovery metadata

## Tools

| Tool | Description | Mutating |
|------|-------------|----------|
| `get_shipping_rates` | Get rate quotes from multiple carriers, sorted by price or delivery time | No |
| `create_shipment` | Create a shipment and purchase a shipping label | Yes |
| `get_shipment` | Get shipment details by ID | No |
| `list_shipments` | List shipments with status, carrier, and date filters | No |
| `cancel_shipment` | Cancel a shipment and void its label | Yes |
| `track_package` | Track a package by tracking number with full event history | No |
| `list_carriers` | List connected carriers and their capabilities | No |
| `schedule_pickup` | Schedule a carrier pickup for one or more shipments | Yes |
| `create_manifest` | Create an end-of-day manifest (SCAN form) | Yes |
| `list_orders` | List orders and fulfillment status, or fetch a single order by ID | No |

### Tool Details

**`get_shipping_rates`** -- Compare shipping options across carriers. Accepts origin/destination addresses, parcel dimensions and weight, optional carrier filter, and sort order (`price` or `delivery_time`). Returns ranked rates with carrier name, service, total charge, and estimated delivery.

**`create_shipment`** -- Purchase a shipping label. Requires full shipper and recipient addresses, parcel details, carrier name, and service code. Supports PDF, ZPL, and PNG label formats. This tool is marked as destructive because it incurs a charge.

**`track_package`** -- Real-time package tracking. Provide a tracking number and optionally a carrier name (auto-detection is supported). Returns status, estimated delivery, and a chronological event history with locations.

**`list_carriers`** -- Discover which carriers are connected to your Karrio instance and what capabilities each supports (tracking, rating, shipping, pickup).

**`schedule_pickup`** -- Book a carrier pickup at a specified address with date, ready time, and closing time windows. Optionally include specific shipment IDs.

**`create_manifest`** -- Generate an end-of-day manifest that consolidates shipments into a single carrier document. Optionally scope to specific shipment IDs.

**`list_orders`** -- Query orders by status (`unfulfilled`, `fulfilled`, `cancelled`, `partial`) or retrieve a specific order by ID with full line items and shipment details.

## Resources

MCP Resources give AI agents direct access to structured reference data without requiring a tool call.

| URI | Description |
|-----|-------------|
| `karrio://carriers` | Complete multi-carrier capability catalog (all connected carriers) |
| `karrio://carriers/{carrier_id}` | Detailed info for a specific carrier connection |

Resources are supported by Claude Desktop, Claude Code, VS Code Copilot, and Continue. For clients that do not support Resources (such as Cursor or ChatGPT), use the `list_carriers` tool instead.

## Configuration

| Environment Variable | CLI Flag | Description | Default |
|---------------------|----------|-------------|---------|
| `KARRIO_API_URL` | `--api-url` | Karrio API base URL | `http://localhost:5002` |
| `KARRIO_API_KEY` | `--api-key` | Karrio API key (**required**) | -- |
| `PORT` | `--port` | HTTP transport port | `3100` |
| -- | `--http` | Enable Streamable HTTP transport (instead of stdio) | `false` |

CLI flags take precedence over environment variables.

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Run in development (watch mode)
npm run dev

# Run tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests only
npm run test:integration

# Lint
npm run lint
```

## Architecture

```
src/
  index.ts              CLI entry point (stdio or HTTP transport)
  server.ts             McpServer setup and tool/resource registration
  client.ts             Karrio REST API client
  auth.ts               API key validation utilities
  tools/
    rates.ts            get_shipping_rates
    shipments.ts        create_shipment, get_shipment, list_shipments, cancel_shipment
    tracking.ts         track_package
    carriers.ts         list_carriers, list_carrier_connections
    pickups.ts          schedule_pickup
    manifests.ts        create_manifest
    orders.ts           list_orders
  resources/
    carriers.ts         karrio://carriers, karrio://carriers/{carrier_id}
  transports/
    http.ts             Streamable HTTP transport with session management
```

## License

Apache-2.0
