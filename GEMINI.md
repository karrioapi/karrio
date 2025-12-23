# Gemini Code Instructions

This file provides Gemini-specific context for the Karrio repository.

## Primary Guidelines

**All coding preferences, project context, and conventions are documented in [AGENTS.md](./AGENTS.md).**

Please read `AGENTS.md` thoroughly before making any changes. It contains:

- Project structure and architecture (Backend/Frontend)
- Build, test, and development commands
- Coding style and naming conventions
- Testing guidelines (including Django test writing patterns)
- Commit and PR guidelines
- Carrier integration reference
- Before-making-changes checklist

## Gemini-Specific Reminders

- When writing Django tests, always add `print(response)` before assertions for debugging
- Favor functional, declarative style over imperative loops
- Write code as if the same person authored the entire codebase
- Read referenced files first, create a plan, then implement step by step

---

**Single source of truth**: [AGENTS.md](./AGENTS.md)
