# Skill: Create Extension Module

Scaffold a new karrio extension module that hooks into core without modifying the core modules.

## When to Use

- Creating new domain logic (e.g., a new resource, workflow, or integration)
- Extending GraphQL schema with new types/mutations
- Adding REST endpoints for new resources
- Registering signal handlers or pre-processing hooks at startup

## Prerequisites

- Read `.claude/rules/extension-patterns.md` first.
- Study existing karrio extension modules for reference:
  - `modules/orders/karrio/server/orders/` — REST + GraphQL + signals
  - `modules/events/karrio/server/events/` — webhooks, Huey task registration
  - `modules/documents/karrio/server/documents/` — auto-discovered REST URLs
  - `modules/graph/karrio/server/graph/schemas/base/` — canonical GraphQL module layout

## Steps

### 1. Create Module Directory Structure

```bash
mkdir -p modules/<name>/karrio/server/<name>
mkdir -p modules/<name>/karrio/server/settings
```

Create `__init__.py` files at each level with namespace package declarations:

```python
# modules/<name>/karrio/__init__.py
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

# modules/<name>/karrio/server/__init__.py
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
```

### 2. Create AppConfig

```python
# modules/<name>/karrio/server/<name>/apps.py
from django.apps import AppConfig

class <Name>Config(AppConfig):
    name = "karrio.server.<name>"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        # Register hooks here
        from karrio.server.<name> import hooks
        hooks.register()
```

### 3. Create Settings Auto-Discovery

```python
# modules/<name>/karrio/server/settings/<name>.py
from karrio.server.settings.base import *  # noqa

INSTALLED_APPS += ["karrio.server.<name>"]

# If module has REST endpoints:
# KARRIO_URLS += ["karrio.server.<name>.urls"]
```

### 4. Add Hook Registration (if extending core behavior)

```python
# modules/<name>/karrio/server/<name>/hooks.py
def register():
    from karrio.server.manager.serializers import ShipmentSerializer
    # Append validation/processing hooks
    ShipmentSerializer.pre_process_functions.append(your_validator)
```

### 5. Add GraphQL Schema (if needed)

For tenant-scoped (base graph):
```
modules/<name>/karrio/server/graph/schemas/<name>/
├── __init__.py    # Query & Mutation classes
├── types.py
├── mutations.py
└── inputs.py
```

For admin-scoped:
```
modules/<name>/karrio/server/admin/schemas/<name>/
├── __init__.py
├── types.py
├── mutations.py
└── inputs.py
```

Ensure namespace `__init__.py`:
```python
# modules/<name>/karrio/server/graph/schemas/__init__.py
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
```

### 6. Add pyproject.toml

```toml
[project]
name = "karrio.server.<name>"
version = "2026.1"
dependencies = ["karrio.server"]

[tool.setuptools.packages.find]
where = ["."]
```

### 7. Add Tests

```python
# modules/<name>/karrio/server/<name>/tests.py
from karrio.server.graph.tests import GraphTestCase

class Test<Name>Feature(GraphTestCase):
    fixtures = ["fixtures"]

    def test_query(self):
        response = self.query(QUERY, operation_name="...")
        self.assertResponseNoErrors(response)
```

### 8. Register in Build Requirements

Add the module to `requirements.build.txt`:

```
-e ./modules/<name>
```

Without this, the module will NOT be installed in Docker images and schema discovery will silently skip it on staging/production.

Also add `karrio.server.<name>.tests` to `bin/run-server-tests` so the test suite runs in CI.

### 9. Install in Development

```bash
pip install -e modules/<name>
```

## Verification

```bash
# Check module is discovered
python -c "import karrio.server.<name>; print('OK')"

# Run module tests
karrio test --failfast karrio.server.<name>.tests
```
