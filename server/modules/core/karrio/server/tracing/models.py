from functools import partial
from django.conf import settings
from django.db import models
from django.db.models.fields import json

from karrio.core.utils import identity
from karrio.server.core.models import OwnedEntity, uuid


class TracingRecord(OwnedEntity):
    HIDDEN_PROPS = (*(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),)

    class Meta:
        db_table = "tracing-record"
        verbose_name = "Tracing Record"
        verbose_name_plural = "Tracing Records"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                json.KeyTextTransform("object_id", "meta"),
                condition=models.Q(meta__object_id__isnull=False),
                name="trace_object_idx",
            ),
            models.Index(
                json.KeyTextTransform("request_log_id", "meta"),
                condition=models.Q(meta__request_log_id__isnull=False),
                name="request_log_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="trace_"),
        editable=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    key = models.CharField(max_length=50)
    record = models.JSONField(
        default=partial(identity, value={}),
        help_text="Record data",
    )
    timestamp = models.FloatField()
    meta = models.JSONField(
        blank=True,
        null=True,
        default=partial(identity, value={}),
        help_text="Readonly Context metadata use for filtering and premission check",
    )
    test_mode = models.BooleanField(null=False)

    @property
    def object_type(self):
        return "tracking_record"
