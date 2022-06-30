from functools import partial
from django.db import models
from django.core.validators import RegexValidator

from karrio.server.core.utils import identity
from karrio.server.orgs.models import Organization
from karrio.server.core.models import OwnedEntity, uuid
from karrio.server.data.serializers import OPERATION_STATUS, RESOURCE_TYPE, ResourceType


class BatchOperation(OwnedEntity):
    class Meta:
        db_table = "batch-operation"
        verbose_name = "Batch Operation"
        verbose_name_plural = "Batch Operations"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="batch_"),
        editable=False,
    )

    status = models.CharField(
        max_length=25, choices=OPERATION_STATUS, default=OPERATION_STATUS[0][0]
    )
    resource_type = models.CharField(
        max_length=25, choices=RESOURCE_TYPE, default=RESOURCE_TYPE[0][0]
    )
    resources = models.JSONField(
        blank=True, null=True, default=partial(identity, value=[])
    )
    test_mode = models.BooleanField(null=False)

    org = models.ManyToManyField(
        Organization, related_name="batch_operations", through="BatchOperationLink"
    )

    @property
    def object_type(self):
        return "batch"


class BatchOperationLink(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="batch_operation_links"
    )
    item = models.OneToOneField(
        BatchOperation, on_delete=models.CASCADE, related_name="link"
    )


class DataTemplate(OwnedEntity):
    class Meta:
        db_table = "data-template"
        verbose_name = "Data Template"
        verbose_name_plural = "Data Templates"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="data_"),
        editable=False,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=25, validators=[RegexValidator(r"^[a-z0-9_]+$")])
    description = models.CharField(max_length=50, null=True, blank=True)
    resource_type = models.CharField(
        max_length=25, blank=False, null=False, choices=RESOURCE_TYPE
    )
    fields_mapping = models.JSONField(
        blank=False,
        null=False,
        default=partial(identity, value={}),
        help_text="""
        The fields is a mapping of key value pairs linking the resource type's
        data field (key) to header used for import/export.

        e.g: resource: tracking | fields [{'id': 'ID', 'tracking_number': 'Tracking Number'}]
        """,
    )

    org = models.ManyToManyField(
        Organization, related_name="data_templates", through="DataTemplateLink"
    )

    @property
    def object_type(self):
        return "data_template"

    @property
    def data_fields(self):
        default_fields_mapping = ResourceType.get_default_mapping(self.resource_type)

        return {
            **default_fields_mapping,
            **self.fields_mapping,
        }


class DataTemplateLink(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="data_template_links"
    )
    item = models.OneToOneField(
        DataTemplate, on_delete=models.CASCADE, related_name="link"
    )
