from functools import partial
from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator

from karrio.server.orgs.models import Organization
from karrio.server.core.models import OwnedEntity, uuid


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
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=20, validators=[RegexValidator(r"^[a-z0-9_]+$")])
    template = models.TextField()
    description = models.CharField(max_length=50, null=True, blank=True)
    related_objects = fields.ArrayField(models.CharField(max_length=25), blank=False)

    org = models.ManyToManyField(
        Organization, related_name="document_templates", through="DocumentTemplateLink"
    )

    @property
    def object_type(self):
        return "document_template"


class DocumentTemplateLink(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="document_template_links"
    )
    item = models.OneToOneField(
        DocumentTemplate, on_delete=models.CASCADE, related_name="link"
    )
