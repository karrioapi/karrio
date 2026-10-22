# Connection Config Enum Lists

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-10-22 |
| Status | Completed |
| Owner | Joaqim Planstedt |
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

---

## Executive Summary

A connector can declare a connection config whose value is an ordered list of enum values, such as a preference order of notification channels, but the SDK neither publishes the allowed values nor coerces the stored value into a list, and the dashboard has no widget for it.
This PRD makes the SDK publish the member names of a `typing.List[SomeEnum]` connection config as its `enum`, coerces every list connection config value into a list, and renders such configs in the carrier connection dialog as selectable, reorderable pills.

### Key Architecture Decisions

1. **Publish item enum names on list configs**: `typing.List[SomeEnum]` publishes `type: "list"` and `enum: [member names]`, the same `enum` key that single-value enum configs already use, so the dashboard needs no new reference field.
2. **Coerce all list configs, not only enum lists**: a string or other scalar stored for a list config becomes a one-item list; this includes the bare `list` configs `shipping_options` and `shipping_services`, which today turn a string into a list of characters.
3. **No item validation in the SDK**: list items pass through unchanged, so an unknown name reaches the connector, which rejects or ignores it.
4. **Every list-of-enum config renders as reorderable pills**: there is no opt-in flag; the order of the stored list is the user's preference order.
5. **Native HTML5 drag events plus move buttons**: no new dependency; the ← and → buttons give a keyboard and screen-reader path for reordering.
6. **An empty selection is stored as unset**: the widget emits `null`, which the server's config merge drops, rather than `[]`.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| List coercion in `OptionEnum.__call__` | Django admin `SystemConnection` form |
| `enum` publishing for `typing.List[Enum]` connection configs and shipping options | Legacy `connect-provider-modal` |
| `parse_type` returning `list` before the `enum` substring check | `apps/www` documentation site |
| `OrderedEnumPills` component in `packages/ui` | Built `elements` bundle |
| Wiring in `carrier-connection-dialog.tsx`, including default pre-fill for new connections | Any connector change; the first consumer ships separately |

---

## Open Questions & Decisions

### Pending Questions

None.

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Which list configs are coerced | All list configs, including bare `list` | A string stored for `shipping_options` becoming characters is the same defect | 2026-10-22 |
| D2 | Coercion rules | `None` → `None`; `list`/`tuple` → `list(value)`; any other value, a string included → `[value]` | Matches how a single value set through the API or an environment-sourced default is meant | 2026-10-22 |
| D3 | Item validation | None in the SDK | The connector owns the meaning of each name | 2026-10-22 |
| D4 | Widget opt-in | Every list-of-enum renders as pills | No configs of this shape exist yet, so there is nothing to keep compatible | 2026-10-22 |
| D5 | Drag implementation | Native HTML5 drag and drop plus ←/→ buttons | Avoids a dependency; buttons cover keyboard and assistive technology | 2026-10-22 |
| D6 | Empty selection | Stored as `null` (unset) | `process_dictionaries_mutations` merges config, so omitting the key would keep the old value; `null` is stripped by `lib.to_dict` | 2026-10-22 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| A stored value contains a name outside the published enum | Widget could hide it | Rendered as a selected pill so it can be seen and removed | ❌ No |
| A stored value repeats a name | Duplicate pills | Rendered once, at its first position; the next edit saves it once | ❌ No |
| A `dict`, `set`, or other non-list iterable is stored | `list(value)` would yield keys or an arbitrary order | Treated as a scalar: `[value]` | ❌ No |
| Empty string stored for a list config | Becomes `[""]` | Follows D2 literally; the widget never writes `""` | ❌ No |

---

## Problem Statement

### Current State

```python
class ConnectionConfig(lib.Enum):
    postnord_default_notification = lib.OptionEnum(
        "postnord_default_notification", typing.List[NotificationChannel]
    )
    shipping_options = lib.OptionEnum("shipping_options", list)

# references publishes no enum for the list config:
# {"type": "list", ...}

# OptionEnum.__call__ for the bare list:
lib.OptionEnum("shipping_options", list)("signature").state
# ['s', 'i', 'g', 'n', 'a', 't', 'u', 'r', 'e']
```

`OptionEnum.__call__` and `references` both decide enum handling with `"enum" in str(type)`.
For `typing.List[X]` that string includes the module path of `X`, so a module path containing `enum` routes a list type into the single-value enum branch, and `references` then iterates the typing generic.

### Desired State

```python
lib.OptionEnum("shipping_options", list)("signature").state
# ['signature']

# references publishes:
# {
#     "name": "postnord_default_notification",
#     "code": "postnord_default_notification",
#     "required": False,
#     "type": "list",
#     "enum": ["sms", "email", "letter"],
# }
```

The dashboard shows the selected names as numbered pills in order, the unselected names as add-pills, and lets the user drag or move pills to change the order.

### Problems

1. **No published choices**: the dashboard cannot know which names a list config accepts.
2. **String values split into characters**: a single value for a bare `list` config is stored as a list of characters.
3. **Substring type detection**: list generics can be mistaken for enums by module path.
4. **No widget**: list configs without nested `fields` are not rendered at all.

---

## Goals & Success Criteria

### Goals

1. A connector declaring `lib.OptionEnum(code, typing.List[SomeEnum])` gets a working dashboard field without dashboard changes.
2. Every list connection config value read through `ConnectionConfigOptions` is `None` or a `list`.
3. Existing published references for all upstream connectors are unchanged.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| SDK unit tests for coercion and publishing | Pass, and fail against the unpatched SDK | Must-have |
| Full SDK and connector test suite | Pass unchanged | Must-have |
| TypeScript errors in `packages/ui` | No new errors | Must-have |
| Reordering without a pointer | Possible with ←/→ buttons | Must-have |

### Launch Criteria

**Must-have (P0):**
- [x] Coercion in `OptionEnum.__call__` for `list` and `typing.List[...]`
- [x] `enum` published for `typing.List[Enum]` connection configs
- [x] Pills widget wired into the carrier connection dialog

**Nice-to-have (P1):**
- [x] Same `enum` publishing for shipping options of type `typing.List[Enum]`
- [x] Published `default` pre-fills new connections

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Publish `enum` on list configs and render pills | Reuses the `enum` key; no new reference shape | `enum` now means "allowed items" for lists | **Selected** |
| New `item_enum` reference key | Explicit | Second key for the same concept; dashboard must read both | Rejected |
| Multi-select dropdown (`MultiSelect`) | Existing component | No ordering | Rejected |
| Drag-and-drop library | Polished interactions | New dependency for one widget | Rejected |
| Coerce only `typing.List[Enum]` | Smaller behaviour change | Leaves the character-splitting defect in `shipping_options` | Rejected |

### Trade-off Analysis

Reusing `enum` keeps the published shape flat and lets single-value and list configs share the same lookup in the dashboard, which already branches on `type`.
Coercing every list config changes behaviour for bare `list` configs, but only for values that were already broken: a string for a list config never produced a meaningful list.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `OptionEnum.__call__` | `modules/sdk/karrio/core/utils/enum.py` | Add a list branch before the enum substring check |
| `ConnectionConfigOptions` | `modules/sdk/karrio/core/units.py` | Unchanged; calls `OptionEnum` per key |
| `collect_references`, `parse_type` | `modules/sdk/karrio/references.py` | Shared `extract_enum_names` for options and connection configs |
| `extract_list_item_fields` | `modules/sdk/karrio/references.py` | Pattern for the new `extract_list_item_enum` |
| `process_dictionaries_mutations` | `modules/core/karrio/server/serializers/abstract.py` | Config merge; drops `None` values, which makes `null` mean unset |
| `Badge`, `Button`, lucide icons | `packages/ui/components/ui/` | Pill styling and controls |
| `renderConfigFields` | `packages/ui/components/carrier-connection-dialog.tsx` | New branch for `type === "list"` with `enum` and no `fields` |

### Architecture Overview

```
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ connector units.py   │     │ karrio.references    │     │ dashboard dialog     │
│ OptionEnum(code,     │────>│ type: "list"         │────>│ OrderedEnumPills     │
│   List[SomeEnum])    │     │ enum: [names]        │     │ (drag, ←/→, ×, +)    │
└──────────────────────┘     └──────────────────────┘     └──────────┬───────────┘
          ▲                                                          │ config[code]
          │                                                          ▼
┌─────────┴────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ ConnectionConfig-    │<────│ carrier connection   │<────│ GraphQL mutation     │
│ Options → OptionEnum │     │ config (JSON)        │     │ (merge, null drops)  │
│ coerces to list      │     └──────────────────────┘     └──────────────────────┘
└──────────────────────┘
```

### Sequence Diagram

```
┌────────┐        ┌──────────┐        ┌────────┐        ┌───────────┐
│  User  │        │ Dialog   │        │ Server │        │ Connector │
└───┬────┘        └────┬─────┘        └───┬────┘        └─────┬─────┘
    │ pick carrier     │                  │                   │
    │─────────────────>│ pre-fill default │                   │
    │ add/move pills   │                  │                   │
    │─────────────────>│                  │                   │
    │ save             │ config {code:[…]}│                   │
    │─────────────────>│─────────────────>│ store config      │
    │                  │                  │ rate/ship request │
    │                  │                  │──────────────────>│
    │                  │                  │  state: [names]   │
```

### Data Flow Diagram

```
stored value                OptionEnum(list or List[E]).state
────────────                ─────────────────────────────────
None                  ───>  None
"sms"                 ───>  ["sms"]
3                     ───>  [3]
["letter", "sms"]     ───>  ["letter", "sms"]   (new list, same order)
("email", "sms")      ───>  ["email", "sms"]
["sms", "pigeon"]     ───>  ["sms", "pigeon"]   (items not validated)
```

### Published Shape

| Field | Type | Present | Description |
|-------|------|---------|-------------|
| `name` | string | always | Enum member name of the config |
| `code` | string | always | `OptionEnum.code` |
| `required` | boolean | always | `false` |
| `type` | string | always | `"list"` |
| `enum` | string[] | when the item type is an `Enum` subclass | Member names in declaration order |
| `default` | string[] | when declared | Pre-fills new connections; declare as member names |

### Widget Behaviour

| Interaction | Result |
|-------------|--------|
| Click an add-pill | Appends the value to the end of the selection |
| Click × on a pill | Removes the value |
| Drag a pill onto another | Moves it to that position |
| Click ← or → | Moves the pill one position earlier or later |
| Remove the last pill | Emits `null`; the key is unset on save |
| Open a new connection for a carrier with a published `default` | The selection starts as the default |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| `typing.List[str]` config | `type: "list"`, no `enum` | Not rendered as pills; unchanged from today |
| `typing.List[AttrsClass]` config | `type: "list"`, `fields` | Object-array editor, unchanged |
| Enum name not in published `enum` | Kept and shown | Connector decides how to treat it |
| Duplicate names | Shown once; saved once after an edit | Widget de-duplicates |
| `default` declared and value `None` | `default` is used | Existing `OptionEnum` default handling, then coerced |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| A consumer relied on a string splitting into characters | List of characters becomes one-item list | No upstream connector reads a string from these configs; listed as a behaviour change |
| Browser without HTML5 drag events (touch) | Drag does not work | ←/→ buttons remain |

### Security Considerations

- [x] No credentials involved; connection configs are non-secret
- [x] Values are rendered as text, not HTML

---

## Implementation Plan

### Phase 1: SDK

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Coerce list connection config values | `modules/sdk/karrio/core/utils/enum.py` | Done | S |
| Coercion tests | `modules/sdk/tests/core/test_option_enum_list.py` | Done | S |
| Publish enum choices for list configs and options | `modules/sdk/karrio/references.py` | Done | S |
| Publishing tests | `modules/sdk/tests/core/test_references_connection_configs.py` | Done | S |

### Phase 2: Dashboard

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| `OrderedEnumPills` component | `packages/ui/components/ordered-enum-pills.tsx` | Done | M |
| Render enum list configs and pre-fill defaults | `packages/ui/components/carrier-connection-dialog.tsx` | Done | S |

**Dependencies:** Phase 2 reads the reference shape produced by Phase 1.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `modules/sdk/tests/core/test_option_enum_list.py` | Every coercion rule, default, `to_connection_config` |
| Unit Tests | `modules/sdk/tests/core/test_references_connection_configs.py` | Published shape for enum list, plain list, single enum, bare list; options; `parse_type` |
| Type check | `packages/ui` | No new `tsc --noEmit` errors |
| Manual | Dashboard connection dialog | Add, remove, drag, ←/→, empty save, default pre-fill |

### Running Tests

```bash
python -m unittest discover -v -f modules/sdk/tests
./bin/run-sdk-tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Bare-list coercion changes stored-string behaviour | Low | Low | Only affects values that were already malformed |
| `enum` on list options changes option forms | Low | Low | No upstream shipping option uses `typing.List[Enum]` |
| Test failures elsewhere | Medium | Low | Full SDK and connector suite run |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: references for existing connectors are unchanged; list configs that were already lists read the same.
- **Data compatibility**: no stored data changes; coercion applies on read.
- **Behaviour change**: a string or other scalar stored for any list connection config, including `shipping_options` and `shipping_services`, now reads as a one-item list instead of a list of characters.

### Rollback Procedure

1. Revert the dashboard commit; enum list configs are then not rendered.
2. Revert the SDK commits; list configs read as before and lose their published `enum`.
