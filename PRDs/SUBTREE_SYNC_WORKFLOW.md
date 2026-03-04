# Subtree Sync Workflow — JTL Shipping Platform ↔ Karrio Upstream

<!-- ARCHITECTURE: System design PRD for bi-directional subtree synchronization -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-03-04 |
| Status | Active |
| Owner | Daniel Kobina |
| Type | Architecture / Operations |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Repository Topology](#repository-topology)
3. [Sync Direction: Upstream → Shipping Platform (Pull)](#sync-direction-upstream--shipping-platform-pull)
4. [Sync Direction: Shipping Platform → Upstream (Push)](#sync-direction-shipping-platform--upstream-push)
5. [Conflict Resolution](#conflict-resolution)
6. [Safety Rules & Pre-flight Checks](#safety-rules--pre-flight-checks)
7. [Agent Playbook (Step-by-Step)](#agent-playbook-step-by-step)
8. [Failure Modes & Recovery](#failure-modes--recovery)
9. [Appendices](#appendices)

---

## Executive Summary

The JTL Shipping Platform (`jtlshipping/shipping-platform`) embeds two upstream Karrio repositories as **git subtrees**:

| Subtree prefix | Upstream repository | Upstream clone path |
|---|---|---|
| `karrio/` | `karrioapi/karrio` | `/Users/danielkobina/Workspace/karrio/karrio` |
| `karrio-insiders/` | `karrioapi/karrio-insiders` | `/Users/danielkobina/Workspace/karrio/karrio/ee/insiders` (submodule) |

Changes flow **bi-directionally**: upstream fixes are pulled into the shipping platform, and shipping-platform improvements are exported back upstream. This PRD codifies the exact process, safety checks, and conflict resolution strategy so that any agent (human or AI) can execute it safely.

### Key Architecture Decisions

1. **Git subtrees, not submodules**: The shipping platform uses `git subtree` (squash merge strategy) for `karrio/` and `karrio-insiders/`. This means each sync creates a squash commit referencing the upstream commit range.
2. **Patch-based export**: Changes from the shipping platform are exported as unified diffs (with prefix stripped) and applied to the upstream clones — never pushed directly via `git subtree push`.
3. **Upstream-first conflict resolution**: When both sides have the same change (common after a round-trip export→merge→pull), take the upstream version (`--theirs`) since it contains the canonical merged result.
4. **karrio-insiders is a submodule inside karrio**: The upstream `karrioapi/karrio` repo has `ee/insiders` as a git submodule pointing to `karrioapi/karrio-insiders`. When applying insiders patches, target the submodule directly (its `.git` is a file, not a directory).

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Bi-directional code sync between shipping-platform and upstream | Repository merge / monorepo migration (see `REPOSITORY_MERGE_AND_LICENSE_GATING.md`) |
| Conflict resolution for subtree pull/push | License gating or enterprise feature management |
| Agent-executable playbook with safety checks | CI/CD pipeline changes |
| Generated asset handling (static elements chunks) | Carrier integration development |

---

## Repository Topology

```
┌──────────────────────────────────────────────────────┐
│           jtlshipping/shipping-platform              │
│                                                      │
│  ┌──────────────┐      ┌───────────────────┐         │
│  │   karrio/    │      │ karrio-insiders/  │         │
│  │  (subtree)   │      │    (subtree)      │         │
│  └──────┬───────┘      └────────┬──────────┘         │
│         │                       │                    │
└─────────┼───────────────────────┼────────────────────┘
          │ pull/push             │ pull/push
          ▼                       ▼
┌─────────────────┐    ┌──────────────────────────┐
│  karrioapi/     │    │  karrioapi/              │
│  karrio         │    │  karrio-insiders         │
│  (upstream)     │    │  (upstream)              │
│                 │    │                          │
│  ee/insiders ───┼───>│  (submodule reference)   │
│  (submodule)    │    │                          │
└─────────────────┘    └──────────────────────────┘
```

### Git Remotes (in shipping-platform)

| Remote name | URL | Purpose |
|---|---|---|
| `origin` | `git@github.com:jtlshipping/shipping-platform.git` | Main shipping-platform repo |
| `karrio` | `git@github.com:karrioapi/karrio.git` | Upstream karrio (for subtree pull) |
| `karrio-insiders` | `git@github.com:karrioapi/karrio-insiders.git` | Upstream karrio-insiders (for subtree pull) |

### Local Upstream Clones (for patch application)

| Upstream | Local clone path | Notes |
|---|---|---|
| `karrioapi/karrio` | `/Users/danielkobina/Workspace/karrio/karrio` | Standard git repo |
| `karrioapi/karrio-insiders` | `/Users/danielkobina/Workspace/karrio/karrio/ee/insiders` | **Git submodule** — `.git` is a file, not a directory |

---

## Sync Direction: Upstream → Shipping Platform (Pull)

### When to Pull

- Before exporting local changes upstream (to minimize conflicts)
- When upstream has released a new patch version
- When upstream has merged your previously exported PR

### Script

```bash
# From shipping-platform root
./bin/update-subtrees                     # Pull both subtrees
./bin/update-subtrees --karrio-only       # Pull only karrio
./bin/update-subtrees --karrio-insiders-only  # Pull only karrio-insiders
./bin/update-subtrees --branch <branch>   # Pull from specific branch
./bin/update-subtrees --resolve-theirs    # Auto-resolve conflicts (upstream wins)
```

### What Happens

1. `git fetch <remote>` — fetches latest from upstream
2. `git subtree pull --prefix=<prefix> <remote> <branch> --squash` — pulls and squash-merges
3. Creates a merge commit with message: `Squashed '<prefix>/' changes from <old>..<new>`

---

## Sync Direction: Shipping Platform → Upstream (Push)

### When to Push

- After developing features or fixes in the shipping-platform subtrees
- Before a karrio release that should include shipping-platform changes

### Script

```bash
# From shipping-platform root

# 1. Check sync status (recommended first step)
./bin/export-karrio-patches --check-upstream
./bin/export-karrio-patches --insiders --check-upstream

# 2. Preview changes (stdout)
./bin/export-karrio-patches
./bin/export-karrio-patches --insiders

# 3a. Save to file
./bin/export-karrio-patches -o /tmp/karrio.patch
./bin/export-karrio-patches --insiders -o /tmp/insiders.patch

# 3b. Apply directly to upstream clone
./bin/export-karrio-patches --apply /path/to/karrio-clone
./bin/export-karrio-patches --insiders --apply /path/to/insiders-clone

# Force (skip upstream-ahead check)
./bin/export-karrio-patches --force --apply /path/to/clone

# 3-way merge (handles some conflicts automatically)
./bin/export-karrio-patches --3way --apply /path/to/clone
```

### How the Patch is Generated

1. Finds the last `Squashed '<prefix>/' changes from ...` commit in history
2. Finds the merge commit that integrated that squash
3. Runs `git diff --relative="<prefix>/" <merge-point>..HEAD -- <prefix>/` to get all local changes since last sync
4. Excludes generated files by default: `package-lock.json`, `schemas/graphql*.json`
5. Outputs a clean patch with the subtree prefix stripped (ready to apply to upstream)

### Applying to Upstream (Manual Process When Script Fails)

When the `--apply` flag fails (e.g., because the target is a submodule with a `.git` file), apply manually:

```bash
# 1. Export to file
./bin/export-karrio-patches --force -o /tmp/karrio.patch

# 2. In the upstream clone
cd /path/to/upstream/clone
git checkout main && git pull origin main
git checkout -b sync/shipping-platform-patches-YYYY-MM-DD

# 3. Try clean apply
git apply --check /tmp/karrio.patch

# 4. If clean apply fails, use 3-way merge
git apply --3way /tmp/karrio.patch

# 5. Resolve any remaining conflicts (see Conflict Resolution below)

# 6. Commit, push, create PR
git add -A
git commit -m "fix: sync shipping-platform patches"
git push -u origin sync/shipping-platform-patches-YYYY-MM-DD
gh pr create --title "sync: shipping-platform patches YYYY-MM-DD" --body "..."
```

---

## Conflict Resolution

### Why Conflicts Happen

Conflicts during **pull** (upstream → shipping-platform) typically occur when:
- You exported patches upstream, they were merged, and now you're pulling back — both sides have the same change under different commits
- Upstream made independent changes to the same files you modified locally

Conflicts during **push** (shipping-platform → upstream) typically occur when:
- Upstream diverged significantly since the last subtree sync
- Generated files (static assets, migrations) differ between the two

### Resolution Strategy

#### For Pull Conflicts (after `update-subtrees`)

```bash
# Automatic: take upstream version for all subtree conflicts
./bin/resolve-subtree-conflicts

# Or during update:
./bin/update-subtrees --resolve-theirs

# Manual: resolve specific files
./bin/resolve-subtree-conflicts --karrio      # Only karrio/
./bin/resolve-subtree-conflicts --insiders    # Only karrio-insiders/
./bin/resolve-subtree-conflicts --dry-run     # Preview without changes
./bin/resolve-subtree-conflicts --no-commit   # Resolve but review before committing
```

#### For Push Conflicts (when applying patches to upstream)

Use this decision matrix for each conflicted file:

| File Category | Resolution | Rationale |
|---|---|---|
| **Static assets** (`static/karrio/elements/`) | Take subtree (shipping-platform) version | These are generated build outputs; the subtree has the latest rebuild |
| **Auto-generated files** (`next-env.d.ts`, `package-lock.json`) | Take subtree version | Generated files should match the build environment |
| **Connector settings** (`settings.py`) | Take subtree version | Shipping-platform typically has the latest sensitive field annotations |
| **Upstream-only features** (new methods, new props) | Keep upstream version | Don't lose upstream work that shipping-platform doesn't have yet |
| **Version numbers** (`pyproject.toml` version) | Keep upstream version | Upstream controls release versioning |
| **Migration files** (same migration, different formatting) | Take either (prefer subtree for consistency) | Cosmetic differences only |
| **UI components with extra props/features** | Keep upstream if it has additions the subtree lacks | Prevent feature regression |

### Per-File Resolution Commands

```bash
# In the upstream clone, after `git apply --3way`:

# Take the shipping-platform (subtree) version:
cp "/path/to/shipping-platform/karrio/<file>" "<file>"
git add "<file>"

# Keep the upstream (current) version:
git checkout --ours "<file>"
git add "<file>"

# For static assets (bulk — take subtree version):
for f in $(git diff --name-only --diff-filter=U | grep "static/karrio/elements"); do
  cp "/path/to/shipping-platform/karrio/$f" "$f"
  git add "$f"
done
```

---

## Safety Rules & Pre-flight Checks

### MUST DO Before Any Sync

| # | Check | Command | Why |
|---|---|---|---|
| 1 | Working tree is clean | `git status` (in shipping-platform) | Uncommitted changes can be lost during subtree operations |
| 2 | On correct branch | `git branch --show-current` | Subtree operations modify history |
| 3 | Check upstream sync status | `./bin/export-karrio-patches --check-upstream` | Know how far upstream has diverged |
| 4 | Verify upstream clone is on main | `cd <upstream> && git branch --show-current` | Don't apply patches to a stale branch |
| 5 | Pull latest upstream main | `cd <upstream> && git checkout main && git pull` | Ensure patches apply against latest code |

### NEVER DO

| Rule | Reason |
|---|---|
| Never `git subtree push` directly | Can create messy merge histories; always use patch export |
| Never force-push to upstream `main` | Destructive; always create a PR branch |
| Never skip the `--check-upstream` step | May cause cascade of conflicts on pull-back |
| Never blindly take subtree version for all conflicts | Upstream may have features/fixes the subtree doesn't have |
| Never commit merge conflict markers | Always verify `git diff --name-only --diff-filter=U` returns empty |
| Never apply patches with generated files if upstream generated differently | Exclude generated files or manually reconcile |

### karrio-insiders Submodule Caveat

The `export-karrio-patches --apply` script checks for a `.git` **directory** at the target. Since `ee/insiders` is a submodule, its `.git` is a **file** (pointing to `../../.git/modules/insiders`). The script will fail with:

```
ERR Target is not a git repository: /path/to/ee/insiders
```

**Workaround**: Export to file and apply manually:

```bash
./bin/export-karrio-patches --insiders --force -o /tmp/insiders.patch
cd /path/to/karrio/ee/insiders
git apply --3way /tmp/insiders.patch  # or git apply --check first
```

---

## Agent Playbook (Step-by-Step)

This is the canonical procedure for an AI agent to follow when asked to sync changes.

### Phase 1: Assessment

```
1. cd /Users/danielkobina/Workspace/jtl/shipping-platform
2. git status                             # Ensure clean working tree
3. ./bin/export-karrio-patches --check-upstream
4. ./bin/export-karrio-patches --insiders --check-upstream
5. Record: how many commits ahead is upstream for each subtree?
```

### Phase 2: Decide Direction

| Scenario | Action |
|---|---|
| User says "push changes upstream" | → Phase 3 (Export) |
| User says "pull upstream changes" | → `./bin/update-subtrees` |
| Upstream is ahead AND we have local changes | Ask user: pull first or force-export? |
| No local changes since last sync | Report "already in sync" and stop |

### Phase 3: Export Patches

```
1. ./bin/export-karrio-patches --force -o /tmp/karrio.patch 2>&1
   → Note file count and line count
   → Check if there are any real code changes vs only static assets

2. ./bin/export-karrio-patches --insiders --force -o /tmp/insiders.patch 2>&1
   → If "No local changes found", skip insiders

3. For each non-empty patch, identify changed files:
   grep "^diff --git" /tmp/karrio.patch | grep -v "static/karrio/elements"
```

### Phase 4: Apply to Upstream

For **karrio**:

```bash
cd /Users/danielkobina/Workspace/karrio/karrio
git checkout main && git pull origin main
git checkout -b sync/shipping-platform-patches-$(date +%Y-%m-%d)
git apply --3way /tmp/karrio.patch
```

For **karrio-insiders**:

```bash
cd /Users/danielkobina/Workspace/karrio/karrio/ee/insiders
git checkout main && git pull origin main
git checkout -b sync/shipping-platform-patches-$(date +%Y-%m-%d)
git apply --3way /tmp/insiders.patch
```

### Phase 5: Resolve Conflicts

```
1. git diff --name-only --diff-filter=U   # List conflicted files
2. For each file, apply the decision matrix from "Conflict Resolution" section
3. Verify: git diff --name-only --diff-filter=U  → must be empty
4. Review staged diff: git diff --cached --stat
```

### Phase 6: Commit & Push

```bash
git add -A
git commit -m "fix: sync shipping-platform patches (brief description of changes)"
git push -u origin <branch-name>
```

### Phase 7: Create PR

```bash
gh pr create \
  --title "sync: shipping-platform patches YYYY-MM-DD" \
  --body "## Summary
- [List of meaningful changes, not static assets]

## Conflict Resolution
- [List files where upstream version was kept and why]

## Source
Exported from jtlshipping/shipping-platform main branch."
```

### Phase 8: Post-merge Cleanup (after PR is merged)

```bash
# Back in shipping-platform
cd /Users/danielkobina/Workspace/jtl/shipping-platform
./bin/update-subtrees          # Pull back the merged changes
# Should be clean (no conflicts) if the PR contained exactly the exported changes
```

---

## Failure Modes & Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Patch doesn't apply at all | `error: patch failed` on `git apply --check` | Use `--3way` flag; if still fails, upstream diverged too much — pull upstream into shipping-platform first, then re-export |
| Submodule `.git` file error | `ERR Target is not a git repository` | Export to file and apply manually (see caveat above) |
| 5000+ commits ahead | `Upstream has N commits since last sync!` | This is normal if subtree sync hasn't happened in a while. Use `--force` to export anyway; many changes may already exist upstream |
| Patch includes files that already match upstream | Files appear in patch but `diff` shows identical content | These will fail to apply but `--3way` handles them gracefully |
| Post-merge pull creates conflicts | Both sides have same changes from different commits | `./bin/resolve-subtree-conflicts` (takes upstream version) |
| Accidentally applied to wrong branch | Changes on `main` instead of sync branch | `git stash && git checkout -b <branch> && git stash pop` |
| Large static asset diffs bloating PR | Hundreds of `.js` chunk files | Expected — these are Vite build outputs. They must be included for the elements to work. |

---

## Appendices

### Appendix A: Script Locations

| Script | Path (in shipping-platform) | Purpose |
|---|---|---|
| `update-subtrees` | `bin/update-subtrees` | Pull upstream → shipping-platform |
| `export-karrio-patches` | `bin/export-karrio-patches` | Generate/apply patches shipping-platform → upstream |
| `resolve-subtree-conflicts` | `bin/resolve-subtree-conflicts` | Resolve subtree merge conflicts |

### Appendix B: Commit Message Conventions

| Direction | Format | Example |
|---|---|---|
| Subtree pull | Auto-generated by git | `Squashed 'karrio/' changes from abc..def` |
| Upstream sync PR | `fix: sync shipping-platform patches (...)` | `fix: sync shipping-platform patches (admin scoping, dhl encryption)` |
| Post-merge pull-back | Auto-generated + optional | `Squashed 'karrio/' changes from def..ghi` |

### Appendix C: Excluded Files

The export script excludes these generated files by default:

**karrio subtree:**
- `karrio/package-lock.json`
- `karrio/schemas/graphql-admin.json`
- `karrio/schemas/graphql-ee.json`
- `karrio/schemas/graphql.json`

**karrio-insiders subtree:**
- `karrio-insiders/package-lock.json`

Use `--include-generated` to include them if needed.

### Appendix D: Verifying Sync State

To check if a specific file is already in sync between the subtree and upstream:

```bash
diff \
  /Users/danielkobina/Workspace/jtl/shipping-platform/karrio/<file> \
  /Users/danielkobina/Workspace/karrio/karrio/<file>
# Exit code 0 = identical (already in sync)
```

To bulk-check all modified files:

```bash
for f in $(./bin/export-karrio-patches --force 2>/dev/null | grep "^diff --git" | sed 's|diff --git a/||;s| b/.*||'); do
  if diff -q \
    "/Users/danielkobina/Workspace/jtl/shipping-platform/karrio/$f" \
    "/Users/danielkobina/Workspace/karrio/karrio/$f" > /dev/null 2>&1; then
    echo "IN SYNC: $f"
  else
    echo "DIFFERS: $f"
  fi
done
```
