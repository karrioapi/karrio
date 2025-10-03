# Repository Guidelines

## Project Structure & Module Organization
- Runtime apps live under `apps/`: `apps/api` hosts the Django service, `apps/dashboard` and `apps/web` power the Next.js UIs, and `apps/www` serves public marketing pages.
- Shared Python code is grouped in `modules/` (core logic, connectors, pricing, etc.), while shared TypeScript utilities live in `packages/`; carrier extensions live in `plugins/` and community-maintained variants sit in `community/`.
- Automation scripts live in `bin/`, and container workflows use the manifests in `docker/` alongside `docker-compose.yml`.

## Build, Test, and Development Commands
- Bootstrap once with `./bin/setup-dev-env` to create the Python virtualenv and install common tooling.
- Run `./bin/start-dev` to launch the API (port 5002) and dashboard (port 3002); `npm run dev -w @karrio/dashboard` targets the dashboard alone, and `docker compose up` inside `docker/` brings up the full stack.
- Front-end builds flow through Turbo: `npm run build` executes `turbo run build`, and `npm run lint` fans out ESLint across all workspaces.

## Coding Style & Naming Conventions
- Python follows PEP 8 with 4-space indentation—format via `black` and keep typing clean with `mypy` (both listed in `requirements.dev.txt`).
- Use snake_case for modules/functions (e.g., `modules/pricing/rate.py`) and PascalCase for classes; mirror existing mapper naming in `modules/connectors`.
- TypeScript and React code are formatted with Prettier (`npm run format`) and linted through `packages/eslint-config-custom`; prefer 2-space indentation and explicit exports.

## Testing Guidelines
- Activate the environment with `source bin/activate-env` before invoking tests.
- Run `./bin/run-server-tests` for the API suites; carrier adapters must stay on Python's `unittest` with canonical files like `test_rate.py` and classes shaped as `Test<Carrier><Feature>`.
- Validate connectors via `python -m unittest discover -v -f modules/connectors/<carrier>/tests`, and guard SDK changes with `./bin/run-sdk-tests`; include the debug prints and tuple assertions mandated in `CARRIER_INTEGRATION_GUIDE.md`.

## Commit & Pull Request Guidelines
- Keep commits focused and follow the short `type: summary` style already used (`fix:`, `feat:`, `chore:`); reference issues with `refs #123` or `fixes #123`.
- Rebase on `main`, rerun lint/test commands, and attach screenshots or CLI transcripts whenever behaviour changes.
- Fill out the PR template, link discussions, enable "Allow edits from maintainers," and list the verification steps reviewers can replay.

## Configuration Tips
- Workspace-specific `.env` files drive local overrides; duplicate provided templates and never commit secrets.
- Use `./bin/create-new-env` when you need a fresh sample configuration, and load additional variables through Docker compose overrides or CI secrets to keep builds reproducible.
