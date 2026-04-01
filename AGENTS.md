# Repository Guidelines

> **For AI Agents**: This is the single source of truth for coding preferences and project context.
> Agent-specific files (CLAUDE.md, GEMINI.md, CODEX.md) reference this document.

---

## Context Priority

1. **Read this file first** for repository conventions
2. For carrier integrations, consult `CARRIER_INTEGRATION_GUIDE.md`
3. Check PRDs in `PRDs/` folder for feature architecture decisions
4. Review existing code patterns before implementing new features
5. **Search for existing utilities before writing new code**

---

## PRD Guidelines

When creating PRDs, use the template at [`PRDs/TEMPLATE.md`](./PRDs/TEMPLATE.md):

1. **Study existing code first** - search for similar patterns, utilities, and implementations to reuse
2. **Always start from the template** - maintains consistency across PRDs
3. **Include architecture diagrams** - use ASCII art for overview, sequence, and dataflow diagrams
4. **Use tables over prose** - easier to scan and maintain
5. **Show Before/After code** - makes changes concrete in Problem Statement
6. **Follow AGENTS.md exactly** - code examples must match original author style and test patterns

### PRD Types and Focus Areas

| Type | Focus | Key Sections |
|------|-------|--------------|
| Integration | API mapping, field translation, carrier quirks | Technical Design, Field Reference, Testing |
| Refactoring | Architecture changes, migration strategy | Alternatives Considered, Migration & Rollback |
| Enhancement | Additive features, enum extensions | Goals, Edge Cases, Backward Compatibility |
| Architecture | System design, cross-cutting concerns | All sections, Security Considerations |

### Required Sections (All PRDs)

- Metadata block (table format)
- Executive Summary with Key Architecture Decisions
- Problem Statement with Current/Desired State code
- Goals & Success Criteria (tables)
- Alternatives Considered (decision table)
- Technical Design with diagrams
- Edge Cases & Failure Modes
- Implementation Plan (phased tables)
- Testing Strategy with code examples
- Risk Assessment (table)
- Migration & Rollback plan

### Writing Style

- Technical but accessible
- Heavy use of tables over prose
- Before/After code comparisons
- No user stories - use technical specs with acceptance criteria
- Bold for emphasis, inline code for technical terms
- ASCII diagrams required: architecture overview, sequence diagrams, dataflow diagrams

### Before Writing a PRD

1. **Search the codebase** for similar implementations and patterns
2. **Identify reusable utilities** in `karrio.lib`, `@karrio/hooks`, `@karrio/ui`
3. **Study existing test files** in related modules for testing patterns
4. **Document findings** in the "Existing Code Analysis" section

### Interactive PRD Creation

PRDs should be created iteratively with user input:

1. **Draft** - Create initial structure with known information
2. **Identify gaps** - Flag edge cases, ambiguities, and decision points
3. **Ask questions** - Prompt user for clarification before finalizing architecture
4. **Document decisions** - Record answers in "Open Questions & Decisions" section
5. **Iterate** - Repeat until all decisions are resolved

**When to ask clarifying questions:**
- Multiple valid architectural approaches exist
- Edge cases have no clear handling strategy
- Trade-offs require business/product input
- Scope boundaries are unclear
- Backward compatibility decisions needed

---

## Domain Context: Shipping & Logistics

Karrio is a **universal shipping API** that abstracts carrier integrations. Key domain concepts:

- **Shipments**: Packages sent from shipper to recipient
- **Rates**: Pricing quotes from carriers for a shipment
- **Tracking**: Real-time package location and status updates
- **Labels**: Shipping documents generated after booking
- **Customs**: International shipping documentation
- **Manifests**: Carrier pickup summaries
- **Carriers/Connectors**: Integrations with shipping providers (UPS, FedEx, DHL, etc.)

---

## Project Structure & Module Organization

### Backend (Django)
- **API Service**: `apps/api/karrio/server/`
- **Settings**: `apps/api/karrio/server/settings/`
- **Core modules**: `modules/` (SDK, connectors, pricing)
- **Carrier connectors**: `modules/connectors/<carrier>/`
- **Community extensions**: `community/`
- **Plugins**: `plugins/` (addresscomplete, googlegeocoding)

### Frontend (Next.js + React)
- **Dashboard**: `apps/dashboard/` (main shipping UI)
- **Web**: `apps/web/` (app interface)
- **Marketing**: `apps/www/` (public site)
- **Shared packages**: `packages/` (hooks, ui, types, lib)

### Other Key Directories
- **Automation scripts**: `bin/`
- **Container workflows**: `docker/` with `docker-compose.yml`

---

## ⚠️ CRITICAL: Reuse Existing Code (DRY)

**NEVER reinvent the wheel. ALWAYS search for existing utilities first.**

### Python Library (`karrio.lib`) — PREFERRED

**Always use `import karrio.lib as lib`** — it provides the cleanest, most readable API.

```python
import karrio.lib as lib

# --- Data Parsing ---
lib.to_dict(response)              # Parse JSON/XML to dict
lib.to_dict_safe(response)         # Safe parse (returns {} on error)
lib.to_json(data)                  # Serialize to JSON string
lib.to_object(MyClass, data)       # Instantiate class from dict/XML

# --- String Manipulation ---
lib.text("value1", "value2")       # Join strings safely (ignores None)
lib.text("long text", max=20)      # Truncate to max length
lib.join("a", "b", separator=", ") # Join with custom separator
lib.to_slug("MyService")           # Convert to snake_case slug
lib.to_snake_case("CamelCase")     # Convert camelCase → snake_case

# --- Number Formatting ---
lib.to_int("15.5")                 # Parse to integer: 15
lib.to_decimal(14.899)             # Parse to 2 decimal places: 14.90
lib.to_money(25.999)               # Format as currency: 26.00
lib.format_decimal(14.899, 1)      # Custom decimal places: 14.9
lib.to_list(value)                 # Ensure value is a list: [] if None

# --- Date/Time Parsing ---
lib.fdate("2024-01-15")            # Format date string
lib.ftime("14:30:00")              # Format time string
lib.fdatetime("2024-01-15 14:30")  # Format datetime string
lib.ftimestamp("1705334400")       # Parse Unix timestamp
lib.to_date("2024-01-15")          # Parse to datetime object

# --- XML Handling ---
lib.to_xml(typed_object)           # Serialize XML object to string
lib.to_element("<xml>...</xml>")   # Parse XML string to Element
lib.find_element("tag", element)   # Find XML element by tag
lib.create_envelope(body, header)  # Create SOAP envelope

# --- Address Utilities ---
lib.to_address(address_model)      # Wrap address with computed fields
lib.to_zip5("12345-6789")          # Extract 5-digit zip: "12345"
lib.to_country_name("US")          # Get full country name
lib.to_state_name("CA", "US")      # Get full state name

# --- Shipping Helpers ---
lib.to_packages(parcels)           # Process parcel list with presets
lib.to_shipping_options(options)   # Parse shipping options
lib.to_services(["express"])       # Parse service list
lib.to_customs_info(customs)       # Process customs with defaults
lib.to_commodities(commodities)    # Process commodity list
lib.to_multi_piece_rates(rates)    # Combine multi-piece rates
lib.to_multi_piece_shipment(ships) # Combine multi-piece shipments

# --- HTTP & Async ---
lib.request(url=url, data=data)    # Make HTTP request
lib.run_concurently(fn, items)     # Parallel execution
lib.run_asynchronously(fn, items)  # Async execution
lib.failsafe(lambda: risky())      # Safe execution (returns None on error)

# --- Document Processing ---
lib.bundle_pdfs(base64_list)       # Merge multiple PDFs
lib.bundle_base64(docs, "PDF")     # Bundle documents by format
lib.image_to_pdf(image_base64)     # Convert image to PDF
lib.zpl_to_pdf(zpl_str, w, h)      # Convert ZPL to PDF
lib.to_buffer(base64_str)          # Decode base64 to buffer
lib.encode_base64(bytes)           # Encode bytes to base64
lib.decode(bytes)                  # Decode bytes with fallback encodings

# --- File Loading ---
lib.load_json(path)                # Load and parse JSON file
lib.load_file_content(path)        # Load file as string
```

### Core Classes (from `karrio.lib`)

```python
import karrio.lib as lib

# Request/Response lifecycle
lib.Serializable(request)          # Wrap request for pipeline
lib.Deserializable(response)       # Wrap response for parsing
lib.Pipeline(job1, job2)           # Chain multiple operations
lib.Job(fn, fallback=None)         # Single pipeline step

# Enums for carrier services/options
lib.Enum                           # Base enum class
lib.StrEnum                        # String-based enum
lib.Flag                           # Flag-based enum
lib.OptionEnum("CODE", type)       # Shipping option enum

# Other utilities
lib.Cache                          # Caching helper
lib.Element                        # XML Element type
lib.Envelope, lib.Header, lib.Body # SOAP envelope components
```

### Legacy Utilities (avoid if possible)

The older utilities still exist but prefer `lib.*` equivalents:

```python
# OLD (avoid)                      # NEW (preferred)
from karrio.core.utils import DP   # → lib.to_dict(), lib.to_object()
from karrio.core.utils import SF   # → lib.text(), lib.join()
from karrio.core.utils import NF   # → lib.to_int(), lib.to_decimal()
from karrio.core.utils import DF   # → lib.fdate(), lib.ftime()
from karrio.core.utils import XP   # → lib.to_xml(), lib.find_element()
```

### TypeScript/React Utilities (`packages/lib/`)

```typescript
import {
  // Null checks
  isNone, isNoneOrEmpty, deepEqual,
  
  // Formatting
  formatDate, formatDateTime, formatAddress, formatWeight,
  formatDimension, formatRef, formatCarrierSlug,
  
  // Data manipulation
  cleanDict, jsonify, getInitials,
  groupBy, snakeCase, toNumber, isEqual,
  
  // URL/routing
  p, url$, getURLSearchParams, insertUrlParam,
  
  // Error handling
  handleFailure, errorToMessages, onError,
  
  // Utilities
  failsafe, debounce, getCookie, setCookie, parseJwt,
  
  // Shipping-specific
  findPreset, getShipmentCommodities, createShipmentFromOrders,
} from "@karrio/lib";
```

### React Hooks (`packages/hooks/`)

```typescript
// Data fetching hooks - USE THESE instead of raw fetch/axios
import { useShipment, useShipments } from "@karrio/hooks/shipment";
import { useTracker, useTrackers } from "@karrio/hooks/tracker";
import { useOrders, useOrder } from "@karrio/hooks/order";
import { useCarrierConnections } from "@karrio/hooks/carrier-connections";
import { useAddresses } from "@karrio/hooks/address";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useAppMode } from "@karrio/hooks/app-mode";
import { useLocation } from "@karrio/hooks/location";
import { useSession } from "@karrio/hooks/session";
import { useUser } from "@karrio/hooks/user";
// ... see packages/hooks/ for full list
```

### UI Components (`packages/ui/`)

```typescript
// ALWAYS use existing components - check packages/ui/core/components/
import {
  InputField, SelectField, TextareaField, CheckboxField,
  Dropdown, DropdownInput,
  Spinner, Loader,
  StatusBadge, CarrierBadge, CarrierImage,
  AddressDescription, ParcelDescription, RateDescription,
  Tabs, Expandable, Modal,
  // ... see packages/ui/core/components/index.tsx
} from "@karrio/ui";
```

### Types (`packages/types/`)

```typescript
// ALWAYS import types from @karrio/types - NEVER define inline
import type {
  ShipmentType, TrackerType, OrderType,
  AddressType, ParcelType, CommodityType, CustomsType,
  RateType, ChargeType, MessageType,
  // ... see packages/types/base.ts
} from "@karrio/types";

// Constants are also available
import {
  COUNTRY_OPTIONS, CURRENCY_OPTIONS, CARRIER_NAMES,
  SHIPMENT_STATUSES, TRACKER_STATUSES, ORDER_STATUSES,
  DEFAULT_PARCEL_CONTENT, DEFAULT_CUSTOMS_CONTENT,
} from "@karrio/types";
```

---

## 🚫 DO NOT (Anti-patterns)

### General
- ❌ **DO NOT** create new utility functions if one exists
- ❌ **DO NOT** define types inline—import from `@karrio/types`
- ❌ **DO NOT** use raw `fetch`/`axios`—use existing hooks
- ❌ **DO NOT** add new dependencies without checking existing ones
- ❌ **DO NOT** copy-paste code—extract to shared utilities
- ❌ **DO NOT** use `any` type—find or create proper types
- ❌ **DO NOT** write overly clever/cryptic code
- ❌ **DO NOT** add features not explicitly requested

### Python
- ❌ **DO NOT** use `pytest`—we use `unittest` and Django tests
- ❌ **DO NOT** use nested loops when `map`/`filter`/comprehensions work
- ❌ **DO NOT** catch bare `Exception`—be specific
- ❌ **DO NOT** use mutable default arguments
- ❌ **DO NOT** import `*` except from designated re-export modules
- ❌ **DO NOT** use raw SQL (`RunSQL`) in Django migrations—use only Django migration operations (`AddField`, `RemoveField`, `RenameField`, `AlterField`, `RunPython`, etc.) to ensure compatibility across SQLite, PostgreSQL, and MySQL

### TypeScript/React
- ❌ **DO NOT** use `class` components—use functional components
- ❌ **DO NOT** define state management outside existing patterns
- ❌ **DO NOT** create new CSS files—use existing Tailwind/SCSS
- ❌ **DO NOT** use inline styles except for dynamic values
- ❌ **DO NOT** create duplicate modal/form patterns

### Testing
- ❌ **DO NOT** test implementation details—test behavior
- ❌ **DO NOT** use `pytest`—we use native `unittest` and Django tests
- ❌ **DO NOT** mock what you don't own
- ❌ **DO NOT** write tests that depend on external services

---

## Build, Test, and Development Commands

### Initial Setup
```bash
./bin/setup-dev-env  # Create Python virtualenv and install tooling
```

### Development Servers
```bash
./bin/start-dev                    # API (5002) + Dashboard (3002)
npm run dev -w @karrio/dashboard   # Dashboard only
cd docker && docker compose up     # Full stack with Docker
```

### Build & Lint
```bash
npm run build   # Turbo: turbo run build
npm run lint    # ESLint across all workspaces
npm run format  # Prettier formatting
```

---

## Coding Style & Naming Conventions

- **Write code as if the same person authored the entire codebase**—consistency is paramount.
- **Favor functional, declarative style**: use `map`, `reduce`, `filter`, and list comprehensions in Python; avoid nested `if` statements and `for` loops when a functional alternative is cleaner.
- **Concise but readable**: code should be terse yet easily maintainable by a human developer—no unnecessary verbosity, but no cryptic one-liners either.

### Python

**Style:**
- PEP 8 with 4-space indentation
- Format via `black`, type check with `mypy`
- Use snake_case for modules/functions, PascalCase for classes

**Import Order:**
```python
# 1. Standard library
import json
import typing
from datetime import datetime

# 2. Third-party
import requests
from django.db import models

# 3. Karrio core
import karrio.lib as lib
from karrio.core.models import Message, TrackingDetails

# 4. Local/relative
from .mapper import Mapper
from .types import ShippingRequest
```

**Good Pattern:**
```python
# Functional style with karrio.lib
import karrio.lib as lib
from karrio.core.models import TrackingDetails, TrackingEvent

def parse_tracking_response(response: dict) -> list:
    data = lib.to_dict(response)
    return [
        TrackingDetails(
            carrier_name="carrier",
            tracking_number=event.get("trackingNumber"),
            events=[
                TrackingEvent(
                    date=lib.fdate(e.get("date")),
                    description=lib.text(e.get("status"), e.get("location")),
                )
                for e in lib.to_list(event.get("events"))
            ],
        )
        for event in lib.to_list(data.get("tracking"))
    ]
```

### TypeScript / React

**Style:**
- 2-space indentation, format with Prettier
- Lint through `packages/eslint-config-custom`
- PascalCase for components, camelCase for functions/variables

**Import Order:**
```typescript
// 1. React/Next
import React from "react";
import { useRouter } from "next/navigation";

// 2. Third-party
import { useQuery } from "@tanstack/react-query";

// 3. Karrio packages
import { useShipment } from "@karrio/hooks/shipment";
import { formatAddress, isNone } from "@karrio/lib";
import type { ShipmentType } from "@karrio/types";

// 4. Local components/utils
import { ShipmentCard } from "./shipment-card";
```

**Good Pattern:**
```typescript
// Use existing hooks and utilities
import { useShipments } from "@karrio/hooks/shipment";
import { formatDate, isNoneOrEmpty } from "@karrio/lib";
import { StatusBadge, Spinner } from "@karrio/ui";

export function ShipmentList() {
  const { query: { data, isLoading } } = useShipments();
  
  if (isLoading) return <Spinner />;
  if (isNoneOrEmpty(data?.shipments)) return <p>No shipments</p>;
  
  return (
    <ul>
      {data.shipments.map((shipment) => (
        <li key={shipment.id}>
          <StatusBadge status={shipment.status} />
          <span>{formatDate(shipment.created_at)}</span>
        </li>
      ))}
    </ul>
  );
}
```

---

## Testing Guidelines

### Quick Reference Commands
```bash
# Activate environment first
source bin/activate-env

# SDK and carrier connector tests
./bin/run-sdk-tests  # all SDK tests
python -m unittest discover -v -f modules/connectors/<carrier>/tests  # single carrier

# Server/Django tests
./bin/run-server-tests  # all server tests
karrio test --failfast karrio.server.<module>.tests  # single module
```

### Key Rules
- **Always run tests from the repository root**
- **Always take inspiration from existing tests**—match the coding style of the project
- **We do NOT use pytest anywhere in the stack**:
  - Carrier integrations: native Python `unittest`
  - Server/Django: Django tests via `karrio` (manage.py wrapper)
- **Test files**: `test_<feature>.py` with classes `Test<Module><Feature>`

### Carrier Integration Tests
- Follow templates in `CARRIER_INTEGRATION_GUIDE.md`
- Canonical files: `test_rate.py`, `test_tracking.py`, `test_shipment.py`
- Classes shaped as `Test<Carrier><Feature>`

### Django Test Writing Style (Important!)

- **When debugging failing tests**, add `print(response)` before assertions to see the actual response
- **Remove print statements once tests pass**—keep test output clean
- **Create objects via API requests**, not direct model manipulation
- **Use `self.assertResponseNoErrors(response)` first**, then:
- **Single comprehensive assertion**: `self.assertDictEqual` or `self.assertListEqual` with full response data
- **Use `mock.ANY`** for dynamic fields like `id`, `created_at`, `updated_at`
- **Avoid multiple single-field assertions**—prefer complete dict/list comparisons

**Example:**
```python
from unittest import mock

def test_create_shipment(self):
    response = self.client.post('/api/shipments', data={...})
    # print(response)  # Uncomment for debugging, remove when tests pass
    self.assertResponseNoErrors(response)
    self.assertDictEqual(
        response.data,
        {
            "id": mock.ANY,
            "status": "draft",
            "shipper": {...},
            "recipient": {...},
            "created_at": mock.ANY,
            "updated_at": mock.ANY,
        }
    )
```

---

## Carrier Integration Patterns

When working with carrier integrations:

1. **Always consult `CARRIER_INTEGRATION_GUIDE.md`**
2. Study existing implementations in `modules/connectors/`
3. Follow the mapper pattern consistently:
   - `karrio/mappers/<carrier>/mapper.py` - Main mapper class
   - `karrio/mappers/<carrier>/proxy.py` - HTTP client
   - `karrio/providers/<carrier>/` - Request/response parsing
4. Test files: `test_rate.py`, `test_tracking.py`, `test_shipment.py`
5. Reuse `karrio.core.utils` extensively

**Mapper Structure:**
```python
# Always inherit from existing base classes
import karrio.lib as lib
from karrio.api.mapper import Mapper as BaseMapper

class Mapper(BaseMapper):
    def create_tracking_request(self, payload):
        # Use lib.Serializable for requests
        return lib.Serializable(
            TrackingRequest(
                tracking_number=payload.tracking_number,
                # ...
            )
        )
```

---

## Error Handling

### Python
```python
# Use specific exceptions
from karrio.core.errors import ShippingSDKError, ProviderError

# Use failsafe for optional operations
from karrio.core.utils import failsafe

result = failsafe(lambda: risky_operation())  # Returns None on failure
```

### TypeScript
```typescript
// Use existing error handling utilities
import { handleFailure, errorToMessages } from "@karrio/lib";

try {
  const result = await handleFailure(apiCall());
} catch (error) {
  const messages = errorToMessages(error);
  // Handle messages...
}
```

---

## Commit & Pull Request Guidelines

- **Never commit without explicit user permission** — always ask before creating a commit
- **Never add AI co-author lines** (e.g., `Co-Authored-By: Claude ...`) to commit messages
- Format: `type: summary` (e.g., `fix:`, `feat:`, `chore:`)
- Reference issues: `refs #123` or `fixes #123`
- Keep commits focused and atomic
- Rebase on `main` before PR
- Run lint/test before pushing
- Fill out PR template, link discussions, enable "Allow edits from maintainers"

---

## Configuration Files

- `.env.sample` - Environment template (never commit secrets!)
- `./bin/create-new-env` - Generate fresh config
- `docker-compose.yml` - Container orchestration
- `turbo.json` - Monorepo build configuration

---

## Before Making Changes

1. **Search for existing code** that does what you need
2. **Read the files mentioned first**
3. **Create a plan** before implementing
4. **Locate specific code sections** to modify (don't read entire large files)
5. **Implement step by step** according to your plan
6. **Stay calm and methodical**—break down overwhelming changes
7. **Don't modify unrelated code**
8. **Test your changes** before committing

---

## Quick Reference: Where to Find Things

| Need | Location |
|------|----------|
| Python utilities | `modules/sdk/karrio/core/utils/` |
| TypeScript utilities | `packages/lib/` |
| React hooks | `packages/hooks/` |
| UI components | `packages/ui/core/components/` |
| Types | `packages/types/` |
| Carrier implementations | `modules/connectors/<carrier>/` |
| API endpoints | `apps/api/karrio/server/` |
| Dashboard pages | `apps/dashboard/src/app/` |

---

## Request Lifecycle & Debugging

Understanding the flow helps you debug faster and know where to add code:

```
1. API Layer (apps/api/karrio/server/)
   └── Receives HTTP request, validates serializer
   
2. Gateway (karrio.server.core.gateway)
   └── Dispatches to correct Carrier Module
   
3. Mapper (modules/connectors/<carrier>/karrio/mappers/<carrier>/mapper.py)
   └── create_..._request: Converts Unified Model → Carrier Payload (XML/JSON)
   
4. Proxy (modules/connectors/<carrier>/karrio/mappers/<carrier>/proxy.py)
   └── Sends HTTP request to Carrier API
   
5. Provider (modules/connectors/<carrier>/karrio/providers/<carrier>/)
   └── parse_..._response: Converts Carrier Response → Unified Model
```

**Debugging Tips:**
- Print the return value of `Mapper.create_..._request` to inspect raw carrier payload
- Check `karrio.server.core.gateway` for request routing logic
- Use `lib.to_json()` to pretty-print complex objects
- Check Django logs at DEBUG level for SQL query analysis

---

## Core Response Models Reference

When writing carrier mappers, you return these objects from `karrio.core.models`:

```python
# Rate Response
RateDetails(
    carrier_name="carrier",
    carrier_id="carrier-account-id",
    service="express",              # Service code
    total_charge=Decimal("25.99"),
    currency="USD",
    transit_days=2,                 # Optional
)

# Tracking Response
TrackingDetails(
    carrier_name="carrier",
    carrier_id="carrier-account-id", 
    tracking_number="1Z999AA...",
    status=TrackingStatus.in_transit,  # Use enum!
    events=[
        TrackingEvent(
            date="2024-01-15",
            description="Package arrived at facility",
            location="New York, NY",
            code="AR",              # Carrier-specific code
            time="14:30",
        )
    ],
    delivered=False,
)

# Shipment Response
ShipmentDetails(
    carrier_name="carrier",
    carrier_id="carrier-account-id",
    tracking_number="1Z999AA...",
    shipment_identifier="SHIP123",  # Carrier's internal ID
    label_type="PDF",
    docs=Documents(label="base64..."),  # Label document
)
```

---

## Django API Patterns

### URL Structure
```
/api/v1/<resource>/           → List/Create
/api/v1/<resource>/{id}/      → Retrieve/Update/Delete  
/api/v1/<resource>/{id}/<action>/  → Custom actions
```

### ViewSet Conventions
```python
from karrio.server.core.views.api import GenericAPIView, APIView

class ShipmentViewSet(GenericAPIView):
    # Use GenericAPIView for authenticated endpoints
    # Use APIView for public endpoints
    # Pagination: self.paginate_queryset()
    # Filtering: use karrio.server.core.filters
    pass

# Serializer rules:
# - Use ModelSerializer for DB models
# - Always define Meta.fields explicitly (never '__all__')
```

### Multi-Tenancy (Critical!)
```python
# All tenant-scoped models inherit from OwnedEntity
# ALWAYS filter by org context to prevent data leakage

# ❌ BAD - Leaks data across tenants!
Shipment.objects.all()

# ✅ GOOD - Properly scoped
Shipment.objects.filter(org=request.user.org)

# Query optimization - avoid N+1
Shipment.objects.select_related('shipper', 'recipient', 'carrier_connection')
Shipment.objects.prefetch_related('parcels', 'customs', 'rates')
```

### ⚠️ N+1 Query Prevention (Critical!)

N+1 queries are a common Django ORM pitfall that can severely degrade performance,
especially on serverless databases (Aurora Serverless) where each query incurs connection overhead.

**Always review loops that touch the database:**

```python
# ❌ BAD - N+1: one UPDATE per tracker in a loop
for tracker in trackers:
    tracker.status = compute_status(tracker)
    tracker.save()  # N individual UPDATE queries

# ❌ BAD - N+1: one SELECT per related object in a loop
for shipment in shipments:
    print(shipment.carrier.name)  # N individual SELECT queries (lazy loading)

# ✅ GOOD - Bulk update: single UPDATE for all trackers
for tracker in trackers:
    tracker.status = compute_status(tracker)
Tracking.objects.bulk_update(trackers, ["status", "updated_at"])

# ✅ GOOD - Prefetch/select related: single JOIN query
shipments = Shipment.objects.select_related("carrier").filter(...)
for shipment in shipments:
    print(shipment.carrier.name)  # No extra queries
```

**Key patterns to watch for:**
- `model.save()` inside a loop → use `bulk_update()` or `bulk_create()`
- `model.related_field.attribute` without `select_related` → add `select_related()`
- `model.related_set.all()` without `prefetch_related` → add `prefetch_related()`
- `update_or_create()` in high-concurrency paths → use split `create()`/`filter().update()` to avoid `SELECT FOR UPDATE` lock contention
- Individual `filter().update()` calls in a loop → collect changes and use `bulk_update()`

---

## Background Jobs (Huey)

### When to Use Background Jobs
- ✅ Carrier tracking updates (polling external APIs)
- ✅ Batch rate shopping (multiple carriers)
- ✅ Document generation (labels, invoices, manifests)
- ✅ Webhook delivery retries
- ✅ Data exports (CSV, PDF reports)
- ❌ Real-time user-facing operations (rate quotes shown in UI)

### Task Pattern
```python
# Task helpers: karrio.server.core.tasks (main) + apps/api/karrio/server/lib/otel_huey.py (instrumentation)
from karrio.server.core.tasks import huey

@huey.task()
def update_tracking(tracking_id: str):
    """Background task pattern."""
    tracking = Tracking.objects.select_related('carrier').get(id=tracking_id)
    # ... update logic
    tracking.save()

# Jobs run synchronously in tests (immediate mode via HUEY['immediate'] = True)
# See apps/api/karrio/server/lib/otel_huey.py for OpenTelemetry instrumentation
```

---

## Carrier Integration Checklist

### Required Files
```
modules/connectors/<carrier>/
├── karrio/
│   ├── mappers/<carrier>/
│   │   ├── __init__.py
│   │   ├── mapper.py      # Main mapper class
│   │   ├── proxy.py       # HTTP client
│   │   └── settings.py    # Carrier credentials
│   └── providers/<carrier>/
│       ├── __init__.py
│       ├── rate.py        # Rate request/response
│       ├── shipment.py    # Shipment request/response
│       ├── tracking.py    # Tracking request/response
│       └── error.py       # Error parsing
└── tests/
    ├── __init__.py
    ├── fixture.py         # Test credentials & mock data
    ├── test_rate.py
    ├── test_shipment.py
    └── test_tracking.py
```

### Definition of Done
- [ ] `test_rate.py`: Single item rate + invalid address error handling
- [ ] `test_shipment.py`: Label generation + void/cancel shipment
- [ ] `test_tracking.py`: Delivered status + in-transit with events
- [ ] All tests pass: `python -m unittest discover -v -f modules/connectors/<carrier>/tests`
- [ ] Service/Option enums defined (never hardcode strings)
- [ ] Uses `karrio.lib` extensively (lib.to_dict, lib.text, lib.fdate, lib.to_xml, etc.)

### Service & Option Enum Pattern
```python
import karrio.lib as lib

# In units.py - NEVER use raw strings for service codes
class ShippingService(lib.StrEnum):
    carrier_express = "EXPRESS_123"
    carrier_ground = "GROUND_456"

class ShippingOption(lib.Enum):
    signature_required = lib.OptionEnum("SIG_REQ", bool)
    insurance = lib.OptionEnum("INS", float)
```

---

## Common Carrier Quirks

### Weight/Dimension Units
| Carrier | Default Units | Notes |
|---------|--------------|-------|
| UPS | LBS/IN (US), KG/CM (intl) | Use `unit_system` parameter |
| FedEx | LBS/IN | Use `unit_system="metric"` for KG/CM |
| DHL Express | KG/CM | Always metric |
| Canada Post | KG/CM | Always metric |
| USPS | LBS/IN or OZ/IN | OZ for small packages |

### Known Issues
- **UPS**: Requires shipper account number in credentials
- **FedEx**: Rate quotes expire after ~10 seconds (must re-rate before ship)
- **DHL**: Requires separate product code for paperless invoices
- **Purolator**: Billing account must match shipper postal code prefix
- **Canada Post**: Contract ID must be numeric, customer number is alpha

### Address Validation
```python
carriers_requiring_validation = ["ups", "fedex", "dhl_express"]
carriers_with_residential_surcharge = ["ups", "fedex", "purolator"]
```

---

## Environment Variables

### Critical Variables
```bash
# API Configuration
KARRIO_API_URL=http://localhost:5002
DJANGO_SETTINGS_MODULE=karrio.server.settings

# Database
DATABASE_URL=postgres://user:pass@localhost:5432/karrio

# Redis (caching & task queue)
REDIS_URL=redis://localhost:6379/0

# Authentication
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### Carrier Credentials Pattern
```bash
# Format: <CARRIER>_<FIELD>
UPS_CLIENT_ID=xxx
UPS_CLIENT_SECRET=xxx
FEDEX_API_KEY=xxx
FEDEX_SECRET_KEY=xxx
```

### Troubleshooting
```bash
# Reset Redis queues
redis-cli FLUSHDB

# Refresh migrations
karrio migrate --run-syncdb

# Check worker status
karrio run_huey --workers 1
```

---

**Remember**: Consistency is paramount. Study existing patterns, match the project's style, reuse existing code, and write code as if you're the original author maintaining coherence across the entire codebase.
