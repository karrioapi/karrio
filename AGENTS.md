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
- **Write code as if the same person authored the entire codebase**—consistency is paramount.
- **Favor functional, declarative style**: use `map`, `reduce`, `filter`, and list comprehensions in Python; avoid nested `if` statements and `for` loops when a functional alternative is cleaner.
- **Concise but readable**: code should be terse yet easily maintainable by a human developer—no unnecessary verbosity, but no cryptic one-liners either.
- Python follows PEP 8 with 4-space indentation—format via `black` and keep typing clean with `mypy` (both listed in `requirements.dev.txt`).
- Use snake_case for modules/functions (e.g., `modules/pricing/rate.py`) and PascalCase for classes; mirror existing mapper naming in `modules/connectors`.
- TypeScript and React code are formatted with Prettier (`npm run format`) and linted through `packages/eslint-config-custom`; prefer 2-space indentation and explicit exports.
- **Frontend**: don't reinvent the wheel—follow existing separation of concerns: `lib/` for logic, `types/` for types (use regenerate scripts), reusable components in `ui/`, same concise functional style.

## Testing Guidelines
- Activate the environment with `source bin/activate-env` before invoking tests.
- **Always run tests from the repository root**.
- **Always take inspiration from existing tests**—match the coding style of the project.
- **We do NOT use pytest anywhere in the stack**:
  - Carrier integrations: native Python `unittest`
  - Server/Django: Django tests via `karrio` (manage.py wrapper)
- **Carrier integration tests**: follow the style in `./bin/run-sdk-tests`—run from root:
  ```bash
  ./bin/run-sdk-tests  # runs all SDK and connector tests
  python -m unittest discover -v -f modules/connectors/<carrier>/tests  # single carrier
  ```
- **Server/Django module tests**: follow the style in `./bin/run-server-tests`—run from root:
  ```bash
  ./bin/run-server-tests  # runs all server tests
  karrio test --failfast karrio.server.<module>.tests  # single module
  ```
- Carrier adapters must stay on Python's `unittest` with canonical files like `test_rate.py` and classes shaped as `Test<Carrier><Feature>`.
- Follow carrier testing templates and style in `CARRIER_INTEGRATION_GUIDE.md`.

### Test Writing Style
- **Avoid multiple single-field assertions**—prefer comprehensive comparisons.
- **Use `assertNoErrors` utility** where it makes sense to validate clean responses.
- **Single `assertDictEqual` or `assertListEqual`** with full API response data comparison:
  - Use `mock.ANY` for dynamic fields like `id`, `dates`, `timestamps`.
- **Carrier tests**: follow the same principles using templates in `CARRIER_INTEGRATION_GUIDE.md`.

## Commit & Pull Request Guidelines
- Keep commits focused and follow the short `type: summary` style already used (`fix:`, `feat:`, `chore:`); reference issues with `refs #123` or `fixes #123`.
- Rebase on `main`, rerun lint/test commands, and attach screenshots or CLI transcripts whenever behaviour changes.
- Fill out the PR template, link discussions, enable "Allow edits from maintainers," and list the verification steps reviewers can replay.

## Configuration Tips
- Workspace-specific `.env` files drive local overrides; duplicate provided templates and never commit secrets.
- Use `./bin/create-new-env` when you need a fresh sample configuration, and load additional variables through Docker compose overrides or CI secrets to keep builds reproducible.

## Carrier Integration Reference

- **Always consult `CARRIER_INTEGRATION_GUIDE.md`** when working with carrier integrations—it contains the canonical patterns, file structures, and testing requirements for all connector work.
