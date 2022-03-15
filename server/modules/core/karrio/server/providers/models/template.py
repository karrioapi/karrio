from functools import partial
from django.db import models

from karrio.server.core.models import OwnedEntity, uuid

LABEL_TEMPLATE_TYPES = [
    ("SVG", "SVG"),
    ("ZPL", "ZPL"),
]


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
    alias = models.CharField(max_length=50)
    template = models.TextField()
    description = models.CharField(max_length=50, null=True, blank=True)
    template_type = models.CharField(max_length=3, choices=LABEL_TEMPLATE_TYPES)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    @property
    def object_type(self):
        return "label_template"
