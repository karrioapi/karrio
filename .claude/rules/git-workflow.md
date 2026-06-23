# Git & Commit Guidelines

## ⛔ `main` is protected — never write to it without explicit permission

NEVER merge, push, force-push, revert, or otherwise modify the `main` (default)
branch — directly or via `gh pr merge` — without the user's **explicit,
per-action** go-ahead. This includes merging community/contributor PRs: their
base must be the active release branch, not `main`.

- All integration happens on the release branch (e.g. `patch/YYYY.M.PATCH`) or a
  feature branch. `main` only advances when the user explicitly says to land it.
- "Merge this PR" / "approve this PR" defaults to the **release branch**, not
  `main`. If `main` ever seems required, stop and ask first.
- Branch-protection settings are off-limits unless the user explicitly asks you
  to change them, and then only with an exact snapshot-and-restore.
- A blanket approval of one action is not standing permission for the next.

## Commit Format
- `type: summary` (e.g., `fix:`, `feat:`, `chore:`, `refactor:`, `docs:`, `test:`)
- `type(scope): summary` for scoped changes (e.g., `fix(smartkargo): ...`)
- Scope = carrier name or module (`dashboard`, `mcp`, `tracing`, `graph`, etc.)
- Lowercase, imperative mood, concise
- Reference issues: `refs #123` or `fixes #123`
- Release commits: `release: YYYY.M.PATCH`
- Keep commits focused and atomic

## Rules
- Never write to `main` without explicit per-action permission (see top of file)
- Never commit without explicit user permission
- Never add AI co-author lines (e.g., `Co-Authored-By: Claude ...`)
- Never add "Generated with Claude Code" or similar AI footers
- Run lint/test before pushing
- Rebase on `main` before PR

## PR Format

### Title
Same as commit format: `type(scope): description`

### Body Structure

**Feature PRs:**
```
## Summary
<1-3 sentences>

## Changes
<bullet list of changes, optionally with file-level detail>

## Why
<motivation>

## Verification
<test evidence or build output>
```

**Fix PRs:**
```
## Bug
<what's broken>

## Root Cause
<why it's broken, with code snippet>

## Fix
<what was changed>

## Tests
<verification>
```

**Release PRs:**
```
## Changes

### Feat
- feat(scope): description

### Fix
- fix(scope): description

### Docs
- docs(scope): description
```

### PR Conventions
- Group changes by type: `### Feat`, `### Fix`, `### Docs`, `### Test`, `### Chore`
- Use tables for file-level change summaries and audit matrices
- Include test/build evidence in verification section
- No AI-generated boilerplate footers

## Submodules
Three submodules exist:
- `ee/insiders` → Enterprise features (private)
- `ee/platform` → Platform features (private)
- `community` → Community plugins (public)

Before releases, ensure submodules are merged to main:
```bash
git submodule status
cd ee/insiders && git checkout main && git pull && cd ../..
```

## CHANGELOG.md
- Categorize: Features, Fixes, Chores, Breaking Changes
- Add breaking change warnings at the top of release sections
- Review commits with `git log <last-tag>..HEAD --oneline`
