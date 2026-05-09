# Triage Inbox Skill

Pull pending items from the Notion **Agent Inbox** plus the karrio GitHub backlog, rank them, tag scope, and produce a ranked work list for the day. Approval-gated — never auto-acts on items.

## When to Use

- Start of a karrio working day (morning triage)
- Before opening a new Conductor workspace ("what should I pick up?")
- Whenever the Inbox grows beyond ~10 pending items

## Inputs

| Source | Tool | Filter |
|---|---|---|
| Notion Agent Inbox | `mcp__claude_ai_Notion__notion-fetch` on `collection://e8147767-2ae6-43df-a1f5-9d89c2312640` | `Status = Pending` and (`Agent = Eng` or `Agent` is empty) |
| GitHub issues | `gh issue list --repo karrioapi/karrio --state open --limit 30` | recent open issues |
| In-repo TODOs (optional) | `Grep "TODO\|FIXME"` | only when explicitly asked |

The Inbox schema:

| Field | Values |
|---|---|
| `Task` | title (required) |
| `Status` | `Pending` / `Approved` / `Done` / `Rejected` |
| `Risk Level` | `Low` / `Medium` / `High` |
| `Suggested Action` | free text |
| `Link` | URL (often a GH issue / PR / Notion doc) |
| `Agent` | `Chief` / `Logger` / `Eng` / `Research` / `Admin` |

## Process

### 1. Pull pending items

```
mcp__claude_ai_Notion__notion-search with
  query: "Pending"
  data_source_url: "collection://e8147767-2ae6-43df-a1f5-9d89c2312640"
```

Then `gh issue list --repo karrioapi/karrio --state open --limit 30 --json number,title,labels,updatedAt`.

### 2. Tag each item by scope

Apply scope tags based on Task / Link content:

| Tag | Trigger keywords |
|---|---|
| `[connector]` | carrier name (UPS, FedEx, SmartKargo, ...), `mapper`, `proxy`, `provider`, `rate`, `tracking`, `shipment` |
| `[server]` | `Django`, `migration`, `model`, `serializer`, `viewset`, `huey`, `graphql` |
| `[frontend]` | `dashboard`, `next`, `react`, `apps/dashboard`, `packages/ui` |
| `[release]` | `version`, `changelog`, `release`, `bump` |
| `[bug]` | `bug`, `error`, `broken`, `regression`, `fix` |
| `[PRD-needed]` | new feature, multi-module, schema change, breaking API — see `.claude/rules/prd-and-review.md` for the rule |
| `[docs]` | `README`, `docs/`, `AGENTS.md`, doc-only |
| `[chore]` | dependency bump, lint config, CI tweak |

Multiple tags allowed. Items with `[PRD-needed]` cannot be `Approved` until a PRD exists in `PRDs/`.

### 3. Rank

Sort by:
1. `Risk Level = High` first (these are usually outages or release blockers)
2. Items linked to an open GitHub issue with `bug` label
3. Smallest scope first (single `[connector]` before cross-module work)
4. Freshness (newer `createdTime` wins ties)

Cap output at **5 items**. Your Life OS rule is "max 3 priorities per week" — surface the top 5, the user picks.

### 4. Suggest workspace + role

For each surfaced item, recommend:

| Tag combo | Suggested skill / role |
|---|---|
| `[connector]` | `carrier-integration` skill, fresh Conductor workspace named `<carrier>-<short-task>` |
| `[server]` + `[bug]` | `debugging` skill, current workspace OK |
| `[server]` + `[PRD-needed]` | `create-prd` skill first, then fresh workspace |
| `[frontend]` | fresh workspace, no skill yet (gap) |
| `[release]` | `release` skill, dedicated release workspace |
| `[bug]` no clear scope | gstack `/investigate` |

### 5. Output

Print a markdown table to chat (do **not** write to Notion until the user approves):

```
## Triage — <date>

| # | Risk | Tags | Task | Suggested action | Workspace |
|---|---|---|---|---|---|
| 1 | High | [connector] [bug] | Fix smartkargo fractional seconds | `debugging` skill in cancun | (current) |
| 2 | Med | [server] [PRD-needed] | Tenant-scoped webhook retries | Write PRD first | new: webhook-retries |
| ... |
```

Below the table, list:
- **Skipped:** items that didn't make the top 5 with one-line reason each
- **Inbox health:** count by Status, count by Agent — flag if Pending > 20

### 6. Approval gate (per Life OS rules)

Wait for the user to pick items. Do **not**:
- Mark Inbox items `Approved` automatically
- Open GitHub issues
- Spawn Conductor workspaces

Once the user approves item N:
- `mcp__claude_ai_Notion__notion-update-page` — set `Status = Approved` on that Inbox row
- If they request a workspace, give them the exact Conductor command to run (don't run it yourself)

## Scheduling

To run this every weekday morning:

```
/schedule create "Karrio morning triage" cron="0 8 * * 1-5" prompt="/triage-inbox"
```

The schedule should produce the table only — actual approval happens when the user reads it.

## Anti-Patterns

- ❌ Auto-marking items `Done` based on commit messages — Logger agent's job, not Eng's
- ❌ Triaging items where `Agent = Admin` or `Research` — wrong lane
- ❌ Surfacing >5 items — defeats the purpose, your rule is max 3 priorities
- ❌ Writing to the Daily Log database from this skill — that's the Logger's role
- ❌ Skipping PRD detection — `[PRD-needed]` items going straight to code is the #1 way scope creeps

## Outputs This Skill Does NOT Produce

To stay in lane (single-responsibility):

- Daily Log entries → Logger agent
- Decision Log entries → Chief of Staff
- Weekly Reviews → separate `/retro` flow
- Code changes → spawned specialist workspaces

## Reference

- Inbox schema: `collection://e8147767-2ae6-43df-a1f5-9d89c2312640`
- Life OS doc: https://www.notion.so/3547c752109c80dc9938dd1bfc13e9f1
- PRD rule: `.claude/rules/prd-and-review.md`
- Conductor workspace conventions: one workspace = one task
