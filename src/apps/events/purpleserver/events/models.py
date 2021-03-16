from functools import partial
from django.db import models
from django.contrib.postgres import fields

from purpleserver.core.models import OwnedEntity, uuid


class Webhook(OwnedEntity):
    class Meta:
        db_table = "webhook"
        verbose_name = 'Webhook'
        verbose_name_plural = 'Webhooks'
        ordering = ['-created_at']

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='web_'), editable=False)

    enabled_events = fields.ArrayField(models.CharField(max_length=200), blank=False)
    url = models.URLField(max_length=200)
    test_mode = models.BooleanField(null=False)
    disabled = models.BooleanField(default=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    last_event_at = models.DateTimeField(null=True)

    # System Reference fields
    failure_streak_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} + {self.url}'
