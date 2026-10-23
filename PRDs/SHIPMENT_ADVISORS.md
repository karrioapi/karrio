# Shipment Advisors Plugin Hook

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-09-25 |
| Status | Completed |
| Owner | Joaqim Planstedt |
| Type | Enhancement / Architecture |
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

Plugins can register carriers or address validators, but nothing lets a plugin contribute to a rate or shipment request while it is processed.
This PRD adds a `shipment_advisors` field to `PluginMetadata`: plugin-provided callables that receive the unified request and a non-secret carrier context and return advisory `Message` objects, which the SDK appends to rate and shipment responses.
Regional or organisational shipping conventions, such as "email the commercial invoice for this lane", can then ship as independently versioned plugins instead of living in carrier connectors or core.

### Key Architecture Decisions

1. **One advisor signature for both operations**: `(request, context) -> Iterable[Message]`, with `context.operation` set to `rating` or `shipping`, because conventions usually apply at both moments and one list keeps the registration surface small.
2. **Context built from an allowlist**: `AdvisorContext` copies `carrier_name`, `carrier_id`, `account_country_code`, `test_mode`, and a deep copy of `config`; credentials are connector-specific attrs fields with no generic marker, so a denylist would leak new ones.
3. **Advisory only**: advisors run after the carrier call on a deep copy of the request, never see the carrier response, and any level other than `info` or `warning` is reported as `warning`.
4. **Failure isolation with one broad exception handler**: a raising advisor becomes a `shipment_advisor_failed` warning naming the plugin; this is the single deliberate `except Exception` (see [Appendix A](#appendix-a-rationale-for-the-single-broad-exception-handler)).
5. **Advise only gateways with a result**: advisors run per rating gateway that still has rates after `filter_rates`, and per shipment creation that returned shipment details.
6. **Persist purchase-time messages**: the server merges the messages returned by shipment creation into `shipment.messages`, de-duplicated by `(carrier_id, code, message)`.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| `PluginMetadata.shipment_advisors` field and `advisor` plugin type | Any concrete convention (shipped as separate community plugins) |
| Advisor registry in `karrio.references` | Advisors for tracking, pickups, manifests, documents |
| Advisor context, runner, and isolation in `karrio.core.advisors` | Advisor ordering, priorities, or configuration in server or dashboard |
| Invocation in `Rating.fetch` and `Shipment.create` | Per-rate (rather than per-response) messages |
| Persisting purchase-time messages on the shipment | Timeouts for slow advisors |
| SDK documentation page | Changes to carrier connectors or generated files |

---

## Open Questions & Decisions

### Pending Questions

None.

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | One or two metadata fields | One `shipment_advisors` list | Conventions usually apply at rating and shipping; advisors branch on `context.operation` | 2026-09-24 |
| D2 | How to keep credentials away from advisors | Allowlisted `AdvisorContext` | Credentials are arbitrary connector-specific fields; a denylist leaks new ones | 2026-09-24 |
| D3 | When to run advisors | After the carrier call, only for gateways with a result | Advice about an operation that then aborts is noise | 2026-09-24 |
| D4 | How to report a broken advisor | Warning `shipment_advisor_failed` with `details: {plugin, error}` | `lib.failsafe` discards the error; the failure must be visible | 2026-09-24 |
| D5 | Registry caching | Uncached `get_advisors()` | `lru_cache` accessors pin the first registry object and miss a later `import_extensions()` | 2026-09-24 |
| D6 | Server change | Persist messages returned at purchase | Advisor messages at purchase would otherwise be dropped | 2026-09-24 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Rate gateway whose rates are all removed by `filter_rates` | Advice would make a no-rate response carry messages | Treated as "no rates": no advice, so the server's 424 rule is unchanged | ❌ No |
| Return shipment | Advisor could reason about the wrong shipper | Advisor receives the swapped request, as sent to the carrier | ❌ No |
| Carrier warnings at purchase (e.g. `customs_omitted_intra_eu`) | Previously dropped, now persisted | Accepted behaviour change, listed in the changelog | ❌ No |

---

## Problem Statement

### Current State

`PluginMetadata` describes carrier and LSP integrations only (`modules/sdk/karrio/core/metadata.py`).
A plugin without Mapper, Proxy, and Settings is typed `unknown`, and nothing in `Rating.fetch` or `Shipment.create` (`modules/sdk/karrio/api/interface.py`) consults plugins.
Every warning message in a response is parsed from a carrier response; no SDK component emits karrio-authored advisories.

```python
# The only place for a lane convention today is inside a connector or core
def parse_shipment_response(response, settings):
    ...
    messages = error.parse_error_response(response, settings)
    # a "SE -> NO needs an emailed invoice" reminder would have to be hardcoded here
    return details, messages
```

The server also discards the messages returned by shipment creation at purchase: `buy_shipment_label` keeps only the messages stored at rating.

### Desired State

```python
import karrio.core.metadata as metadata
import karrio.core.models as models


def invoice_email_advisor(request, context):
    if context.operation != "shipping":
        return []

    if (request.shipper.country_code, request.recipient.country_code) != ("SE", "NO"):
        return []

    return [
        models.Message(
            carrier_name=None,
            carrier_id=None,
            code="commercial_invoice_email",
            level="warning",
            message="Email the commercial invoice to the recipient",
        )
    ]


METADATA = metadata.PluginMetadata(
    id="lane_conventions",
    label="Lane Conventions",
    shipment_advisors=[invoice_email_advisor],
)
```

### Problems

1. **No extension point**: conventions that are neither carrier behaviour nor core behaviour have nowhere to live.
2. **Connector pollution**: putting conventions in connectors couples regional policy to carrier protocol code and duplicates it across carriers.
3. **Lost purchase-time messages**: non-blocking warnings returned when a label is purchased never reach API consumers.

---

## Goals & Success Criteria

### Goals

1. A plugin can declare advisors in metadata and is collected even when it registers no carrier or address validator.
2. Advisor messages appear on rate and shipment responses for each carrier gateway that produced a result.
3. Advisors cannot reach credentials, block operations, or alter requests or carrier responses.
4. Purchase-time messages persist on the purchased shipment.

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Responses without advisor plugins | Identical to before (asserted by tests) | Must-have |
| Credential reachability from `AdvisorContext` | None (asserted by test) | Must-have |
| Raising advisor | Operation succeeds; `shipment_advisor_failed` warning | Must-have |
| Spec scenarios covered by tests | 100% | Must-have |
| Documentation example | Verified by a unit test | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [x] SDK advisor tests pass (`modules/sdk/tests/core/test_shipment_advisors.py`, 28 tests)
- [x] Manager and core server suites pass (`karrio.server.manager.tests`, `karrio.server.core.tests`)
- [x] No generated files or connectors changed

**Nice-to-have (P1):**
- [x] SDK documentation page with a tested example plugin

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Single `shipment_advisors` list with `context.operation` | One registration surface | Advisors branch on operation | **Selected** |
| Separate `rate_advisors` and `shipment_advisors` | Explicit per operation | Doubles registration; conventions usually apply at both | **Rejected** |
| Denylist of credential field names per connector | Exposes the full settings | Credentials have no generic marker; new fields leak | **Rejected** |
| Run advisors before the carrier call | Advice even when the carrier fails | Advice about aborted operations is noise | **Rejected** |
| Wrap advisors with `lib.failsafe` | Existing utility | Discards the error; failure must be reported | **Rejected** |
| Let advisors mutate or veto the request | More powerful plugins | Breaks the advisory contract; hard to reason about | **Rejected** |

### Trade-off Analysis

The selected design adds one optional metadata field, one registry, and one runner shared by both operations, so plugins without advisors and deployments without advisor plugins take the same code paths as before (the runner returns early on an empty registry).
Running advisors after the carrier call costs nothing when the carrier fails and keeps the server's no-rates handling unchanged.
Advisors run synchronously, so a slow advisor delays the call; advisors are expected to be pure functions of the request and context, and timeouts are a possible follow-up.

---

## Technical Design

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `PluginMetadata`, `plugin_types`, `plugin_type` | `modules/sdk/karrio/core/metadata.py` | New field after `system_config`; `advisor` added to type reporting |
| `import_extensions`, `SYSTEM_CONFIGS` collection | `modules/sdk/karrio/references.py` | `ADVISORS` reset and filled beside `SYSTEM_CONFIGS` from `PLUGIN_METADATA` |
| `collect_references` plugin listing | `modules/sdk/karrio/references.py` | Unchanged; reports `advisor` through `plugin_type(s)` |
| `Settings` generic fields | `modules/sdk/karrio/core/settings.py` | Read only: `carrier_name`, `carrier_id`, `account_country_code`, `test_mode`, `config` |
| `Message` model | `modules/sdk/karrio/core/models.py` | Advisor output type; `attr.evolve` fills identity and level |
| `Rating.fetch` / `flatten()` / `filter_rates` | `modules/sdk/karrio/api/interface.py` | Advisors run per gateway after filtering; `run_asynchronously` preserves gateway order |
| `Shipment.create` deserialize closures | `modules/sdk/karrio/api/interface.py` | Wrapped by `advise_shipment` with `payload` or `swapped_payload` |
| `check_operation`, `fail_safe` | `modules/sdk/karrio/api/interface.py` | Aborted and failed gateways yield no details or rates, so no advice |
| `is_sdk_message` | `modules/core/karrio/server/core/utils.py` | Advisor codes avoid `SHIPPING_SDK_` |
| `buy_shipment_label` | `modules/manager/karrio/server/manager/serializers/shipment.py` | Adds `merge_messages` of stored and returned messages |
| `karrio.core.utils.logger` | `modules/sdk/karrio/core/utils/logger.py` | Logs advisor failures |

### Architecture Overview

```
┌──────────────────────────┐        ┌──────────────────────────────┐
│ advisor plugin package   │        │ carrier plugin package       │
│ METADATA = PluginMetadata│        │ METADATA = PluginMetadata    │
│   shipment_advisors=[f]  │        │   Mapper, Proxy, Settings    │
└────────────┬─────────────┘        │   shipment_advisors=[g] (opt)│
             │ entry point /        └──────────────┬───────────────┘
             │ karrio.plugins                      │
             └──────────────┬──────────────────────┘
                            ▼
              ┌───────────────────────────┐
              │ references.import_        │
              │ extensions()              │
              │  PLUGIN_METADATA          │
              │  ADVISORS = [(id, f), ...]│
              └─────────────┬─────────────┘
                            │ get_advisors()
                            ▼
┌──────────────────┐  ┌───────────────────────────┐  ┌───────────────────┐
│ Rating.fetch     │─>│ core.advisors.run_advisors│<─│ Shipment.create   │
│ flatten() per    │  │ AdvisorContext (allowlist)│  │ advise_shipment() │
│ gateway w/ rates │  │  deepcopy(request)        │  │ when details      │
└────────┬─────────┘  │  normalize / isolate      │  └────────┬──────────┘
         │            └───────────────────────────┘           │
         ▼                                                    ▼
  (rates, messages + advice)                   (details, messages + advice)
                                                              │
                                                              ▼
                                         ┌──────────────────────────────────┐
                                         │ server buy_shipment_label        │
                                         │ shipment.messages =              │
                                         │  merge_messages(stored, returned)│
                                         └──────────────────────────────────┘
```

### Sequence Diagram

```
┌────────┐   ┌──────────────┐   ┌─────────┐   ┌─────────┐   ┌──────────────┐
│ Server │   │ Shipment API │   │ Gateway │   │ Carrier │   │ run_advisors │
└───┬────┘   └──────┬───────┘   └────┬────┘   └────┬────┘   └──────┬───────┘
    │ 1. create     │                │             │               │
    │──────────────>│ 2. check_operation           │               │
    │               │───────────────>│             │               │
    │               │ 3. request (swapped if return)│              │
    │               │───────────────>│ 4. call API │               │
    │               │                │────────────>│               │
    │               │                │ 5. response │               │
    │               │                │<────────────│               │
    │               │ 6. parse -> (details, messages)              │
    │               │<───────────────│             │               │
    │               │ 7. details present? run advisors on payload  │
    │               │─────────────────────────────────────────────>│
    │               │                │  8. per advisor: deepcopy,  │
    │               │                │  call, normalize or report  │
    │               │ 9. advice      │             │               │
    │               │<─────────────────────────────────────────────│
    │ 10. (details, messages + advice)             │               │
    │<──────────────│                │             │               │
    │ 11. merge_messages into shipment.messages    │               │
    │               │                │             │               │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                       ADVISOR INPUT                                  │
├──────────────────────────────────────────────────────────────────────┤
│  unified request ──deepcopy──> advisor(request_copy, context)        │
│  gateway.settings ──allowlist──> AdvisorContext                      │
│     carrier_name, carrier_id, account_country_code, test_mode,       │
│     operation, deepcopy(config)          (no credentials, id, meta)  │
├──────────────────────────────────────────────────────────────────────┤
│                       ADVISOR OUTPUT                                 │
├──────────────────────────────────────────────────────────────────────┤
│  Iterable[Message] ──normalize──> Message                            │
│     carrier_name/carrier_id ← context when missing                   │
│     level ∉ {info, warning} → warning                                │
│  raises / invalid output ──> Message(code="shipment_advisor_failed", │
│                                level="warning",                      │
│                                details={plugin, error})              │
│  response messages = carrier messages + advisor messages             │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Models

```python
# modules/sdk/karrio/core/metadata.py
@attr.s(auto_attribs=True)
class PluginMetadata:
    ...
    system_config: Optional[Dict[str, Any]] = None
    # Shipment advisors: callables (request, context) -> Iterable[Message]
    # run during rating and shipment creation (see karrio.core.advisors)
    shipment_advisors: List[Callable] = attr.Factory(list)


# modules/sdk/karrio/core/advisors.py
@attr.s(auto_attribs=True, frozen=True)
class AdvisorContext:
    carrier_name: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    account_country_code: typing.Optional[str] = None
    test_mode: bool = False
    operation: typing.Optional[AdvisorOperation] = None
    config: dict = attr.Factory(dict)
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `PluginMetadata.shipment_advisors` | `List[Callable]` | No | Advisors `(request, context) -> Iterable[Message]`; default `[]` |
| `AdvisorContext.carrier_name` | `str` | No | Carrier name of the connection |
| `AdvisorContext.carrier_id` | `str` | No | Carrier id of the connection |
| `AdvisorContext.account_country_code` | `str` | No | Connection account country code |
| `AdvisorContext.test_mode` | `bool` | No | Connection test mode; default `False` |
| `AdvisorContext.operation` | `"rating"` or `"shipping"` | No | Operation being advised |
| `AdvisorContext.config` | `dict` | No | Deep copy of the connection `config` |

### API Changes

No endpoint or schema changes.
Rate and shipment responses may carry additional `warning` or `info` messages when advisor plugins are installed.
`POST /v1/shipments/{id}/purchase` and single-call purchases now return and persist the messages returned by shipment creation in `messages`, alongside the messages stored at rating.

```json
{
  "status": "created",
  "messages": [
    {"carrier_name": "canadapost", "carrier_id": "canadapost", "code": "rate_warning", "level": "warning", "message": "Rated with default dimensions"},
    {"carrier_name": "canadapost", "carrier_id": "canadapost", "code": "shipment_advice", "level": "warning", "message": "Email the commercial invoice to the recipient"}
  ]
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| No advisor plugin installed | Responses identical to before | `run_advisors` returns `[]`; `advise_shipment` returns the parsed result object unchanged |
| Rate gateway returns no rates, or all are filtered | No advice for that gateway | Advice only when `any(rates)` after `filter_rates` |
| Gateway aborted by `check_operation` | No advice | Abortion yields no rates or details |
| Carrier rejects the shipment | No advice | `advise_shipment` skips when `details is None` |
| Return shipment | Advisor sees shipper and recipient swapped | `swapped_payload` passed to `advise_shipment` |
| Advisor mutates the request | Carrier request and other advisors unaffected | Each advisor gets `copy.deepcopy(request)` |
| Advisor returns `None` | No messages | `advisor(...) or []` |
| Advisor returns `error` level or no level | Reported as `warning` | `_normalize` |
| Advisor omits carrier identity (`None`) | Filled from context | `_normalize` |
| Same message stored at rating and returned at purchase | Stored once | `merge_messages` keeps the first per `(carrier_id, code, message)` |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Advisor raises | Would fail rating or shipping | Caught in `_advise`; `shipment_advisor_failed` warning naming the plugin; other advisors still run |
| Advisor returns non-`Message` items | Would break normalization | Validation runs inside the same handler; reported as `shipment_advisor_failed` |
| Advisor is slow | Delays rating and shipping calls | Documented expectation of fast, pure advisors; timeouts are a follow-up |
| `import_extensions()` re-run | Stale advisors | `ADVISORS` reset on every import; accessor uncached |

### Security Considerations

- [x] Advisors cannot reach credentials: `AdvisorContext` is built from an allowlist and never holds the settings object, `id`, or `metadata`.
- [x] `config` is deep-copied, so advisors cannot mutate the connection configuration.
- [x] No secrets in logs: failures log the plugin id and error string only.
- [x] No change to authentication, authorization, or tenant scoping; the server change reuses the shipment already scoped to the request context.

---

## Implementation Plan

### Phase 1: SDK

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| `shipment_advisors` field, `has_advisors`, `advisor` plugin type | `modules/sdk/karrio/core/metadata.py` | Done | S |
| `ADVISORS` registry and uncached `get_advisors()` | `modules/sdk/karrio/references.py` | Done | S |
| `AdvisorContext`, `run_advisors`, `_advise`, `_normalize` | `modules/sdk/karrio/core/advisors.py` (new) | Done | M |
| Invocation in `Rating.fetch` (`flatten()`) and `Shipment.create` (`advise_shipment`) | `modules/sdk/karrio/api/interface.py` | Done | M |
| SDK tests | `modules/sdk/tests/core/test_shipment_advisors.py` (new) | Done | M |

### Phase 2: Server

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| `merge_messages` in `buy_shipment_label` | `modules/manager/karrio/server/manager/serializers/shipment.py` | Done | S |
| `TestShipmentPurchaseMessages` | `modules/manager/karrio/server/manager/tests/test_shipments.py` | Done | S |

### Phase 3: Documentation

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Advisor contract page and sidebar entry | `apps/www/docs/carriers/sdk/advisors.mdx` (new), `apps/www/sidebars.js` | Done | S |
| This PRD | `PRDs/SHIPMENT_ADVISORS.md` (new) | Done | S |

**Dependencies:** Phase 2 depends on Phase 1 for advisor messages, but the persistence change is independent of advisors and also applies to carrier warnings.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| SDK unit and interface tests (`unittest`) | `modules/sdk/tests/core/test_shipment_advisors.py` | Every spec scenario |
| Server API test (`karrio test`) | `modules/manager/karrio/server/manager/tests/test_shipments.py` | Purchase-time persistence |

### Test Cases

| Test class | Tests | Covers |
|------------|-------|--------|
| `TestPluginMetadataAdvisors` | 4 | `advisor` type, carrier plus advisor types, unchanged types without advisors, no shared default list |
| `TestAdvisorRegistry` | 3 | Collection through the entry point discovery path, reset on re-import, `advisor` in `collect_references` |
| `TestAdvisorContext` | 3 | Allowlist only (no API key, secret, metadata, id), deep-copied config, immutability |
| `TestRunAdvisors` | 7 | No advisors, level downgrade, request isolation, failure isolation, invalid output, identity filling, operation in context |
| `TestRatingAdvisors` | 2 | One advice per rating gateway with rates; none for no-rate or aborted gateways |
| `TestShipmentAdvisors` | 4 | Advice on success with details unchanged; none on failure or abort; swapped request for returns |
| `TestWithoutAdvisors` | 3 | Rate, shipment, and return shipment responses unchanged without advisors |
| `TestDocumentedAdvisorPlugin` | 2 | The documentation example plugin, copied verbatim, is typed `advisor` and advises shipments only |
| `TestShipmentPurchaseMessages` (server) | 1 | Purchased shipment returns and persists rate and purchase messages once each |

The SDK file holds 28 tests: 26 for the implementation and 2 for the documentation example.
Interface tests use `MagicMock` gateways and patch `references.ADVISORS`; the server test patches `karrio.server.core.gateway.utils.identity` like the existing purchase tests and asserts both the API response and the stored model with one `assertDictEqual`.

```python
class TestRunAdvisors(unittest.TestCase):
    def test_failing_advisor_is_reported_and_others_still_run(self):
        messages = self.run_with(
            ("broken_plugin", failing_advisor),
            ("conventions", country_advisor),
        )

        self.assertListEqual(
            lib.to_dict(messages),
            [
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "shipment_advisor_failed",
                    "level": "warning",
                    "message": "Shipment advisor from plugin 'broken_plugin' failed",
                    "details": {"plugin": "broken_plugin", "error": "advisor exploded"},
                },
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "country_advice",
                    "level": "warning",
                    "message": "shipper country SE",
                },
            ],
        )
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# SDK advisor tests
python -m unittest -v modules/sdk/tests/core/test_shipment_advisors.py

# Server tests
karrio test --failfast karrio.server.manager.tests
karrio test --failfast karrio.server.core.tests
```

### Requirement Coverage

| Spec requirement | Scenario | PRD section | Tests |
|------------------|----------|-------------|-------|
| Plugins declare shipment advisors in their metadata | Advisor-only plugin is collected | Data Models; Architecture Overview | `TestPluginMetadataAdvisors.test_advisor_only_plugin_is_typed_advisor`, `TestAdvisorRegistry` |
| | Carrier plugin with advisors reports both types | Data Models | `test_carrier_plugin_with_advisors_reports_both_types` |
| | Plugins without advisors are unaffected | Edge Cases | `test_plugins_without_advisors_keep_their_types`, `TestWithoutAdvisors` |
| Advisors run during rating and shipment creation | Advisor message appears on a shipment response | Sequence Diagram | `test_advisor_message_is_added_to_successful_shipment` |
| | No advisor messages for gateways without a result | Edge Cases | `test_no_advice_for_gateways_without_rates_or_aborted`, `test_no_advice_for_failed_shipment`, `test_no_advice_for_aborted_shipment` |
| | Return shipments are advised on the swapped request | Edge Cases | `test_return_shipment_is_advised_on_swapped_request` |
| | Advisor runs per carrier when rating several carriers | Architecture Overview | `test_advisor_runs_once_per_carrier_with_rates` |
| Advisors receive no credentials | Credentials are absent from the advisor context | Data Flow Diagram; Security Considerations | `test_context_exposes_only_allowlisted_fields`, `test_context_config_is_a_deep_copy` |
| Advisor messages are advisory only | Error-level advisor message is downgraded | Data Flow Diagram; Edge Cases | `test_levels_above_warning_are_downgraded` |
| | Advisor cannot change the request | Edge Cases | `test_mutating_advisor_leaves_request_unchanged` |
| Failing advisors are isolated | Raising advisor is reported and skipped | Failure Modes; Appendix A | `test_failing_advisor_is_reported_and_others_still_run`, `test_invalid_advisor_output_is_reported_as_failure` |
| Purchase-time advisor messages persist on the shipment | Purchase-time advisory is visible on the purchased shipment | API Changes; Implementation Plan Phase 2 | `TestShipmentPurchaseMessages.test_purchase_persists_shipment_creation_messages` |

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Slow advisor delays every rate and shipment call | Medium | Low | Documented expectation of fast, pure advisors; timeouts as follow-up |
| Reviewers object to the broad exception handler | Low | Medium | Confined to one call site; rationale in the docstring and Appendix A |
| Purchase-time carrier warnings newly visible (e.g. `customs_omitted_intra_eu`) | Low | High | Non-breaking additive messages; covered by a Django test and listed as a behaviour change |
| Breaking changes | High | Low | Optional field with empty default; no schema or endpoint change; unchanged-response tests |
| Test failures | Medium | Low | SDK and server suites run before merge |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: no endpoint or schema change; responses gain messages only when advisor plugins are installed, and purchase responses gain the messages returned at purchase.
- **Data compatibility**: `shipment.messages` is an existing JSON field; no migration.
- **Plugin compatibility**: existing plugins keep their types and behaviour; `shipment_advisors` defaults to an empty list.

### Rollback Procedure

1. **Identify issue**: unexpected messages in rate or shipment responses, or `shipment_advisor_failed` warnings.
2. **Stop rollout**: uninstall the advisor plugin; responses return to the pre-change shape.
3. **Revert changes**: revert the feature commits; no data migration to undo.
4. **Verify recovery**: run the SDK and server test suites.

---

## Appendices

### Appendix A: Rationale for the single broad exception handler

`karrio.core.advisors._advise` wraps each advisor call in `except Exception`, a deliberate exception to the repository rule against catching bare `Exception`.
Advisors are third-party plugin code whose failure modes are unknown, and the contract guarantees that a broken plugin never fails rating or shipping.
Catching specific exceptions would let any unanticipated error type abort a label purchase because of an optional convention plugin.
`lib.failsafe` is not used because it discards the error, and the failure must be reported to the API consumer as a `shipment_advisor_failed` warning with `details: {plugin, error}` and logged.
The handler scope is one advisor call, including validation of its returned value, so a malformed return is reported rather than breaking the operation; carrier calls, parsing, and the rest of the SDK keep their existing error handling.

### Appendix B: Commits

| Commit | Summary |
|--------|---------|
| `dc2369fb3` | feat(sdk): add shipment_advisors field to plugin metadata |
| `c69e60f99` | feat(sdk): collect shipment advisors from discovered plugins |
| `6d39092dd` | feat(sdk): add allowlisted advisor context |
| `37cc990a0` | feat(sdk): add failure-isolated shipment advisor runner |
| `9c68b3967` | feat(sdk): run shipment advisors per rating gateway with rates |
| `823460f84` | feat(sdk): run shipment advisors after successful shipment creation |
| `a6dab1739` | test(sdk): verify responses are unchanged without advisor plugins |
| `5d7ff38a2` | style(sdk): format advisor runner |
| `53d5e45df` | feat(server): persist purchase-time shipment messages |
| `a91cc9995` | docs(sdk): document shipment advisors |
