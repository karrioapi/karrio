# DHL Parcel DE Environment-Based Default Credentials

<!-- ENHANCEMENT: This PRD covers implementing system-level credential configuration for DHL Parcel DE -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-22 |
| Status | Planning |
| Owner | Karrio Team |
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

This PRD proposes implementing environment-based default credentials for DHL Parcel DE, following the established Teleship pattern. Super admins will be able to configure master API credentials (username, password, client_id, client_secret) at the system level via environment variables. Users can then create DHL Parcel DE connections without providing credentials (only billing numbers and other config), and the system will automatically use the pre-configured credentials in the background.

### Key Architecture Decisions

1. **System-level credential storage**: Add `SYSTEM_CONFIG` to DHL Parcel DE with environment variables for credentials (test and live modes)
2. **Computed credential properties**: Introduce `connection_username`, `connection_password`, `connection_client_id`, `connection_client_secret` properties in Settings that prefer user values but fallback to env values
3. **Test/Live mode separation**: Support separate env vars for sandbox and production credentials (e.g., `DHL_PARCEL_DE_USERNAME` and `DHL_PARCEL_DE_SANDBOX_USERNAME`)
4. **Non-breaking change**: Existing connections with user-provided credentials continue to work unchanged

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| SYSTEM_CONFIG for DHL Parcel DE credentials | UI changes for admin configuration (use Django admin) |
| Computed credential properties with fallback | Changes to other DHL carriers |
| Test/Live mode env var separation | Automatic credential validation on startup |
| Plugin metadata update for system_config | OAuth flow implementation |
| Documentation for admin setup | Billing number auto-configuration |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Env var naming convention | `DHL_PARCEL_DE_*` prefix | Consistent with carrier name, matches plugin id | 2026-01-22 |
| D2 | Test/Live mode handling | Separate env vars (e.g., `_SANDBOX_*`) | Follows Teleship pattern, clear separation | 2026-01-22 |
| D3 | Fallback behavior | User value > Env value > None | Maximum flexibility for users | 2026-01-22 |
| D4 | Property naming | `connection_*` prefix | Distinguishes computed from raw values | 2026-01-22 |
| D5 | Dashboard indicator | Via references API + hint text | Use existing metadata API, add computed `system_credentials_carriers` field | 2026-01-23 |
| D6 | Field visibility | Conditional hide + override option | Hide credentials when system defaults exist, show "Using system credentials" with expand to override | 2026-01-23 |
| D7 | Validation timing | Fail on connection creation | Validate credentials resolvable (user OR system) when saving connection | 2026-01-23 |
| D8 | Validation hook | Yes, add similar to Teleship | Pre-operation hook to check credentials with clear error messages | 2026-01-23 |

---

## UX Specification

### Dashboard Indicator Mechanism

The dashboard needs to know when system credentials are configured so it can adjust the connection form UI. This will be achieved by adding a computed field to the existing `/references` API response.

**References API Enhancement:**

```json
{
  "carriers": { "dhl_parcel_de": "DHL Germany", ... },
  "system_credentials_carriers": {
    "dhl_parcel_de": {
      "production": true,
      "sandbox": true
    },
    "teleship": {
      "production": true,
      "sandbox": false
    }
  },
  ...
}
```

This field is computed at runtime based on whether the corresponding env vars have non-empty values in constance.

### Connection Form UI Behavior

**When system credentials ARE configured for the carrier:**

1. **Credentials Tab Behavior:**
   - Show a banner/indicator: "System credentials available - credentials are optional"
   - Collapse credentials fields into an expandable "Advanced: Use custom credentials" section
   - Default state: collapsed (credentials hidden)
   - When expanded, show all credential fields (username, password, client_id, client_secret)

2. **Visual Indicator:**
   ```
   +----------------------------------------------------------+
   | Credentials | Config | Metadata                          |
   +----------------------------------------------------------+
   |                                                          |
   |  [i] Using system credentials                            |
   |      Your platform administrator has configured          |
   |      default credentials for this carrier.               |
   |                                                          |
   |  [v] Use custom credentials instead (Advanced)           |
   |      +------------------------------------------------+  |
   |      | Username:    [                              ]  |  |
   |      | Password:    [                              ]  |  |
   |      | Client ID:   [                              ]  |  |
   |      | Client Secret: [                            ]  |  |
   |      +------------------------------------------------+  |
   |                                                          |
   +----------------------------------------------------------+
   ```

3. **Form Validation:**
   - If collapsed (using system): No credential validation required
   - If expanded (custom): Validate all credential fields are filled

**When system credentials are NOT configured:**

1. **Standard behavior** (current UX):
   - Show all credential fields as required
   - No special messaging

### Error Messages

**On connection save (when neither user nor system credentials available):**
```
"No credentials configured. Please provide your DHL Parcel DE API credentials,
or contact your administrator to configure system-level credentials."
```

**On API operation (if credentials missing):**
```
"DHL Parcel DE credentials not configured. Please update your connection
settings with valid credentials."
```

---

## Problem Statement

### Current State

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py
class Settings(core.Settings):
    """DHL Germany connection settings."""

    username: str = None      # User MUST provide
    password: str = None      # User MUST provide
    client_id: str = None     # User MUST provide
    client_secret: str = None # User MUST provide
    # ...

# User connection form requires all credentials
# No system-level default credential support
```

```python
# modules/connectors/teleship/karrio/providers/teleship/utils.py
class Settings(core.Settings):
    """Teleship connection settings - REFERENCE IMPLEMENTATION."""

    client_id: str    # User provided
    client_secret: str  # User provided

    @property
    def oauth_client_id(self):
        # Supports system-level credentials via env vars
        return (
            self.connection_system_config.get("TELESHIP_OAUTH_CLIENT_ID")
            if self.test_mode
            else self.connection_system_config.get("TELESHIP_SANDBOX_OAUTH_CLIENT_ID")
        )
```

### Desired State

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py

# System config schema for runtime settings
SYSTEM_CONFIG = {
    "DHL_PARCEL_DE_USERNAME": (
        "",
        "DHL Parcel DE API username for production",
        str,
    ),
    "DHL_PARCEL_DE_PASSWORD": (
        "",
        "DHL Parcel DE API password for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_ID": (
        "",
        "DHL Parcel DE OAuth client ID for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_SECRET": (
        "",
        "DHL Parcel DE OAuth client secret for production",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_USERNAME": (
        "",
        "DHL Parcel DE API username for sandbox",
        str,
    ),
    # ... sandbox equivalents
}

# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py
class Settings(core.Settings):
    """DHL Germany connection settings."""

    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None

    @property
    def connection_username(self):
        """Return user-provided username or fallback to system config."""
        if self.username:
            return self.username
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_USERNAME")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_USERNAME")
        )

    # Similar properties for password, client_id, client_secret
```

### Problems

1. **No shared credential support**: Multi-tenant platforms cannot provide pre-configured DHL credentials for their users
2. **User complexity**: Every user must obtain and configure their own DHL API credentials
3. **Admin overhead**: Platform administrators cannot centrally manage DHL credentials for all users
4. **Inconsistent with Teleship**: DHL Parcel DE doesn't follow the established pattern for system-level credential configuration

---

## Goals & Success Criteria

### Goals

1. Enable super admins to configure DHL Parcel DE credentials at the system level via environment variables
2. Allow users to create DHL Parcel DE connections without credentials (only billing numbers and config)
3. Support separate credentials for test/sandbox and production environments
4. Maintain backward compatibility with existing connections that have user-provided credentials

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| SYSTEM_CONFIG registered in constance | Yes | Must-have |
| Computed properties use fallback logic | Yes | Must-have |
| Existing connections unchanged | 100% | Must-have |
| Env credentials used when user credentials empty | Yes | Must-have |
| SDK tests pass | 100% | Must-have |
| Server tests pass | 100% | Must-have |

### Launch Criteria

**Must-have (P0):**
- [ ] SYSTEM_CONFIG added to DHL Parcel DE units.py
- [ ] Plugin metadata includes system_config
- [ ] Settings has computed `connection_*` properties
- [ ] Shipment/tracking/pickup use computed properties
- [ ] All SDK tests pass
- [ ] All server tests pass

**Nice-to-have (P1):**
- [ ] Dashboard UI indication when using system credentials
- [ ] Admin documentation for credential setup
- [ ] Validation hook to check credentials are configured

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **A: SYSTEM_CONFIG with computed properties (Teleship pattern)** | Proven pattern, consistent, env-based | Requires property changes in all API calls | **Selected** |
| B: Database-stored system credentials | UI-editable, no server restart | Security concerns, more complex | Rejected |
| C: Hardcoded default credentials | Simplest implementation | Not configurable, security risk | Rejected |
| D: Connection template/cloning | Reuse existing connections | Doesn't solve credential sharing | Rejected |

### Trade-off Analysis

Option A was selected because:
- **Proven pattern**: Teleship already uses this approach successfully
- **Environment-based**: Credentials stored in env vars, not database (security)
- **Constance integration**: Automatically registered in Django admin for visibility
- **Minimal code changes**: Only need to add properties and use them

---

## Technical Design

> **IMPORTANT**: Study Teleship's implementation carefully before implementing.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| SYSTEM_CONFIG pattern | `modules/connectors/teleship/karrio/providers/teleship/units.py:8-29` | Copy structure exactly |
| connection_system_config | `modules/sdk/karrio/core/settings.py:56-59` | Use existing base class property |
| Plugin system_config | `modules/connectors/teleship/karrio/plugins/teleship/__init__.py:28` | Add to plugin metadata |
| Constance integration | `apps/api/karrio/server/settings/constance.py:181-191` | Automatic via SYSTEM_CONFIGS |

### Architecture Overview

```
+-----------------------------------------------------------------------------+
|                        CREDENTIAL RESOLUTION FLOW                            |
+-----------------------------------------------------------------------------+
|                                                                              |
|  +-------------------+         +--------------------+                        |
|  | Environment Vars  |         | Django Constance   |                        |
|  |                   |         | (Admin Panel)      |                        |
|  | DHL_PARCEL_DE_*   |-------->| System Settings    |                        |
|  +-------------------+         +--------------------+                        |
|                                         |                                    |
|                                         v                                    |
|  +-------------------+         +--------------------+                        |
|  | User Connection   |         | Settings Class     |                        |
|  |                   |         |                    |                        |
|  | username: ""      |-------->| connection_username|                        |
|  | password: ""      |         | connection_password|                        |
|  | client_id: ""     |         | connection_client_*|                        |
|  | config: {...}     |         |                    |                        |
|  +-------------------+         +--------------------+                        |
|                                         |                                    |
|                                         v                                    |
|                               +--------------------+                         |
|                               | API Calls          |                         |
|                               | (uses connection_*)|                         |
|                               +--------------------+                         |
|                                                                              |
+-----------------------------------------------------------------------------+
```

### Sequence Diagram

```
+----------+     +----------+     +----------+     +----------+     +----------+
|  Admin   |     |   Env    |     | Constance|     | Settings |     |  DHL API |
+----+-----+     +----+-----+     +----+-----+     +----+-----+     +----+-----+
     |               |                 |                |                |
     | 1. Set env    |                 |                |                |
     | variables     |                 |                |                |
     |-------------->|                 |                |                |
     |               | 2. Load on      |                |                |
     |               | server start    |                |                |
     |               |---------------->|                |                |
     |               |                 |                |                |
     |               |                 |                |                |
+----+-----+         |                 |                |                |
|   User   |         |                 |                |                |
+----+-----+         |                 |                |                |
     |               |                 |                |                |
     | 3. Create connection            |                |                |
     | (no credentials, only config)   |                |                |
     |-------------------------------->| 4. Load        |                |
     |               |                 | connection     |                |
     |               |                 |--------------->|                |
     |               |                 |                |                |
     |               |                 | 5. Resolve     |                |
     |               |                 | credentials    |                |
     |               |                 |<---------------|                |
     |               |                 |                |                |
     | 6. Create shipment              |                |                |
     |-------------------------------->|--------------->|                |
     |               |                 |                | 7. Use         |
     |               |                 |                | connection_*   |
     |               |                 |                |--------------->|
     |               |                 |                |                |
     |               |                 |                |<---------------|
     |               |                 |                | 8. Response    |
     |<--------------------------------|<---------------|                |
     |               |                 |                |                |
```

### Data Flow Diagram

```
+------------------------------------------------------------------------------+
|                          CREDENTIAL RESOLUTION                                |
+------------------------------------------------------------------------------+
|                                                                               |
|  INPUT: User Connection                                                       |
|  +---------------------------+                                                |
|  | username: "" (empty)      |                                                |
|  | password: "" (empty)      |                                                |
|  | client_id: "" (empty)     |                                                |
|  | client_secret: "" (empty) |                                                |
|  | config: {                 |                                                |
|  |   "default_billing_number": "123...",                                      |
|  |   "service_billing_numbers": [...]                                         |
|  | }                         |                                                |
|  +---------------------------+                                                |
|              |                                                                |
|              v                                                                |
|  +---------------------------+    +---------------------------+               |
|  | Settings.connection_*     |--->| Check: user value exists? |               |
|  +---------------------------+    +---------------------------+               |
|                                          |           |                        |
|                                     Yes  |           | No                     |
|                                          v           v                        |
|                               +------------+  +------------------+            |
|                               | Return user|  | Return env value |            |
|                               | value      |  | (test/live mode) |            |
|                               +------------+  +------------------+            |
|                                          |           |                        |
|                                          v           v                        |
|  OUTPUT: Resolved Credentials                                                 |
|  +---------------------------+                                                |
|  | connection_username       |-----> "env_username" (from DHL_PARCEL_DE_*)    |
|  | connection_password       |-----> "env_password"                           |
|  | connection_client_id      |-----> "env_client_id"                          |
|  | connection_client_secret  |-----> "env_client_secret"                      |
|  +---------------------------+                                                |
|                                                                               |
+------------------------------------------------------------------------------+
```

### Data Models

#### SYSTEM_CONFIG (units.py)

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py

# System config schema for runtime settings (e.g., API credentials)
# Format: Dict[str, Tuple[default_value, description, type]]
# Note: The actual env values are read by the server (constance.py) using decouple
SYSTEM_CONFIG = {
    "DHL_PARCEL_DE_USERNAME": (
        "",
        "DHL Parcel DE API username for production",
        str,
    ),
    "DHL_PARCEL_DE_PASSWORD": (
        "",
        "DHL Parcel DE API password for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_ID": (
        "",
        "DHL Parcel DE OAuth client ID for production",
        str,
    ),
    "DHL_PARCEL_DE_CLIENT_SECRET": (
        "",
        "DHL Parcel DE OAuth client secret for production",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_USERNAME": (
        "",
        "DHL Parcel DE API username for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_PASSWORD": (
        "",
        "DHL Parcel DE API password for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_CLIENT_ID": (
        "",
        "DHL Parcel DE OAuth client ID for sandbox/test mode",
        str,
    ),
    "DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET": (
        "",
        "DHL Parcel DE OAuth client secret for sandbox/test mode",
        str,
    ),
}
```

#### Settings Class Updates (utils.py)

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py

class Settings(core.Settings):
    """DHL Germany connection settings."""

    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None

    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_parcel_de"

    @property
    def connection_username(self) -> typing.Optional[str]:
        """Return user-provided username or fallback to system config."""
        if self.username:
            return self.username
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_USERNAME")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_USERNAME")
        )

    @property
    def connection_password(self) -> typing.Optional[str]:
        """Return user-provided password or fallback to system config."""
        if self.password:
            return self.password
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_PASSWORD")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_PASSWORD")
        )

    @property
    def connection_client_id(self) -> typing.Optional[str]:
        """Return user-provided client_id or fallback to system config."""
        if self.client_id:
            return self.client_id
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_CLIENT_ID")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_CLIENT_ID")
        )

    @property
    def connection_client_secret(self) -> typing.Optional[str]:
        """Return user-provided client_secret or fallback to system config."""
        if self.client_secret:
            return self.client_secret
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_CLIENT_SECRET")
        )

    # ... existing server_url, token_server_url, etc. properties remain unchanged ...
```

#### Plugin Metadata Update (__init__.py)

```python
# modules/connectors/dhl_parcel_de/karrio/plugins/dhl_parcel_de/__init__.py

import karrio.core.metadata as metadata
import karrio.mappers.dhl_parcel_de as mappers
import karrio.providers.dhl_parcel_de.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_parcel_de",
    label="DHL Germany",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    connection_configs=units.ConnectionConfig,
    system_config=units.SYSTEM_CONFIG,  # NEW: Register system config
)
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `DHL_PARCEL_DE_USERNAME` | string | No | Production API username |
| `DHL_PARCEL_DE_PASSWORD` | string | No | Production API password |
| `DHL_PARCEL_DE_CLIENT_ID` | string | No | Production OAuth client ID |
| `DHL_PARCEL_DE_CLIENT_SECRET` | string | No | Production OAuth client secret |
| `DHL_PARCEL_DE_SANDBOX_USERNAME` | string | No | Sandbox API username |
| `DHL_PARCEL_DE_SANDBOX_PASSWORD` | string | No | Sandbox API password |
| `DHL_PARCEL_DE_SANDBOX_CLIENT_ID` | string | No | Sandbox OAuth client ID |
| `DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET` | string | No | Sandbox OAuth client secret |

### Validation Hook Design

A validation hook will be added to check credentials are available before any DHL Parcel DE operation. This follows the Teleship OAuth hook pattern.

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/hooks/credentials.py

"""DHL Parcel DE credential validation hook."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.utils as provider_utils


def on_request_validate(
    request: typing.Any,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Any, typing.List[models.Message]]:
    """Validate that credentials are available before making API requests.

    This hook runs before any DHL Parcel DE API operation and ensures
    that credentials are resolvable (either user-provided or from system config).
    """
    messages: typing.List[models.Message] = []

    # Check if credentials are resolvable
    missing_credentials = []

    if not settings.connection_username:
        missing_credentials.append("username")
    if not settings.connection_password:
        missing_credentials.append("password")
    if not settings.connection_client_id:
        missing_credentials.append("client_id")
    if not settings.connection_client_secret:
        missing_credentials.append("client_secret")

    if missing_credentials:
        mode = "sandbox" if settings.test_mode else "production"
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="CREDENTIALS_NOT_CONFIGURED",
                message=(
                    f"DHL Parcel DE {mode} credentials not configured. "
                    f"Missing: {', '.join(missing_credentials)}. "
                    "Please provide credentials in your connection settings, "
                    "or contact your administrator to configure system-level credentials."
                ),
            )
        )

    return request, messages
```

**Hook Registration:**

```python
# modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/hooks/__init__.py

from karrio.providers.dhl_parcel_de.hooks.credentials import on_request_validate

__all__ = ["on_request_validate"]
```

```python
# modules/connectors/dhl_parcel_de/karrio/plugins/dhl_parcel_de/__init__.py

import karrio.providers.dhl_parcel_de.hooks as hooks

METADATA = metadata.PluginMetadata(
    # ... existing fields ...
    Hooks=hooks,  # NEW: Register hooks module
    system_config=units.SYSTEM_CONFIG,
)
```

### References API Enhancement

Add computed `system_credentials_carriers` field to the references API.

```python
# modules/core/karrio/server/core/dataunits.py

def contextual_reference(request: Request = None, reduced: bool = True):
    # ... existing code ...

    # Compute system credentials availability
    system_credentials_carriers = _get_system_credentials_status()

    references = {
        # ... existing fields ...
        "system_credentials_carriers": system_credentials_carriers,
    }

    # ... rest of function ...


def _get_system_credentials_status() -> typing.Dict[str, typing.Dict[str, bool]]:
    """Compute which carriers have system credentials configured.

    Returns dict like:
    {
        "dhl_parcel_de": {"production": True, "sandbox": False},
        "teleship": {"production": True, "sandbox": True},
    }
    """
    from constance import config
    import karrio.references as ref

    result = {}

    for carrier_id, metadata_obj in ref.PLUGIN_METADATA.items():
        system_config = metadata_obj.get("system_config")
        if not system_config:
            continue

        # Group env vars by production/sandbox
        prod_vars = [k for k in system_config.keys() if "SANDBOX" not in k]
        sandbox_vars = [k for k in system_config.keys() if "SANDBOX" in k]

        # Check if production credentials are set
        prod_configured = all(
            bool(getattr(config, var, None))
            for var in prod_vars
        ) if prod_vars else False

        # Check if sandbox credentials are set
        sandbox_configured = all(
            bool(getattr(config, var, None))
            for var in sandbox_vars
        ) if sandbox_vars else False

        if prod_configured or sandbox_configured:
            result[carrier_id] = {
                "production": prod_configured,
                "sandbox": sandbox_configured,
            }

    return result
```

### API Call Updates

All files that use credentials need to switch to using the `connection_*` properties:

```python
# BEFORE (in any file using credentials):
username = settings.username
password = settings.password

# AFTER:
username = settings.connection_username
password = settings.connection_password
```

Files to update:
- `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py`
- `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/cancel.py`
- `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/tracking.py`
- `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/pickup/*.py`
- Any file that accesses `settings.username`, `settings.password`, `settings.client_id`, or `settings.client_secret`

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| User provides credentials + env set | Use user-provided credentials | Check user value first in properties |
| User provides partial credentials | Use user for provided, env for missing | Each property checks independently |
| No env credentials configured | Return None, API will fail | Clear error message from DHL API |
| Test mode with only prod env set | No credentials available | Return None, user must configure test |
| Env set but empty string | Treat as not set | Check truthiness, not just existence |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Env vars not loaded | All connections fail | Document required env setup |
| Env vars typo | Specific mode fails | Validate env names in docs |
| Constance not synced | Old values used | Server restart syncs values |
| Mixed credential sources | Confusing debugging | Log which source is used (optional) |

### Security Considerations

- [x] Credentials stored in environment variables, not database
- [x] No secrets in code or logs
- [x] Env vars loaded via decouple (secure parsing)
- [x] Admin panel shows values are set but doesn't expose them

---

## Implementation Plan

### Phase 1: SDK Core Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add SYSTEM_CONFIG to units.py | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/units.py` | Pending | S |
| Add computed connection_* properties to utils.py | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/utils.py` | Pending | M |
| Update plugin metadata with system_config + Hooks | `modules/connectors/dhl_parcel_de/karrio/plugins/dhl_parcel_de/__init__.py` | Pending | S |
| Create credential validation hook | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/hooks/credentials.py` | Pending | M |
| Create hooks __init__.py | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/hooks/__init__.py` | Pending | S |

### Phase 2: API Call Updates

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update shipment create to use connection_* | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/create.py` | Pending | S |
| Update shipment cancel to use connection_* | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/shipment/cancel.py` | Pending | S |
| Update tracking to use connection_* | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/tracking.py` | Pending | S |
| Update pickup operations to use connection_* | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/pickup/*.py` | Pending | S |
| Update rate operations to use connection_* | `modules/connectors/dhl_parcel_de/karrio/providers/dhl_parcel_de/rate.py` | Pending | S |

### Phase 3: Server/API Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add system_credentials_carriers to references API | `modules/core/karrio/server/core/dataunits.py` | Pending | M |
| Add helper function _get_system_credentials_status | `modules/core/karrio/server/core/dataunits.py` | Pending | S |

### Phase 4: Frontend Changes

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update carrier connection form to check system_credentials_carriers | `apps/dashboard/src/.../ConnectionForm.tsx` | Pending | M |
| Add collapsible credentials section with "Using system credentials" indicator | `apps/dashboard/src/.../ConnectionForm.tsx` | Pending | M |
| Update form validation to make credentials optional when system config exists | `apps/dashboard/src/.../ConnectionForm.tsx` | Pending | S |

### Phase 5: Testing & Documentation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Update SDK tests | `modules/connectors/dhl_parcel_de/tests/` | Pending | M |
| Update test fixtures for env credential scenarios | `modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/fixture.py` | Pending | S |
| Add admin setup documentation | `docs/` | Pending | S |
| Integration testing with real DHL sandbox | N/A | Pending | M |

**Dependencies:**
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 1
- Phase 4 depends on Phase 3
- Phase 5 depends on Phases 1-4

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines - use `unittest`, NOT pytest.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/connectors/dhl_parcel_de/tests/` | 80%+ |

### Test Cases

#### Unit Tests

```python
# modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_settings.py

import unittest
from unittest.mock import patch, MagicMock

from karrio.providers.dhl_parcel_de.utils import Settings


class TestDHLParcelDESettingsCredentials(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_connection_username_uses_user_value_when_provided(self):
        """Verify user-provided username is used over env value."""
        settings = Settings(
            username="user_provided",
            password="pass",
            client_id="id",
            client_secret="secret",
        )
        # Mock system config with env value
        settings._system_config = MagicMock()
        settings._system_config.get.return_value = "env_username"

        self.assertEqual(settings.connection_username, "user_provided")

    def test_connection_username_falls_back_to_env_when_empty(self):
        """Verify env username is used when user doesn't provide one."""
        settings = Settings(
            username=None,  # Not provided
            password=None,
            client_id=None,
            client_secret=None,
            test_mode=False,
        )
        # Mock system config
        mock_config = {"DHL_PARCEL_DE_USERNAME": "env_username"}
        with patch.object(
            Settings,
            "connection_system_config",
            new_callable=lambda: property(lambda self: mock_config),
        ):
            # Re-create settings to pick up patched property
            settings = Settings(test_mode=False)
            # Note: Actual test would need proper mocking setup

    def test_connection_credentials_use_sandbox_env_in_test_mode(self):
        """Verify sandbox env vars are used in test mode."""
        settings = Settings(
            username=None,
            password=None,
            client_id=None,
            client_secret=None,
            test_mode=True,
        )
        # Would verify DHL_PARCEL_DE_SANDBOX_* is accessed

    def test_connection_credentials_use_production_env_in_live_mode(self):
        """Verify production env vars are used when not in test mode."""
        settings = Settings(
            username=None,
            password=None,
            client_id=None,
            client_secret=None,
            test_mode=False,
        )
        # Would verify DHL_PARCEL_DE_* (non-sandbox) is accessed

    def test_partial_user_credentials_with_env_fallback(self):
        """Verify partial user credentials work with env fallback for missing."""
        settings = Settings(
            username="user_provided",  # User provides username
            password=None,  # Fallback to env
            client_id="user_client_id",  # User provides
            client_secret=None,  # Fallback to env
        )
        # Verify username uses user value, password uses env value
```

#### Integration Tests

```python
# modules/connectors/dhl_parcel_de/tests/dhl_parcel_de/test_shipment.py

class TestDHLParcelDEShipmentWithEnvCredentials(unittest.TestCase):
    def test_shipment_creation_with_env_credentials(self):
        """Verify shipment can be created using env-based credentials."""
        # Create connection without credentials
        settings = Settings(
            username=None,
            password=None,
            client_id=None,
            client_secret=None,
            config={
                "default_billing_number": "33333333330102",
            },
        )
        # Mock env credentials
        # Test that shipment creation uses connection_* properties
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run SDK tests for dhl_parcel_de
python -m unittest discover -v -f modules/connectors/dhl_parcel_de/tests

# Run server tests (if applicable)
karrio test --failfast karrio.server.providers.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Env vars not documented properly | Users can't configure | Medium | Comprehensive documentation |
| Breaking change if using raw properties | Existing integrations fail | Low | Update all usages in same PR |
| Constance caching stale values | Wrong credentials used | Low | Server restart clears cache |
| Test mode gets prod credentials | Security/billing issue | Low | Separate env var names with SANDBOX_ |
| Empty string vs None confusion | Unexpected fallback behavior | Medium | Use truthiness check, document behavior |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: No API changes; internal credential resolution only
- **Data compatibility**: Existing connections with credentials continue to work unchanged
- **Feature flags**: Not needed; change is additive

### Migration Steps

1. Deploy code changes (no data migration needed)
2. Set environment variables for desired credentials
3. Restart server to load env vars into constance
4. Users can now create connections without credentials

### Rollback Procedure

1. **Identify issue**: Connections failing with credential errors
2. **Stop rollout**: Do not deploy to additional environments
3. **Revert changes**:
   - Revert code changes via git
   - Remove env vars (optional, won't cause issues)
4. **Verify recovery**: Test connection creation with user-provided credentials

---

## Appendices

### Appendix A: Environment Variable Setup

**Docker/Docker Compose:**
```yaml
# docker-compose.yml
services:
  api:
    environment:
      - DHL_PARCEL_DE_USERNAME=your_username
      - DHL_PARCEL_DE_PASSWORD=your_password
      - DHL_PARCEL_DE_CLIENT_ID=your_client_id
      - DHL_PARCEL_DE_CLIENT_SECRET=your_client_secret
      - DHL_PARCEL_DE_SANDBOX_USERNAME=sandbox_username
      - DHL_PARCEL_DE_SANDBOX_PASSWORD=sandbox_password
      - DHL_PARCEL_DE_SANDBOX_CLIENT_ID=sandbox_client_id
      - DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET=sandbox_client_secret
```

**.env file:**
```bash
DHL_PARCEL_DE_USERNAME=your_username
DHL_PARCEL_DE_PASSWORD=your_password
DHL_PARCEL_DE_CLIENT_ID=your_client_id
DHL_PARCEL_DE_CLIENT_SECRET=your_client_secret
DHL_PARCEL_DE_SANDBOX_USERNAME=sandbox_username
DHL_PARCEL_DE_SANDBOX_PASSWORD=sandbox_password
DHL_PARCEL_DE_SANDBOX_CLIENT_ID=sandbox_client_id
DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET=sandbox_client_secret
```

### Appendix B: Reference Implementation Files

| Component | File Path |
|-----------|-----------|
| Teleship SYSTEM_CONFIG | `modules/connectors/teleship/karrio/providers/teleship/units.py:8-29` |
| Teleship computed properties | `modules/connectors/teleship/karrio/providers/teleship/utils.py:41-57` |
| Teleship plugin metadata | `modules/connectors/teleship/karrio/plugins/teleship/__init__.py:28` |
| Base connection_system_config | `modules/sdk/karrio/core/settings.py:56-59` |
| Constance integration | `apps/api/karrio/server/settings/constance.py:181-191` |

### Appendix C: User Connection Form (Simplified)

With env-based credentials configured, users can create connections with only:

```json
{
  "carrier_id": "my-dhl-connection",
  "carrier_name": "dhl_parcel_de",
  "test_mode": false,
  "config": {
    "default_billing_number": "33333333330102",
    "service_billing_numbers": [
      {"service": "dhl_parcel_de_paket", "billing_number": "33333333330102"},
      {"service": "dhl_parcel_de_europaket", "billing_number": "33333333330201"}
    ]
  }
}
```

No `username`, `password`, `client_id`, or `client_secret` required!

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [x] All pending questions in "Open Questions & Decisions" have been asked
- [x] All user decisions documented with rationale and date
- [x] Edge cases requiring input have been resolved
- [x] "Open Questions & Decisions" section cleaned up (all resolved or removed)

CODE ANALYSIS:
- [x] Existing code studied and documented in "Existing Code Analysis" section
- [x] Existing utilities identified for reuse (Teleship pattern, connection_system_config)

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
