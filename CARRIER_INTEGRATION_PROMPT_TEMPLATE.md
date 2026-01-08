# Carrier Integration Prompt Template

> **Purpose**: Concise prompt for AI agents implementing karrio carrier integrations.

---

## Prompt Template

```
You are implementing a new carrier integration for Karrio.

## Required Reading (In Order)

Before writing any code, read these files thoroughly:

1. **CARRIER_INTEGRATION_GUIDE.md** - Step-by-step integration process
2. **CARRIER_INTEGRATION_FAQ.md** - Common pitfalls and best practices
3. **AGENTS.md** - Coding style and project conventions

## Task

Implement a carrier integration for {CARRIER_NAME}.

- Carrier slug: {carrier_slug}
- Display name: {Display Name}
- API type: [JSON/XML]
- Features: [rating, shipping, tracking, pickup]
- API docs: {documentation_url}

## Process

1. Bootstrap using CLI (CARRIER_INTEGRATION_GUIDE.md Phase 1)
2. Generate schemas from API samples (Phase 2)
3. Implement features following patterns in FAQ sections 7-8
4. Write tests following the 4-test pattern (Phase 4)
5. Verify against FAQ best practices checklist
6. Run all success criteria commands (Phase 6)

## Reference Carriers

Study these for implementation patterns:
- DHL Express: `modules/connectors/dhl_express/` (single tree instantiation)
- Canada Post: `modules/connectors/canadapost/` (services inline)
- UPS: `modules/connectors/ups/` (options handling)
```

---

## Usage

### New Integration
```
[Paste template above with carrier details filled in]
```

### Adding Features
```
Add {FEATURE} to the existing {CARRIER_NAME} integration.
Follow CARRIER_INTEGRATION_GUIDE.md Phases 3-6.
Reference: modules/connectors/{reference_carrier}/
```

### Bug Fixes
```
Fix {ISSUE} in {CARRIER_NAME} integration.
Review CARRIER_INTEGRATION_FAQ.md for relevant best practices.
```

---

## See Also

- [CARRIER_INTEGRATION_GUIDE.md](./CARRIER_INTEGRATION_GUIDE.md)
- [CARRIER_INTEGRATION_FAQ.md](./CARRIER_INTEGRATION_FAQ.md)
- [AGENTS.md](./AGENTS.md)
