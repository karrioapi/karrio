# Triage Inbox Skill

Surface the top 5 karrio engineering items for the day, ranked and tagged. Bridge between the **Notion Agent Inbox** (cross-domain capture surface) and the **Linear Karrio Maintenance project** (engineering source of truth). Approval-gated — never auto-acts.

## Two-Surface Architecture

```
NOTION Agent Inbox            LINEAR Karrio Maintenance
(any role: Eng/Chief/         (engineering execution —
 Logger/Research/Admin)        agents read state here)

  capture ──promote──►  EBE-### issue ──branch──► PR ──merge──► Done
  (user approves)                                  (auto-update via
                                                    EBE-### in title)
```

- **Notion** = capture + reflection. The skill never works directly off Inbox items; it promotes the Eng-tagged ones into Linear first.
- **Linear** = canonical engineering backlog. Issue IDs (`EBE-###`) embed in branch names so parallel agents don't collide.
- **GitHub** = code only (issues are disabled on `karrioapi/karrio`). PR titles include `[EBE-###]` so Linear auto-moves issues to In Review / Done.

## When to Use

- Start of a karrio working day (morning triage)
- Before opening a new Conductor workspace ("what should I pick up?")
- Whenever the Notion Inbox grows beyond ~10 pending Eng-tagged items

## Modes

This skill has **two modes**. The user picks; default is `triage`.

| Mode | Purpose |
|---|---|
| `triage` (default) | Rank Linear backlog + surface top 5. Recommend workspaces. |
| `promote` | Walk through Notion Inbox `Pending` items tagged `Eng`, propose Linear issues, create on approval. |

## Inputs

| Source | Tool | Filter |
|---|---|---|
| Linear backlog | `mcp__claude_ai_Linear__list_issues` | `project: "Karrio Maintenance"`, `state: Backlog` or `Todo` |
| Notion Agent Inbox | `mcp__claude_ai_Notion__notion-search` on `collection://e8147767-2ae6-43df-a1f5-9d89c2312640` | `Status = Pending` AND (`Agent = Eng` OR `Agent` is empty) |
| In-repo TODOs (optional) | `Grep "TODO\|FIXME"` | only when explicitly asked |

### Reference IDs

| Surface | ID |
|---|---|
| Linear team | `Eben Labs` (`EBE`) — `12c98fbb-796b-498b-9674-7e634219c964` |
| Linear project | `Karrio Maintenance` — `da42e101-382d-4c57-a90b-a12204ca5c31` |
| Notion Inbox | `collection://e8147767-2ae6-43df-a1f5-9d89c2312640` |

### Notion Inbox schema

| Field | Values |
|---|---|
| `Task` | title (required) |
| `Status` | `Pending` / `Approved` / `Done` / `Rejected` |
| `Risk Level` | `Low` / `Medium` / `High` |
| `Suggested Action` | free text |
| `Link` | URL |
| `Agent` | `Chief` / `Logger` / `Eng` / `Research` / `Admin` |

### Linear scope labels (created)

| Label | When to apply |
|---|---|
| `scope/connector` | `modules/connectors/<carrier>/` |
| `scope/server` | Django API, models, migrations, GraphQL, Huey jobs |
| `scope/frontend` | `apps/dashboard/`, `packages/` |
| `scope/release` | version bumps, changelog |
| `scope/docs` | README, AGENTS.md, in-repo docs |
| `scope/chore` | CI, deps, lint, infra |
| `needs-PRD` | requires `PRDs/<name>.md` before work starts (see `.claude/rules/prd-and-review.md`) |
| `Bug` / `Feature` / `Improvement` | workspace-level (pre-existing) |

---

## Mode: `triage` (default)

### 1. Pull Linear backlog

```
mcp__claude_ai_Linear__list_issues with
  project: "Karrio Maintenance"
  state: "Backlog"   (also pull "Todo" — those are next-up)
  limit: 50
```

If the backlog is empty, **switch to `promote` mode** automatically — the user has nothing to triage.

### 2. Rank

Sort by:
1. `priority = 1 (Urgent)` first — outages or release blockers
2. `Bug` label before `Feature`/`Improvement` (production over polish)
3. Smallest scope first (single `scope/connector` before cross-module work)
4. `state = Todo` before `state = Backlog` (already accepted into the queue)
5. Freshness (newer `updatedAt` wins ties)

Cap output at **5 items**. Life OS rule is "max 3 priorities per week" — surface 5 so the user picks 1-3.

### 3. Recommend workspace + role

For each surfaced item, suggest:

| Label combo | Suggested skill / Conductor workspace |
|---|---|
| `scope/connector` | `carrier-integration` skill, workspace `EBE-{n}-{carrier}-{short}` |
| `scope/server` + `Bug` | `debugging` skill, current workspace OK if scoped |
| `scope/server` + `needs-PRD` | `create-prd` skill first, then fresh workspace |
| `scope/frontend` | fresh workspace `EBE-{n}-{short}` (no dedicated skill yet — flagged gap) |
| `scope/release` | `release` skill, dedicated release workspace |
| `Bug` w/o scope | gstack `/investigate` |

Workspace naming convention: **`EBE-{issue-number}-{short-slug}`**. The branch becomes the same. Linear auto-links the PR when `[EBE-{n}]` appears in the PR title.

### 4. Output

```
## Triage — <date>

| # | Pri | Labels | Issue | Suggested action | Workspace |
|---|---|---|---|---|---|
| 1 | Urgent | scope/connector, Bug | EBE-12 SmartKargo fractional seconds | `debugging` skill | EBE-12-smartkargo-seconds |
| 2 | High | scope/server, needs-PRD | EBE-9 Tenant-scoped webhook retries | Write PRD first | EBE-9-webhook-retries |
| ... |
```

Below the table:
- **Skipped:** items that didn't make the top 5 with one-line reason each
- **Backlog health:** count by status, count by scope; flag if Backlog > 30
- **Notion Inbox status:** count of `Pending` Eng-tagged items not yet promoted

### 5. Approval gate

Wait for the user to pick items. Do **not**:
- Move Linear issues to `Todo` / `In Progress` automatically
- Spawn Conductor workspaces
- Modify branch state

Once the user picks issue `EBE-{n}`:
- `mcp__claude_ai_Linear__save_issue` with `id: "EBE-{n}", state: "Todo"` (or `In Progress` if they're starting now)
- Print the exact Conductor command for the workspace + the branch name

---

## Mode: `promote`

For pushing Notion Inbox items into Linear. Run when:
- Linear backlog is sparse and Notion Inbox has Eng-tagged Pending items
- User explicitly says "promote" / "drain the inbox"

### 1. Pull Eng-tagged Pending Inbox items

```
mcp__claude_ai_Notion__notion-search with
  query: ""
  data_source_url: "collection://e8147767-2ae6-43df-a1f5-9d89c2312640"
```

Filter results in-process to `Status = Pending` AND (`Agent = Eng` OR `Agent` empty).

### 2. For each item, draft a Linear issue

Build a draft per Inbox row:

| Linear field | Source |
|---|---|
| `team` | `Eben Labs` |
| `project` | `Karrio Maintenance` |
| `title` | Notion `Task` field |
| `description` | Notion `Suggested Action` + Notion row URL as "Source" link |
| `priority` | Map Notion `Risk Level`: High → 2 (High), Medium → 3 (Medium), Low → 4 (Low) |
| `labels` | Inferred scope label(s) from keyword matching, plus `Bug` / `Feature` / `Improvement` |
| `state` | `Backlog` |

#### Scope inference (from `Task` text)

| Tag | Trigger keywords |
|---|---|
| `scope/connector` | carrier name (UPS, FedEx, SmartKargo, ...), `mapper`, `proxy`, `provider`, `rate`, `tracking`, `shipment` |
| `scope/server` | `Django`, `migration`, `model`, `serializer`, `viewset`, `huey`, `graphql` |
| `scope/frontend` | `dashboard`, `next`, `react`, `apps/dashboard`, `packages/ui` |
| `scope/release` | `version`, `changelog`, `release`, `bump` |
| `scope/docs` | `README`, `docs/`, `AGENTS.md`, doc-only |
| `scope/chore` | dependency bump, lint config, CI tweak |
| `needs-PRD` | new feature / multi-module / schema change / breaking API — see `.claude/rules/prd-and-review.md` |

If no scope keyword matches, leave scope unset and flag it for the user.

### 3. Show drafts to user, batched

Print a table of all drafts. Do **not** create yet:

```
## Promote Inbox → Linear (drafts)

| # | Notion Task | Proposed Linear title | Labels | Priority |
|---|---|---|---|---|
| 1 | "Fix smartkargo seconds" | "Fix smartkargo fractional seconds parsing" | scope/connector, Bug | High |
| 2 | "Webhook retries" | "Tenant-scoped webhook retry queue" | scope/server, needs-PRD | Medium |
```

Ask the user which to create. Accept ranges ("1-3, 5") or `all`.

### 4. On approval — create issues + close Inbox rows

For each approved draft:
1. `mcp__claude_ai_Linear__save_issue` with the drafted fields → returns `EBE-{n}`
2. `mcp__claude_ai_Notion__notion-update-page` on the source Inbox row:
   - `Status = Approved`
   - `Link = <Linear issue URL>` (so the Notion row points to the canonical issue)

Print the resulting `EBE-{n}` IDs back to the user.

---

## Scheduling

```
/schedule create "Karrio morning triage" cron="0 8 * * 1-5" prompt="/triage-inbox"
```

The schedule produces the table only. Actual approval happens when the user reads it. Don't schedule `promote` — promotion should be deliberate.

## Anti-Patterns

- ❌ Creating Linear issues without showing the user the draft first
- ❌ Surfacing >5 items in `triage` mode — defeats the purpose
- ❌ Skipping `needs-PRD` detection — items going straight to code is the #1 way scope creeps
- ❌ Working off Inbox items directly without promoting first — splits the source of truth
- ❌ Auto-moving Linear issues to `In Progress` — that's a deliberate user action, marks the start of work
- ❌ Triaging items where `Agent = Admin` or `Research` — wrong lane, leave them alone
- ❌ Writing to the Notion Daily Log — that's the Logger role's job

## Outputs This Skill Does NOT Produce

Single-responsibility — keep these in their lanes:

- Daily Log entries → Logger role
- Decision Log entries → Chief of Staff
- Weekly Reviews → `/retro` flow
- Code changes → spawned specialist workspaces

## Reference

- Linear project: https://linear.app/eben-labs/project/karrio-maintenance-58f70aa22f0e
- Notion Inbox: `collection://e8147767-2ae6-43df-a1f5-9d89c2312640`
- Life OS doc: https://www.notion.so/3547c752109c80dc9938dd1bfc13e9f1
- PRD rule: `.claude/rules/prd-and-review.md`
- Branch convention: `EBE-{n}-{short-slug}` — keeps Linear auto-link working
