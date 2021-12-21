from functools import partial
from django.db import models

from purplship.server.core.models import OwnedEntity, uuid


class LabelTemplate(OwnedEntity):
    class Meta:
        db_table = "label-template"
        verbose_name = "Label Template"
        verbose_name_plural = "Label Templates"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="tpl_"),
        editable=False,
    )
    name = models.CharField(max_length=50)
    template = models.TextField()
    description = models.CharField(max_length=50, null=True, blank=True)
