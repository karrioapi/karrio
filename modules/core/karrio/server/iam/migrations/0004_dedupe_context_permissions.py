from django.db import migrations, models
from django.db.models import Count


def dedupe_context_permissions(apps, schema_editor):
    """Collapse duplicate ContextPermission rows before the uniqueness
    constraint is applied.

    Concurrent permission syncs (e.g. a double-submitted tenant onboarding
    mutation) could insert more than one row for the same
    (content_type, object_pk) pair. Keep the oldest row, merge the groups and
    user_permissions of the duplicates into it, then delete the extras.
    """
    ContextPermission = apps.get_model("iam", "ContextPermission")

    duplicates = (
        ContextPermission.objects.values("content_type", "object_pk").annotate(count=Count("id")).filter(count__gt=1)
    )

    for entry in duplicates:
        rows = list(
            ContextPermission.objects.filter(content_type=entry["content_type"], object_pk=entry["object_pk"]).order_by(
                "id"
            )
        )
        survivor, extras = rows[0], rows[1:]
        for extra in extras:
            survivor.groups.add(*extra.groups.all())
            survivor.user_permissions.add(*extra.user_permissions.all())
            extra.delete()


class Migration(migrations.Migration):
    # Run non-atomically: the dedupe deletes cascade into the M2M through
    # tables, which queues deferred trigger events on iam_contextpermission.
    # PostgreSQL refuses to ALTER TABLE (AddConstraint) while a table has
    # pending trigger events in the same transaction
    # ("cannot ALTER TABLE ... because it has pending trigger events").
    # Without an enclosing transaction each operation autocommits, so the
    # dedupe flushes its trigger events before the constraint is added.
    atomic = False

    dependencies = [
        ("iam", "0003_remove_permission_groups"),
    ]

    operations = [
        migrations.RunPython(
            dedupe_context_permissions,
            # Forward-only data cleanup: duplicates are a bug, never recreated.
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="contextpermission",
            constraint=models.UniqueConstraint(
                fields=["content_type", "object_pk"],
                name="unique_context_permission_per_object",
            ),
        ),
    ]
