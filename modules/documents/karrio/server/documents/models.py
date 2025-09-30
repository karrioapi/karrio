import functools
import django.urls as urls
from django.db import models
from django.core.validators import RegexValidator

import karrio.server.core.models as core


@core.register_model
class DocumentTemplate(core.OwnedEntity):
    class Meta:
        db_table = "document-template"
        verbose_name = "Document Template"
        verbose_name_plural = "Document Templates"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="doc_"),
        editable=False,
    )
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(
        max_length=20,
        validators=[RegexValidator(r"^[a-z0-9_]+$")],
        db_index=True,
    )
    template = models.TextField()
    description = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
    )
    related_object = models.CharField(max_length=25, blank=True, null=True)
    active = models.BooleanField(
        default=True,
        help_text="disable template flag. to filter out from active document downloads",
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
    )
    options = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
    )

    @property
    def object_type(self):
        return "document-template"

    @property
    def preview_url(self):
        return urls.reverse(
            "karrio.server.documents:templates-documents-print",
            kwargs=dict(pk=self.pk, slug=self.slug),
        ) + f"?{self.related_object or 'shipment'}s=sample"
