from functools import partial
from django.db import models
from django.core.validators import RegexValidator

import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.data.serializers as serializers


@core.register_model
class BatchOperation(core.OwnedEntity):
    class Meta:
        db_table = "batch-operation"
        verbose_name = "Batch Operation"
        verbose_name_plural = "Batch Operations"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(core.uuid, prefix="batch_"),
        editable=False,
    )

    status = models.CharField(
        max_length=25,
        choices=serializers.OPERATION_STATUS,
        default=serializers.OPERATION_STATUS[0][0],
    )
    resource_type = models.CharField(
        max_length=25,
        choices=serializers.RESOURCE_TYPE,
        default=serializers.RESOURCE_TYPE[0][0],
    )
    resources = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
    )
    test_mode = models.BooleanField(null=False)

    @property
    def object_type(self):
        return "batch"


@core.register_model
class DataTemplate(core.OwnedEntity):
    class Meta:
        db_table = "data-template"
        verbose_name = "Data Template"
        verbose_name_plural = "Data Templates"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(core.uuid, prefix="data_"),
        editable=False,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=25, validators=[RegexValidator(r"^[a-z0-9_]+$")])
    description = models.CharField(max_length=50, null=True, blank=True)
    resource_type = models.CharField(
        max_length=25, blank=False, null=False, choices=serializers.RESOURCE_TYPE
    )
    fields_mapping = models.JSONField(
        blank=False,
        null=False,
        default=partial(utils.identity, value={}),
        help_text="""
        The fields is a mapping of key value pairs linking the resource type's
        data field (key) to header used for import/export.

        e.g: resource: tracking | fields [{'id': 'ID', 'tracking_number': 'Tracking Number'}]
        """,
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
    )

    @property
    def object_type(self):
        return "data_template"

    @property
    def data_fields(self):
        default_fields_mapping = serializers.ResourceType.get_default_mapping(
            self.resource_type
        )

        return {
            **default_fields_mapping,
            **self.fields_mapping,
        }
