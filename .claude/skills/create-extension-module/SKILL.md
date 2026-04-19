# Skill: Create Extension Module

Scaffold a new karrio extension module that hooks into core without modifying core code. Karrio is modular by design — `modules/core`, `modules/graph`, `modules/admin` form the server core, `modules/connectors/*` are carrier plugins, and everything else (`modules/orders`, `modules/data`, `modules/documents`, `modules/events`, `modules/pricing`, `modules/manager`, …) is an auto-discovered extension module following the pattern below.

## When to Use

- New domain logic (a new resource, workflow, or integration)
- Extending the GraphQL schema with new types / mutations
- Adding REST endpoints for new resources
- Registering signal handlers, hook functions, or Huey tasks at startup

**Do NOT use this pattern for carrier connectors** — they live in `modules/connectors/*` and are scaffolded via `./bin/cli sdk add-extension`. See `.claude/skills/carrier-integration/SKILL.md` and `.claude/rules/carrier-integration.md`.

## Prerequisites

Read these first:

- `.claude/rules/extension-patterns.md` — namespace-package caveats, dependency-direction rule, hook points table
- `.claude/skills/django-rest-api/SKILL.md` — REST view / router / serializer conventions
- `.claude/skills/django-graphql/SKILL.md` — Strawberry GraphQL conventions

Study these existing modules — they are the canonical examples, use them as templates:

- `modules/orders/karrio/server/orders/` — REST + GraphQL + signals (the most complete extension module reference)
- `modules/documents/karrio/server/documents/` — REST + Huey tasks for document generation
- `modules/events/karrio/server/events/` — webhook delivery + Huey task registration
- `modules/data/karrio/server/data/` — import / export module with REST views
- `modules/pricing/karrio/server/pricing/` — admin-scoped pricing with markups and fees

## Steps

### 1. Create the module directory

```bash
mkdir -p modules/<name>/karrio/server/<name>
mkdir -p modules/<name>/karrio/server/settings
```

Optional sub-packages (create only what you need):

```bash
mkdir -p modules/<name>/karrio/server/<name>/serializers
mkdir -p modules/<name>/karrio/server/<name>/tests
mkdir -p modules/<name>/karrio/server/<name>/migrations
mkdir -p modules/<name>/karrio/server/graph/schemas/<name>    # only if adding GraphQL
mkdir -p modules/<name>/karrio/server/admin/schemas/<name>    # only if adding admin GraphQL
```

**Namespace-package rule (critical):** the only `__init__.py` files you create are inside the **leaf** directories unique to your module — i.e. `karrio/server/<name>/__init__.py`, `karrio/server/<name>/tests/__init__.py`, `karrio/server/graph/schemas/<name>/__init__.py`, etc. Never create `__init__.py` at `karrio/`, `karrio/server/`, `karrio/server/graph/`, `karrio/server/graph/schemas/`, `karrio/server/admin/`, or `karrio/server/admin/schemas/` — those paths are owned by core modules and must stay as implicit namespace packages. Adding an `__init__.py` there shadows the core package and silently breaks `pkgutil.iter_modules()` discovery. See `.claude/rules/extension-patterns.md` for details.

Verify by looking at `modules/orders/karrio/` — there is no `__init__.py` at `karrio/` or `karrio/server/`, only inside `karrio/server/orders/` and its sub-packages.

### 2. Create the AppConfig

```python
# modules/<name>/karrio/server/<name>/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class <Name>Config(AppConfig):
    name = "karrio.server.<name>"
    verbose_name = _("<Name>")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from karrio.server.core import utils
        from karrio.server.<name> import signals  # only if you have signals

        @utils.skip_on_commands()
        def _init():
            signals.register_signals()

        _init()
```

Karrio conventions (see `modules/orders/karrio/server/orders/apps.py`):

- Wrap registration in `@utils.skip_on_commands()` — this prevents signal / hook registration from running during `migrate`, `collectstatic`, `makemigrations`, etc. Without it you get noisy side-effects (or outright failures) when running management commands on a fresh database.
- Wrap `verbose_name` in `gettext_lazy` so the admin UI can be translated.
- Import signals lazily inside `ready()`, never at module top-level — Django is not fully initialized yet when `apps.py` is imported.

### 3. Register signal / hook handlers

```python
# modules/<name>/karrio/server/<name>/signals.py
import karrio.server.<name>.models as models
from django.db.models import signals
from karrio.server.core import utils
from karrio.server.core.logging import logger


def register_signals():
    signals.post_save.connect(_on_save, sender=models.Widget)
    signals.post_delete.connect(_on_delete, sender=models.Widget)
    logger.info("Signal registration complete", module="karrio.<name>")


@utils.disable_for_loaddata
def _on_save(sender, instance, created, **kwargs):
    ...


@utils.disable_for_loaddata
def _on_delete(sender, instance, **kwargs):
    ...
```

`@utils.disable_for_loaddata` prevents signals from firing during fixture loading (test setup, `loaddata`). See the orders module's `signals.py` for a full-featured example that touches related models.

To hook into a core serializer's validation pipeline, append to `pre_process_functions`:

```python
# inside register_signals() or a separate hooks.py
from karrio.server.manager.serializers import ShipmentSerializer
from karrio.server.<name> import validators

ShipmentSerializer.pre_process_functions.append(validators.validate_widget_link)
```

### 4. Add settings auto-discovery

```python
# modules/<name>/karrio/server/settings/<name>.py
# ruff: noqa: F403, F405, I001
from karrio.server.settings.base import *  # noqa

INSTALLED_APPS += ["karrio.server.<name>"]
KARRIO_URLS += ["karrio.server.<name>.urls"]  # only if the module has REST endpoints
```

`apps/api/karrio/server/settings/__init__.py` iterates its known module names with `importlib.util.find_spec(...)` and imports `karrio.server.settings.<name>` when the module is installed. Your settings file must follow that exact path — `modules/<name>/karrio/server/settings/<name>.py` — for discovery to work.

If your extension is a completely new module not already listed in `apps/api/karrio/server/settings/__init__.py`, add a matching `find_spec` guard there as a separate PR (this edits core and needs review). Karrio's current guards cover `graph`, `orders`, `data`, `admin`, `huey`, `servicebus`, `main` — check the file when adding a new one.

### 5. Add REST endpoints (if needed)

Follow `.claude/skills/django-rest-api/SKILL.md`. At minimum:

- `modules/<name>/karrio/server/<name>/router.py` — `router = DefaultRouter(trailing_slash=False)`
- `modules/<name>/karrio/server/<name>/urls.py` — `app_name = "karrio.server.<name>"`, mount `router.urls` at `v1/`
- `modules/<name>/karrio/server/<name>/views.py` — views extending `karrio.server.core.views.api.GenericAPIView` / `APIView`, with a unique 5-char `ENDPOINT_ID`, `@openapi.extend_schema(...)` annotations, and self-registration via `router.urls.append(path(...))`

### 6. Add GraphQL schemas (if needed)

Follow `.claude/skills/django-graphql/SKILL.md`. Four files under a schemas sub-package:

```
modules/<name>/karrio/server/graph/schemas/<name>/        # tenant-scoped
├── __init__.py    # Query + Mutation classes + extra_types = [] (thin interface)
├── types.py       # @strawberry.type with resolve / resolve_list static methods
├── inputs.py      # @strawberry.input filters + mutation inputs
└── mutations.py   # @strawberry.type mutations with mutate() static methods
```

For admin-scoped (system) schemas use `modules/<name>/karrio/server/admin/schemas/<name>/` instead. `modules/graph/karrio/server/graph/schema.py` auto-discovers both via `pkgutil.iter_modules()` — no registration required.

`extra_types: list = []` is required in every schema `__init__.py` even if empty — `schema.py` reads it unconditionally.

### 7. Add `pyproject.toml`

Match the orders module's structure (`modules/orders/pyproject.toml`):

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "karrio_server_<name>"
version = "2026.1.29"  # keep in sync with apps/api/karrio/server/VERSION
description = "Multi-carrier shipping API <name> module"
readme = "README.md"
requires-python = ">=3.11"
license = "LGPL-3.0"
authors = [
    {name = "karrio", email = "hello@karrio.io"}
]
classifiers = [
    "Programming Language :: Python :: 3",
]
dependencies = [
    "karrio_server_core",
    "karrio_server_graph",     # if adding GraphQL
    "karrio_server_manager",   # if importing from manager models
]

[project.urls]
Homepage = "https://github.com/karrioapi/karrio"

[tool.setuptools]
zip-safe = false
include-package-data = true

[tool.setuptools.package-dir]
"" = "."

[tool.setuptools.packages.find]
exclude = ["tests.*", "tests"]
namespaces = true
```

`namespaces = true` is mandatory — karrio uses PEP 420 namespace packages across modules.

### 8. Add tests

Tests live in a `tests/` **directory** (not a single `tests.py`):

```
modules/<name>/karrio/server/<name>/tests/
├── __init__.py         # re-exports test classes for karrio test discovery
├── base.py             # optional: shared fixture class extending APITestCase / GraphTestCase
├── test_<resource>.py  # REST tests
└── test_<feature>.py   # GraphQL / signal tests
```

Use the right base class:

- REST: `karrio.server.core.tests.APITestCase` (see `modules/core/karrio/server/core/tests/base.py`)
- GraphQL: `karrio.server.graph.tests.GraphTestCase` (see `modules/graph/karrio/server/graph/tests/base.py`)

Both provide `setUpTestData` with a superuser, API token, and seeded carrier connections.

```python
# modules/<name>/karrio/server/<name>/tests/test_widgets.py
import json
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase


class TestWidgets(APITestCase):
    def test_create_widget(self):
        url = reverse("karrio.server.<name>:widget-list")
        response = self.client.post(url, {"name": "Hello"})
        # print(response.data)  # DEBUG — remove when passing
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### 9. Register in build / dev / CI

All three files must be updated — missing any of them means the module is silently skipped:

| File | Purpose |
| --- | --- |
| `requirements.build.txt` | Installs the module in prod Docker images. Without this, the module never reaches staging / production. |
| `requirements.server.dev.txt` | Installs the module in local dev environments. Without this, `./bin/run-server-tests` skips it locally. |
| `bin/run-server-tests` | Adds `karrio.server.<name>.tests` to the Django test-runner invocation. Without this, tests pass locally but never run in CI. |

Add a line like `-e ./modules/<name>` to both requirements files, and add `karrio.server.<name>.tests \` to the `$KARRIO_TEST --failfast` invocation in `bin/run-server-tests`.

### 10. Install in development

```bash
source bin/activate-env
pip install -e modules/<name>
./bin/run-server-tests            # full server suite
karrio test --failfast karrio.server.<name>.tests   # just your module
```

## Verification

```bash
# 1. Module imports
python -c "import karrio.server.<name>; print('OK')"

# 2. Settings auto-discovery picked it up (INSTALLED_APPS, KARRIO_URLS)
python -c "from django.conf import settings; print('karrio.server.<name>' in settings.INSTALLED_APPS)"

# 3. Django migrations generate
karrio makemigrations <name>
karrio migrate <name>

# 4. GraphQL schema registration (if added)
python -c "from karrio.server.graph.schema import schema; print(schema)"

# 5. REST endpoints reachable (if added)
./bin/start
curl -H "Authorization: Token <tkn>" http://localhost:5002/api/v1/widgets
```

If `pkgutil.iter_modules()` silently skips your GraphQL schema, the usual culprits are:

1. A stray `__init__.py` at `modules/<name>/karrio/server/graph/` or `.../schemas/` — delete it.
2. A circular import between `types.py`, `mutations.py`, and `utils.py` — `schema.py` catches the `ImportError` and moves on (check `karrio.server.core.logging` output).
3. The module isn't installed — `pip install -e modules/<name>` and confirm in `pip list`.
4. `requirements.build.txt` missing the `-e ./modules/<name>` line — schema discovery works locally but staging / prod silently omit the module.
