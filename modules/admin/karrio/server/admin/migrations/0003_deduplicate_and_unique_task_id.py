from datetime import timedelta

from django.db import migrations, models
from django.utils import timezone


def deduplicate_and_fix_stale(apps, schema_editor):
    """Remove duplicate TaskExecution records and fix stale 'executing' statuses."""
    TaskExecution = apps.get_model("karrio_admin", "TaskExecution")
    from django.db.models import Count

    # 1. Deduplicate: find task_ids with multiple records
    dupes = (
        TaskExecution.objects.values("task_id")
        .annotate(cnt=Count("id"))
        .filter(cnt__gt=1)
    )

    for entry in dupes:
        task_id = entry["task_id"]
        records = TaskExecution.objects.filter(task_id=task_id).order_by("-id")
        # Keep the latest (highest id), delete the rest
        keep = records.first()
        records.exclude(pk=keep.pk).delete()

    # 2. Fix stale "executing" tasks — if started more than 10 minutes ago,
    #    the task is done but its completion signal failed to record.
    stale_cutoff = timezone.now() - timedelta(minutes=10)
    TaskExecution.objects.filter(
        status="executing",
        started_at__lt=stale_cutoff,
    ).update(status="complete")


class Migration(migrations.Migration):

    dependencies = [
        (
            "karrio_admin",
            "0002_rename_admin_task_e_queued__b1c3e3_idx_admin_task__queued__be444e_idx_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            deduplicate_and_fix_stale,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="taskexecution",
            name="task_id",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
