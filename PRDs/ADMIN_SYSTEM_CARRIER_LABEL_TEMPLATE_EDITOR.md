# Admin Label-Template Editor for System Carriers

## Executive Summary

Platform admins need to define label templates on system carriers so every tenant who enables such a carrier gets the rendered label automatically.
The runtime propagation already works: brokered connections resolve credentials from their system connection at gateway-build time, and the generic connector renders `credentials.label_template` through `generate_label`.
The gap is tooling: the admin console has no editor, and the label preview endpoint reads an attribute that no longer exists on the redesigned models.

### Key Architecture Decisions

| Decision | Choice |
|---|---|
| Template storage | `credentials.label_template` on the SystemConnection (no new graph input fields) |
| Downstream propagation | Existing BrokeredConnection credential delegation — no core changes |
| Editor component | Reuse `LabelTemplateEditModal` from `@karrio/ui` (landed with the user-connections editor) |
| Access control | Admin-only by construction: SystemConnection mutations require admin permissions |

### Scope

In scope: admin UI for editing system-carrier label templates; label.pdf preview endpoint repair; regression tests.
Out of scope: tenant-owned connection inheritance (each `CarrierConnection` keeps its own template); non-generic carriers (label_template is generic-connector-only); shipment-meta display-name propagation for brokered generics (`gateway.py:326`).

## Problem Statement

### Current State

The redesigned connections architecture is three-tier:

```
CarrierConnection      tenant-owned user connections (credentials JSON)
SystemConnection       admin-managed platform-wide carriers (credentials JSON)
BrokeredConnection     a tenant's enabled instance of a SystemConnection
                       (credentials delegate to the system connection)
```

The label-template editor restored for user connections lives in the tenant dashboard only.
The admin console (`/admin/carriers`, system connections tab) edits credentials as raw JSON with no template editor.
The label preview endpoint reads `carrier.label_template` (views/carriers.py:286), an attribute absent from the redesigned `CarrierConnection` model, so previews fail (static analysis: AttributeError swallowed into a 409).

### Desired State

Admins edit a system generic carrier's label template from `/admin/carriers` with the same modal UX as tenants.
Saving writes `credentials.label_template` through the existing system-connection update mutation.
Every brokered tenant of that carrier renders labels with the template immediately (cache versioning on `updated_at` already propagates credential edits).
The preview endpoint resolves the template from connection credentials and returns a rendered PDF.

## Goals & Success Criteria

1. Admin opens `/admin/carriers`, sees an edit-label action on generic system connections, edits and saves a template.
2. A tenant with that system carrier enabled generates a label rendered through the admin template, with no tenant-side action.
3. `GET /v1/carriers/{id}/label.pdf` returns a rendered template for connections carrying one (and its previous behavior otherwise).
4. Non-generic carriers show no edit-label action.
5. Admin graph tests and endpoint tests pass; admin app typechecks and builds.

## Alternatives Considered

| Alternative | Why rejected |
|---|---|
| Top-level `label_template` on the system-connection graph input | Schema churn; credentials already persist and serialize the field through the generic settings mapper |
| Inheritance: tenant-owned connections fall back to the system carrier's template | Blurs the tenancy boundary; admins would influence tenant-owned connection rendering; each owned connection already has its own editor |
| Separate admin-only template store keyed by carrier | New model + resolution layer for a flow the credential delegation already provides |

## Technical Design

### Existing Code Analysis

| Component | Location | Behavior |
|---|---|---|
| Label rendering | modules/sdk/karrio/addons/label.py:11-45 | Reads `settings.label_template`; default SVG when unset; no fallback chain |
| Generic-only wiring | modules/sdk/karrio/universal/mappers/shipping_proxy.py:21,45 | Proxy wired solely into the generic connector |
| Generic settings typing | modules/connectors/generic/karrio/mappers/generic/settings.py:28 | `label_template` is a declared, persisted connection field |
| Brokered credential delegation | modules/core/karrio/server/providers/models/connection.py:610-672 | `data` merges system credentials; gateway built from them; cache keyed on system `updated_at` |
| System connection update | modules/core/karrio/server/providers/serializers/base.py:336-398 | Hand-rolled credentials merge, then maps through `CONNECTION_SERIALIZERS[carrier_code]` |
| Admin credentials read-back | modules/admin .../schemas/base/types.py:112-115 | Admin type returns full decrypted credentials |
| Admin UI data hooks | packages/admin/modules/carriers/index.tsx:7,120-125,205-215 | `useSystemConnections`/`useSystemConnectionMutation`; `handleUpdate` already sends credentials JSON |
| Broken preview | modules/core/karrio/server/providers/views/carriers.py:286 | Reads nonexistent `carrier.label_template`; 409 on error (line 272) |

### Architecture Overview

```
                    /admin/carriers (packages/admin)
                          |
                          | useSystemConnectionMutation
                          | { id, credentials: {..., label_template} }
                          v
                   SystemConnection ----------------------+
                    (admin credentials JSON)               |
                          |                                | updated_at
                          | _get_credentials()             | cache busting
                          v                                v
                   BrokeredConnection ----------> gateway cache
                    (per enabled tenant)             |
                          |                          |
                          | data = system creds      |
                          |                 + overrides
                          v                          v
                    generic Settings -----> create_shipment
                          |                          |
                          v                          v
                   generate_label <---- settings.label_template
```

### Data Flow (edit → downstream)

1. Admin opens editor; modal hydrates from `connection.credentials.label_template` (admin type returns full credentials).
2. Save sends the system-connection update mutation with credentials including `label_template`.
3. Serializer merges credentials and maps through the generic settings serializer; `updated_at` advances.
4. Brokered gateway caches invalidate on next resolution; tenant label generation picks up the new template.

## Implementation Plan

| File | Change |
|---|---|
| packages/admin/modules/carriers/index.tsx | Add edit-label action (generic system connections only), mount `LabelTemplateEditModal` from `@karrio/ui`, save via existing mutation with hydrated credentials |
| modules/core/karrio/server/providers/views/carriers.py | Resolve template from connection credentials (owned and delegated) instead of the dead attribute |
| modules/core tests (providers views) | Endpoint test: generic connection with template renders; without template keeps prior behavior |

### Open Questions (resolve during implementation)

1. Does the system-connection update serializer accept a partial credentials delta (`{ label_template }` only) or require the full dict?
   The admin type exposes full decrypted credentials, so hydrating and sending the full dict is viable either way; verify by test.
   NOTE: a live deployment reports that saving a template on a tenant CarrierConnection shows success but persists nothing — the same credentials-round-trip assumption is under active investigation; resolve that root cause first and revisit this question with its findings.
2. Preview endpoint semantics for brokered connections (tenant hitting preview for a brokered system carrier): resolve via delegation or restrict to the system connection itself.
   Prefer whichever the existing permission scoping already permits.

## Open-Question Resolutions (implementation addendum)

1. Partial credentials delta is viable; the editor sends `{ id, credentials: { label_template } }`.
   `SystemConnectionModelSerializer.update` merges the delta into the decrypted existing credentials before mapping through the generic settings serializer, which keeps `label_template` now that object-typed settings map to `CarrierSettingsDictField` (landed on the parent branch as the root-cause fix for the tenant save-persistence bug).
   Pinned by `TestAdminSystemConnectionLabelTemplate` in `modules/admin/karrio/server/admin/tests/test_connections.py`, which also asserts the other credential keys survive the partial update.
   No full-dict hydration is required.

2. The preview endpoint resolves `CarrierConnection` first, then `SystemConnection`, and keeps its 409 error response when neither matches.
   This serves the admin editor's preview button for system carriers while leaving tenant-owned behavior unchanged.
   Brokered connections remain unserved: no UI path previews them (the tenant modal opens only on owned connections), matching the "restrict" side of the question and the endpoint's existing authenticated, not-org-scoped posture.
   Template reads go through `get_credentials()` so encrypted-credential editions resolve identically.
   Pinned by `test_label_preview_for_system_connection` and `test_label_preview_unknown_connection` in `modules/core/karrio/server/providers/tests/test_label_preview.py`.

Verification: `karrio.server.admin.tests` (96 tests), `karrio.server.providers.tests` (26), and `karrio.server.graph.tests` (108) pass via the worktree overlay runner; `tsc --noEmit` on `packages/admin` is clean; the `@karrio/dashboard` production build (which compiles the admin carriers page) succeeds.
The manual dev-deployment check from the testing strategy remains open.

## Testing Strategy

Backend: unittest/Django tests for the preview endpoint (with and without template); existing admin and provider suites stay green.
Frontend: `tsc --noEmit` on the admin package and a production build of the admin app; no component-test harness exists.
Manual: admin edit on dev deployment, then a tenant brokered shipment rendering the admin template.
