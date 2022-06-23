from functools import partial
from django.db import models
from django.core.validators import RegexValidator

from karrio.server.core.models import OwnedEntity, uuid, register_model

LABEL_TEMPLATE_TYPES = [
    ("SVG", "SVG"),
    ("ZPL", "ZPL"),
]


@register_model
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
    slug = models.SlugField(max_length=30, validators=[RegexValidator(r"^[a-z0-9_]+$")])
    template = models.TextField()
    template_type = models.CharField(max_length=3, choices=LABEL_TEMPLATE_TYPES)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    shipment_sample = models.JSONField(blank=True, null=True, default=dict)

    @property
    def object_type(self):
        return "label_template"
