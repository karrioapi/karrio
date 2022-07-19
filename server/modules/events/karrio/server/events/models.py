from functools import partial
from django.conf import settings
from django.db import models
from django.db.models.fields import json
from django.contrib.postgres import fields

from karrio.server.core.utils import identity
from karrio.server.core.models import OwnedEntity, uuid, register_model


@register_model
class Webhook(OwnedEntity):
    HIDDEN_PROPS = (*(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),)

    class Meta:
        db_table = "webhook"
        verbose_name = "Webhook"
        verbose_name_plural = "Webhooks"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="weh_"),
        editable=False,
    )

    enabled_events = fields.ArrayField(models.CharField(max_length=200), blank=False)
    url = models.URLField(max_length=200)
    secret = models.CharField(max_length=100, default=partial(uuid, prefix="whsec_"))
    test_mode = models.BooleanField(null=False)
    disabled = models.BooleanField(null=True, default=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    last_event_at = models.DateTimeField(null=True)

    # System Reference fields
    failure_streak_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} + {self.url}"

    @property
    def object_type(self):
        return "webhook"


class Event(OwnedEntity):
    HIDDEN_PROPS = (*(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),)

    class Meta:
        db_table = "event"
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                json.KeyTextTransform("id", "data"),
                condition=models.Q(data__id__isnull=False),
                name="event_object_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="evt_"),
        editable=False,
    )

    type = models.CharField(max_length=50)
    data = models.JSONField(default=partial(identity, value={}))
    test_mode = models.BooleanField(null=False)
    pending_webhooks = models.IntegerField(default=0)

    @property
    def object_type(self):
        return "event"
