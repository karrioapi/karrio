"""Django system checks for rolling-deploy schema safety.

These checks run via ``manage.py check`` (and implicitly before every
``manage.py test`` run) to catch schema-shape bugs that unit tests can't:
when unit tests run, code and migrations are always in lockstep, so an INSERT
that omits a column is never exercised. In production during a rolling deploy
the older pods may still be running pre-migration code that doesn't know about
a newly added column — if the column is ``NOT NULL`` with only a Python-level
``default`` (no DB-level ``DEFAULT``), those INSERTs trip the constraint.

``karrio.E001`` flags fields that were added via ``AddField`` (i.e. to an
existing table) that are NOT NULL, carry a Python ``default``, but have no
``db_default``. Adding ``db_default=<value>`` makes the DB column carry an
actual ``DEFAULT`` clause, closing the rolling-deploy gap.
"""

from django.apps import apps
from django.core.checks import Error, Tags, Warning, register
from django.core.exceptions import FieldDoesNotExist
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.operations.fields import AddField
from django.db.models import NOT_PROVIDED

# Apps we don't own — we can't add ``db_default`` to third-party model fields
# without monkey-patching. Skipped entirely.
THIRD_PARTY_APPS = frozenset(
    {
        "oauth2_provider",
        "otp_email",
        "otp_static",
        "otp_totp",
    }
)

# Known existing rolling-deploy hazards at the time this check was introduced.
# Each entry is ``(app_label, model_name, field_name)``. Fix by adding
# ``db_default=<value>`` to the field and generating an ``AlterField``
# migration, then REMOVE the entry from this set. The check emits
# ``karrio.W001`` for any baseline entry that is no longer a hazard, so this
# set drifts to empty over time instead of going stale.
BASELINE_HAZARDS = frozenset(
    {
        ("apps", "appinstallation", "app_type"),
        ("apps", "appinstallation", "is_active"),
        ("automation", "workflow", "is_active"),
        ("documents", "documenttemplate", "active"),
        ("events", "webhook", "secret"),
        ("manager", "pickup", "meta"),
        ("manager", "pickup", "status"),
        ("manager", "tracking", "status"),
        ("orders", "order", "order_date"),
        ("orgs", "organization", "metadata"),
        ("orgs", "organizationinvitation", "is_owner"),
        ("orgs", "organizationinvitation", "roles"),
        ("orgs", "organizationuser", "metadata"),
        ("orgs", "organizationuser", "roles"),
        ("pricing", "fee", "test_mode"),
        ("pricing", "markup", "meta"),
        ("providers", "servicelevel", "use_volumetric"),
        ("user", "token", "test_mode"),
        ("user", "user", "metadata"),
    }
)


def _is_hazard(field):
    if not field.concrete or field.many_to_many:
        return False
    if field.null:
        return False
    if field.default is NOT_PROVIDED:
        return False
    return getattr(field, "db_default", NOT_PROVIDED) is NOT_PROVIDED


@register(Tags.database)
def check_rolling_deploy_safe_fields(app_configs, **kwargs):
    issues = []

    loader = MigrationLoader(connection=None, ignore_no_migrations=True)

    added_fields = set()
    for migration in loader.disk_migrations.values():
        for operation in migration.operations:
            if isinstance(operation, AddField):
                added_fields.add((migration.app_label, operation.model_name.lower(), operation.name))

    selected_app_labels = {app_config.label for app_config in app_configs} if app_configs else None

    hazards = set()
    resolved_safe = set()  # fields we evaluated and found safe (not hazards)

    for app_label, model_name, field_name in added_fields:
        if app_label in THIRD_PARTY_APPS:
            continue
        if selected_app_labels is not None and app_label not in selected_app_labels:
            continue
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            # App not loaded in this config (e.g., community build without
            # insiders submodule). Can't evaluate — leave baseline entry alone.
            continue
        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            continue

        key = (app_label, model_name, field_name)
        if not _is_hazard(field):
            resolved_safe.add(key)
            continue

        hazards.add(key)

        if key in BASELINE_HAZARDS:
            continue

        issues.append(
            Error(
                (
                    f"{app_label}.{model_name}.{field_name} is NOT NULL with a Python "
                    f"default ({field.default!r}) but no db_default. This is a rolling-"
                    f"deploy hazard: INSERTs from pods still running pre-migration code "
                    f"will send no value for this column and trip the NOT NULL constraint."
                ),
                hint=(
                    "Add db_default=<value> to the field and generate an AlterField "
                    "migration so the DB column carries a DEFAULT clause. If you "
                    "genuinely cannot add a DB default, make the field nullable during "
                    "the deploy window and tighten it in a follow-up release."
                ),
                obj=field,
                id="karrio.E001",
            )
        )

    # Flag stale baseline entries so the allowlist shrinks as hazards are fixed.
    # Only entries we actually evaluated and found safe count as stale — not
    # entries whose app isn't loaded in this build variant.
    if selected_app_labels is None:
        for stale in sorted(BASELINE_HAZARDS & resolved_safe):
            issues.append(
                Warning(
                    (
                        f"Baseline entry {'.'.join(stale)} is no longer a rolling-"
                        f"deploy hazard — remove it from BASELINE_HAZARDS in "
                        f"karrio.server.core.checks."
                    ),
                    hint="Delete the tuple from BASELINE_HAZARDS.",
                    id="karrio.W001",
                )
            )

    return issues
