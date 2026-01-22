# [Feature/Change Title]

<!--
PRD TEMPLATE v1.0
=================
This template captures Karrio's established PRD patterns combined with industry
best practices from Google Design Docs and Anthropic's safety-first approach.

CRITICAL REQUIREMENTS:
- ALWAYS study related existing code and utilities before designing
- NEVER reinvent the wheel - search codebase for similar patterns to reuse
- Follow AGENTS.md coding style EXACTLY as the original authors
- Include ASCII diagrams: architecture overview, sequence, and dataflow
- ASK CLARIFYING QUESTIONS when edge cases or ambiguities arise

INTERACTIVE PRD CREATION PROCESS:
1. Research: Study existing code and identify patterns
2. Draft: Create initial PRD structure with known information
3. Identify Gaps: Flag edge cases, ambiguities, and decisions needing input
4. Ask Questions: Prompt user for clarification on architecture decisions
5. Update: Incorporate answers into the PRD
6. Iterate: Repeat steps 3-5 until all decisions are resolved
7. Finalize: Complete PRD with all decisions documented

WHEN TO ASK CLARIFYING QUESTIONS:
- Multiple valid architectural approaches exist
- Edge cases have no clear handling strategy
- Trade-offs require business/product input
- Scope boundaries are unclear
- Backward compatibility decisions needed
- Performance vs simplicity trade-offs

USAGE INSTRUCTIONS:
1. Copy this template for new PRDs
2. Study existing code in related modules FIRST
3. Fill in all required sections (marked with *)
4. STOP and ask questions when you encounter ambiguities or decision points
5. Document user decisions in the "Open Questions & Decisions" section
6. Include optional sections based on PRD type markers
7. Delete unused optional sections and these instructions
8. All code examples must follow AGENTS.md style exactly

PRD TYPE MARKERS:
<!-- INTEGRATION: Include for carrier integrations -->
<!-- REFACTORING: Include for refactoring/migration PRDs -->
<!-- ENHANCEMENT: Include for feature enhancements -->
<!-- ARCHITECTURE: Include for system design PRDs -->
-->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | YYYY-MM-DD |
| Status | Planning / In Progress / Completed |
| Owner | [Name/Team] |
| Type | Integration / Refactoring / Enhancement / Architecture |
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
8. [Testing Strategy](#testing-strategy)
9. [Risk Assessment](#risk-assessment)
10. [Migration & Rollback](#migration--rollback)
11. [Appendices](#appendices)

---

## Executive Summary

<!-- * REQUIRED: 2-3 sentence overview of the change -->

[Brief description of what this PRD proposes and why it matters.]

### Key Architecture Decisions

<!-- * REQUIRED: Numbered list of major technical decisions -->

1. **[Decision 1]**: [Rationale]
2. **[Decision 2]**: [Rationale]
3. **[Decision 3]**: [Rationale]

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| [Feature/change included] | [Explicitly excluded items] |
| [Another included item] | [Another excluded item] |

---

## Open Questions & Decisions

<!--
* REQUIRED during PRD creation process
* This section tracks questions raised and decisions made during PRD development
* Move resolved questions to "Resolved Decisions" once answered
* Delete this section or mark all as resolved before final PRD submission
-->

### Pending Questions

<!-- Questions that need user/stakeholder input before proceeding -->

| # | Question | Context | Options | Status |
|---|----------|---------|---------|--------|
| Q1 | [Question needing clarification] | [Why this matters] | A) Option 1, B) Option 2 | ⏳ Pending |
| Q2 | [Edge case question] | [Impact on design] | A) Option 1, B) Option 2 | ⏳ Pending |

### Resolved Decisions

<!-- Document answers received and rationale for decisions made -->

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | [What was decided] | [Selected option] | [Why this choice] | YYYY-MM-DD |

### Edge Cases Requiring Input

<!-- Specific edge cases identified that need architecture decisions -->

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| [Edge case scenario] | [What breaks or is unclear] | [Suggested approach] | ✅ Yes / ❌ No |

---

## Problem Statement

<!-- * REQUIRED: Describe current state, desired state, and specific problems -->

### Current State

<!-- Show code examples demonstrating the problem -->

```python
# Current implementation example
# Highlight what's problematic
```

### Desired State

<!-- Show code examples demonstrating the solution -->

```python
# Proposed implementation example
# Highlight improvements
```

### Problems

<!-- Numbered list of specific issues this PRD addresses -->

1. **[Problem 1]**: [Description and impact]
2. **[Problem 2]**: [Description and impact]
3. **[Problem 3]**: [Description and impact]

---

## Goals & Success Criteria

<!-- * REQUIRED -->

### Goals

1. [Goal 1 - specific and measurable]
2. [Goal 2 - specific and measurable]
3. [Goal 3 - specific and measurable]

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| [Metric 1] | [Target value] | Must-have |
| [Metric 2] | [Target value] | Must-have |
| [Metric 3] | [Target value] | Nice-to-have |

### Launch Criteria

<!-- From Google Design Docs pattern -->

**Must-have (P0):**
- [ ] [Critical requirement 1]
- [ ] [Critical requirement 2]

**Nice-to-have (P1):**
- [ ] [Optional improvement 1]
- [ ] [Optional improvement 2]

---

## Alternatives Considered

<!-- * REQUIRED: Show you've evaluated other approaches -->

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| [Option A] | [Benefits] | [Drawbacks] | **Selected** / Rejected |
| [Option B] | [Benefits] | [Drawbacks] | Selected / **Rejected** |
| [Option C] | [Benefits] | [Drawbacks] | Selected / **Rejected** |

### Trade-off Analysis

[Explain why the selected approach was chosen over alternatives. Consider:
- Performance implications
- Maintenance burden
- Migration complexity
- Developer experience]

---

## Technical Design

<!-- * REQUIRED -->

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

<!-- * REQUIRED: Document what existing code was studied -->

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| [Existing utility/pattern] | `path/to/file.py` | [How it will be reused] |
| [Related implementation] | `path/to/file.py` | [Reference for patterns] |

### Architecture Overview

<!-- ASCII diagram showing system components and their relationships -->

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Component  │────>│  Component  │────>│  Component  │
│      A      │     │      B      │     │      C      │
└─────────────┘     └─────────────┘     └─────────────┘
        │                  │                   │
        └──────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Database  │
                    └─────────────┘
```

### Sequence Diagram

<!-- ASCII sequence diagram showing component interactions over time -->

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ Client │     │  API   │     │ Mapper │     │ Carrier│
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │
    │  1. Request  │              │              │
    │─────────────>│              │              │
    │              │  2. Create   │              │
    │              │─────────────>│              │
    │              │              │  3. Call API │
    │              │              │─────────────>│
    │              │              │              │
    │              │              │  4. Response │
    │              │              │<─────────────│
    │              │  5. Parse    │              │
    │              │<─────────────│              │
    │  6. Result   │              │              │
    │<─────────────│              │              │
    │              │              │              │
```

### Data Flow Diagram

<!-- ASCII diagram showing how data transforms through the system -->

```
┌──────────────────────────────────────────────────────────────────┐
│                         REQUEST FLOW                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────┐│
│  │ Unified │───>│   Mapper    │───>│   Carrier   │───>│ Carrier││
│  │ Payload │    │ (transform) │    │   Payload   │    │   API  ││
│  └─────────┘    └─────────────┘    └─────────────┘    └────────┘│
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                         RESPONSE FLOW                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────┐│
│  │ Unified │<───│  Provider   │<───│   Carrier   │<───│ Carrier││
│  │ Response│    │  (parse)    │    │  Response   │    │   API  ││
│  └─────────┘    └─────────────┘    └─────────────┘    └────────┘│
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Models

<!-- Show Python/TypeScript code for new or modified models -->

```python
# Python model example
@attr.s(auto_attribs=True)
class NewModel:
    """Description of the model."""

    field_one: str          # Field description
    field_two: int = None   # Optional field with default
```

```typescript
// TypeScript type example
interface NewType {
  fieldOne: string;    // Field description
  fieldTwo?: number;   // Optional field
}
```

### Field Reference

<!-- Table format for field mappings, especially useful for integrations -->

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_one` | string | Yes | Description |
| `field_two` | int | No | Description with default: `0` |

<!-- INTEGRATION: Include this section for carrier integrations -->
### API Changes

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/resource` | Create new resource |
| GET | `/api/v1/resource/{id}` | Get resource by ID |

**Request/Response:**

```json
// Request example
{
  "field": "value"
}

// Response example
{
  "id": "abc123",
  "field": "value",
  "created_at": "2025-01-15T10:00:00Z"
}
```

---

## Edge Cases & Failure Modes

<!-- * REQUIRED: Anthropic safety-first pattern -->

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| [Edge case 1] | [What should happen] | [How it's handled] |
| [Edge case 2] | [What should happen] | [How it's handled] |
| [Empty/null input] | [What should happen] | [How it's handled] |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| [Failure scenario 1] | [User/system impact] | [Prevention/recovery] |
| [Failure scenario 2] | [User/system impact] | [Prevention/recovery] |
| [External service down] | [User/system impact] | [Prevention/recovery] |

<!-- ARCHITECTURE: Include for security-sensitive changes -->
### Security Considerations

- [ ] Input validation for all user-provided data
- [ ] No secrets in code or logs
- [ ] Proper authentication/authorization checks
- [ ] SQL injection prevention
- [ ] XSS prevention (if applicable)

---

## Implementation Plan

<!-- * REQUIRED -->

### Phase 1: [Phase Name]

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| [Task 1] | `path/to/file.py` | Pending | S/M/L |
| [Task 2] | `path/to/file.ts` | Pending | S/M/L |

### Phase 2: [Phase Name]

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| [Task 3] | `path/to/file.py` | Pending | S/M/L |
| [Task 4] | `path/to/file.ts` | Pending | S/M/L |

**Dependencies:** Phase 2 depends on Phase 1 completion.

<!-- REFACTORING: Include for migration PRDs -->
### Phase 3: Migration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| [Migration task 1] | `migrations/` | Pending | M |
| [Data backfill] | `scripts/` | Pending | M |

---

## Testing Strategy

<!-- * REQUIRED: Follow AGENTS.md testing guidelines EXACTLY -->

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly as the original authors:
> - Use `unittest` for SDK/connector tests (NOT pytest - we do NOT use pytest anywhere)
> - Use Django tests via `karrio` for server tests
> - Run tests from repository root
> - Use functional, declarative style (map/filter/comprehensions over loops)
> - Prefer comprehensive `assertDictEqual`/`assertListEqual` over multiple single assertions
> - Use `mock.ANY` for dynamic fields (id, created_at, updated_at)
> - Add `print(response)` before assertions when debugging, remove when tests pass
> - Study existing test files in similar modules for patterns to follow

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests | `tests/test_*.py` | 80%+ |
| Integration Tests | `tests/integration/` | Key flows |
| E2E Tests | `tests/e2e/` | Critical paths |

### Test Cases

#### Unit Tests

```python
"""Example test following AGENTS.md patterns."""

import unittest
from unittest.mock import patch, ANY

class TestFeatureName(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_expected_behavior(self):
        """Verify [specific behavior]."""
        result = function_under_test(input_data)

        # Use comprehensive assertions per AGENTS.md
        self.assertDictEqual(
            result,
            {
                "field": "expected_value",
                "id": ANY,  # Use mock.ANY for dynamic fields
            }
        )
```

#### Integration Tests

```python
def test_api_endpoint(self):
    """Verify API endpoint behavior."""
    response = self.client.post('/api/endpoint', data={...})
    # print(response)  # Uncomment for debugging
    self.assertResponseNoErrors(response)
    self.assertDictEqual(response.data, expected_data)
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run SDK tests
python -m unittest discover -v -f path/to/tests

# Run server tests
karrio test --failfast karrio.server.module.tests
```

---

## Risk Assessment

<!-- * REQUIRED -->

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
| [Breaking changes] | High | Low | [Backward compatibility approach] |
| [Test failures] | Medium | Medium | [Run full test suite before merge] |

---

## Migration & Rollback

<!-- * REQUIRED for changes affecting existing data or behavior -->

### Backward Compatibility

<!-- Describe how existing functionality is preserved -->

- **API compatibility**: [How existing API consumers are unaffected]
- **Data compatibility**: [How existing data is handled]
- **Feature flags**: [If using feature flags for gradual rollout]

<!-- REFACTORING: Include for data migrations -->
### Data Migration

```python
# Migration script example
def migrate_data():
    """Migrate existing records to new schema."""
    # Implementation following AGENTS.md patterns
    pass
```

**Migration Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Rollback Procedure

<!-- Describe how to revert if issues arise -->

1. **Identify issue**: [How to detect problems]
2. **Stop rollout**: [Immediate actions]
3. **Revert changes**: [Specific revert steps]
4. **Verify recovery**: [Validation steps]

---

## Appendices

<!-- Optional: Include supporting materials -->

### Appendix A: [Title]

<!-- Example: Code examples, field mappings, reference links -->

### Appendix B: [Title]

<!-- Example: API response samples, carrier documentation links -->

<!-- INTEGRATION: Include for carrier integrations -->
### Appendix C: Carrier-Specific Reference

**API Documentation:**
- [Link to carrier API docs]

**Field Mappings:**

| Karrio Field | Carrier Field | Notes |
|--------------|---------------|-------|
| `tracking_number` | `TrackingID` | Direct mapping |
| `status` | `StatusCode` | Requires enum translation |

---

<!--
CHECKLIST BEFORE SUBMISSION:

INTERACTIVE PROCESS:
- [ ] All pending questions in "Open Questions & Decisions" have been asked
- [ ] All user decisions documented with rationale and date
- [ ] Edge cases requiring input have been resolved
- [ ] "Open Questions & Decisions" section cleaned up (all resolved or removed)

CODE ANALYSIS:
- [ ] Existing code studied and documented in "Existing Code Analysis" section
- [ ] Existing utilities identified for reuse (karrio.lib, hooks, components)

CONTENT:
- [ ] All required sections completed
- [ ] Code examples follow AGENTS.md style EXACTLY as original authors
- [ ] Architecture diagrams included (overview, sequence, dataflow - ASCII art)
- [ ] Tables used for structured data (not prose)
- [ ] Before/After code shown in Problem Statement
- [ ] Success criteria are measurable
- [ ] Alternatives considered and documented
- [ ] Edge cases and failure modes identified

TESTING:
- [ ] Test cases follow unittest patterns (NOT pytest)
- [ ] Test examples use assertDictEqual/assertListEqual with mock.ANY

RISK & MIGRATION:
- [ ] Risk assessment completed
- [ ] Migration/rollback plan documented
-->
