from functools import partial
from django.db import models
from jsonfield import JSONField

from purpleserver.core.models import OwnedEntity, uuid


class Webhook(OwnedEntity):
    class Meta:
        db_table = "webhook"
        verbose_name = 'Webhook'
        verbose_name_plural = 'Webhooks'
        ordering = ['-created_at']

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='web_'), editable=False)

    enabled_events = JSONField(default=[])
    url = models.URLField(max_length=200)
    test_mode = models.BooleanField(null=False)
    disabled = models.BooleanField(null=True)
    last_event_at = models.DateTimeField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
