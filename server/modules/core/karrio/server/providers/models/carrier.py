from functools import partial
from typing import Dict

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator

import karrio
import karrio.core.units as units
import karrio.core.utils as utils
import karrio.api.gateway as gateway
import karrio.server.core.models as core
import karrio.server.core.fields as fields
import karrio.server.core.datatypes as datatypes


COUNTRIES = [(c.name, c.name) for c in units.Country]
CURRENCIES = [(c.name, c.name) for c in units.Currency]
WEIGHT_UNITS = [(c.name, c.name) for c in units.WeightUnit]
DIMENSION_UNITS = [(c.name, c.name) for c in units.DimensionUnit]
CAPABILITIES_CHOICES = [(c, c) for c in units.CarrierCapabilities.get_capabilities()]


class CarrierManager(models.Manager):
    def get_queryset(self):
        from karrio.server.providers.models import MODELS

        return (
            super()
            .get_queryset()
            .prefetch_related(*[Model.__name__.lower() for Model in MODELS.values()])
        )


class Carrier(core.OwnedEntity):
    class Meta:
        ordering = ["test_mode", "-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_id = models.CharField(
        max_length=200,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups...",
        db_index=True,
    )
    test_mode = models.BooleanField(
        default=True, db_column="test_mode", help_text="Toggle carrier connection mode"
    )
    active = models.BooleanField(
        default=True, help_text="Disable/Hide carrier from clients", db_index=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    active_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="active_users"
    )
    capabilities = fields.MultiChoiceField(
        choices=CAPABILITIES_CHOICES,
        default=core.field_default([]),
        help_text="Select the capabilities of the carrier that you want to enable",
    )
    metadata = models.JSONField(blank=True, null=True, default=dict)

    objects = CarrierManager()

    def __str__(self):
        return self.carrier_id

    @property
    def object_type(self):
        return "carrier"

    @property
    def carrier_name(self):
        return getattr(self.settings, "carrier_name", None)

    @property
    def settings(self):
        _, settings = self.__class__.resolve_settings(self)
        return settings

    @property
    def ext(self) -> str:
        return (
            "generic"
            if hasattr(self.settings, "custom_carrier_name")
            else self.settings.carrier_name
        )

    @property
    def gateway(self) -> gateway.Gateway:
        from karrio.server.core import middleware

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", utils.Tracer())
        _carrier_name = self.ext

        return karrio.gateway[_carrier_name].create({**self.data.to_dict()}, _tracer)

    @property
    def data(self) -> datatypes.CarrierSettings:
        _extra: Dict = dict()

        if hasattr(self.settings, "services"):
            _extra.update(
                services=[model_to_dict(s) for s in self.settings.services.all()]
            )

        return datatypes.CarrierSettings.create(
            {
                "id": self.settings.id,
                "carrier_name": self.settings.carrier_name,
                "display_name": self.settings.carrier_display_name,
                **model_to_dict(self.settings),
                **_extra,
            }
        )

    @staticmethod
    def resolve_settings(carrier):
        from karrio.server.providers.models import MODELS

        return next(
            (
                (name, getattr(carrier, model.__name__.lower()))
                for name, model in MODELS.items()
                if hasattr(carrier, model.__name__.lower())
            ),
            (None, None),
        )

    @property
    def carrier_display_name(self):
        if hasattr(self.settings, "display_name"):
            return self.settings.display_name

        import karrio.references as references

        return references.collect_references()["carriers"].get(
            self.settings.carrier_name
        )


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
        default=partial(core.uuid, prefix="svc_"),
        editable=False,
    )
    service_name = models.CharField(max_length=50)
    service_code = models.CharField(
        max_length=50, validators=[RegexValidator(r"^[a-z0-9_]+$")]
    )
    description = models.CharField(max_length=250, null=True, blank=True)
    active = models.BooleanField(null=True, default=True)

    cost = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=4, choices=CURRENCIES, null=True, blank=True)

    estimated_transit_days = models.IntegerField(blank=True, null=True)

    max_weight = models.FloatField(blank=True, null=True)
    max_width = models.FloatField(blank=True, null=True)
    max_height = models.FloatField(blank=True, null=True)
    max_length = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(
        max_length=2, choices=WEIGHT_UNITS, null=True, blank=True
    )
    dimension_unit = models.CharField(
        max_length=2, choices=DIMENSION_UNITS, null=True, blank=True
    )

    domicile = models.BooleanField(null=True)
    international = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.id} | {self.service_name}"

    @property
    def object_type(self):
        return "service_level"
