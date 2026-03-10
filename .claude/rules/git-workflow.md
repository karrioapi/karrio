# Git & Commit Guidelines

## Commit Format
- `type: summary` (e.g., `fix:`, `feat:`, `chore:`, `refactor:`, `docs:`, `test:`)
- `type(scope): summary` for scoped changes (e.g., `fix(smartkargo): ...`)
- Scope = carrier name or module (`dashboard`, `mcp`, `tracing`, `graph`, etc.)
- Lowercase, imperative mood, concise
- Reference issues: `refs #123` or `fixes #123`
- Release commits: `release: YYYY.M.PATCH`
- Keep commits focused and atomic

## Rules
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
