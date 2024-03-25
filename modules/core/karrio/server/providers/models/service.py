import functools
import django.db.models as models
import django.core.validators as validators

import karrio.server.core.models as core
import karrio.server.core.datatypes as datatypes


@core.register_model
class ServiceLevel(core.OwnedEntity):
    class Meta:
        db_table = "service-level"
        verbose_name = "Service Level"
        verbose_name_plural = "Service Levels"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="svc_"),
        editable=False,
    )
    service_name = models.CharField(max_length=50)
    service_code = models.CharField(
        max_length=50, validators=[validators.RegexValidator(r"^[a-z0-9_]+$")]
    )
    carrier_service_code = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    active = models.BooleanField(null=True, default=True)

    currency = models.CharField(
        max_length=4, choices=datatypes.CURRENCIES, null=True, blank=True
    )

    transit_days = models.IntegerField(blank=True, null=True)
    transit_time = models.FloatField(blank=True, null=True)

    max_width = models.FloatField(blank=True, null=True)
    max_height = models.FloatField(blank=True, null=True)
    max_length = models.FloatField(blank=True, null=True)
    dimension_unit = models.CharField(
        max_length=2, choices=datatypes.DIMENSION_UNITS, null=True, blank=True
    )

    min_weight = models.FloatField(blank=True, null=True)
    max_weight = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(
        max_length=2, choices=datatypes.WEIGHT_UNITS, null=True, blank=True
    )

    domicile = models.BooleanField(null=True)
    international = models.BooleanField(null=True)

    zones = models.JSONField(blank=True, null=True, default=core.field_default([]))
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    def __str__(self):
        return f"{self.id} | {self.service_name}"

    @property
    def object_type(self):
        return "service_level"
