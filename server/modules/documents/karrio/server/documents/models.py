from functools import partial
from django.db import models
from django.core.validators import RegexValidator

from karrio.server.core.models import OwnedEntity, uuid, register_model


@register_model
class DocumentTemplate(OwnedEntity):
    class Meta:
        db_table = "document-template"
        verbose_name = "Document Template"
        verbose_name_plural = "Document Templates"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="doc_"),
        editable=False,
    )
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(
        max_length=20, validators=[RegexValidator(r"^[a-z0-9_]+$")], db_index=True
    )
    template = models.TextField()
    description = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    related_object = models.CharField(max_length=25, blank=False)
    active = models.BooleanField(
        default=True,
        help_text="disable template flag. to filter out from active document downloads",
    )

    @property
    def object_type(self):
        return "document_template"
