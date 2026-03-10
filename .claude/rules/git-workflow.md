# Git & Commit Guidelines

## Commit Format
- `type: summary` (e.g., `fix:`, `feat:`, `chore:`, `refactor:`)
- `type(scope): summary` for scoped changes (e.g., `fix(smartkargo): ...`)
- Reference issues: `refs #123` or `fixes #123`
- Keep commits focused and atomic

## Rules
- Never commit without explicit user permission
- Never add AI co-author lines (e.g., `Co-Authored-By: Claude ...`)
- Run lint/test before pushing
- Rebase on `main` before PR

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
