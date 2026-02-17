from django.db import models


class TaskExecution(models.Model):
    """Records Huey task execution lifecycle events."""

    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("executing", "Executing"),
        ("complete", "Complete"),
        ("error", "Error"),
        ("retrying", "Retrying"),
        ("revoked", "Revoked"),
        ("expired", "Expired"),
    ]

    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True)
    queued_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    retries = models.IntegerField(default=0)
    args_summary = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "karrio_admin"
        db_table = "admin_task_execution"
        ordering = ["-queued_at"]
        indexes = [
            models.Index(fields=["-queued_at"]),
            models.Index(fields=["status", "-queued_at"]),
            models.Index(fields=["task_name", "-queued_at"]),
        ]

    def __str__(self):
        return f"{self.task_name} ({self.task_id}) - {self.status}"
