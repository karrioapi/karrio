# Code Style & Naming Conventions

## General
- Write code as if the same person authored the entire codebase
- Favor functional, declarative style: use `map`, `reduce`, `filter`, list comprehensions
- Concise but readable: no unnecessary verbosity, no cryptic one-liners
- Never reinvent the wheel — always search for existing utilities first

## Python
- PEP 8 with 4-space indentation
- Format: `black`, type check: `mypy`
- snake_case for modules/functions, PascalCase for classes
- Always use `import karrio.lib as lib` — never the legacy `DP`, `SF`, `NF`, `DF`, `XP` utilities
- Import order: stdlib → third-party → karrio core → local/relative

## TypeScript/React
- 2-space indentation, format with Prettier
- PascalCase for components, camelCase for functions/variables
- Functional components only (no class components)
- Import order: React/Next → third-party → @karrio packages → local
- Always import types from `@karrio/types` (never define inline)
- Use existing hooks from `@karrio/hooks/*` (never raw fetch/axios)
- Use existing UI components from `@karrio/ui` (never duplicate patterns)

## Anti-Patterns
- Never use `pytest` — we use `unittest` and Django tests
- Never use raw SQL in Django migrations — use Django operations only
- Never catch bare `Exception` — be specific
- Never use mutable default arguments
- Never add features not explicitly requested
- Never use `any` type in TypeScript
