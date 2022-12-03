from functools import partial
from typing import Dict

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator

from karrio import gateway
from karrio.core.utils import Enum, Tracer
from karrio.core.units import Country, Currency, DimensionUnit, WeightUnit
from karrio.api.gateway import Gateway
from karrio.server.core.models import OwnedEntity, uuid, register_model
from karrio.server.core.datatypes import CarrierSettings
from karrio.server.core.fields import MultiChoiceField


class CarrierCapabilities(Enum):
    pickup = "pickup"
    rating = "rating"
    shipping = "shipping"
    tracking = "tracking"
    paperless = "paperless"

    @classmethod
    def get_capabilities(cls):
        return [c.name for c in list(cls)]


CAPABILITIES_CHOICES = [(c, c) for c in CarrierCapabilities.get_capabilities()]
COUNTRIES = [(c.name, c.name) for c in Country]
CURRENCIES = [(c.name, c.name) for c in Currency]
WEIGHT_UNITS = [(c.name, c.name) for c in WeightUnit]
DIMENSION_UNITS = [(c.name, c.name) for c in DimensionUnit]


class CarrierManager(models.Manager):
    def get_queryset(self):
        from karrio.server.providers.models import MODELS

        return (
            super()
            .get_queryset()
            .prefetch_related(*[Model.__name__.lower() for Model in MODELS.values()])
        )


class Carrier(OwnedEntity):
    class Meta:
        ordering = ["test_mode", "-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="car_"),
        editable=False,
    )
    carrier_id = models.CharField(
        max_length=200,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups...",
    )
    test_mode = models.BooleanField(
        default=True, db_column="test_mode", help_text="Toggle carrier connection mode"
    )
    active = models.BooleanField(
        default=True, help_text="Disable/Hide carrier from clients"
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
    capabilities = MultiChoiceField(
        models.CharField(max_length=50, choices=CAPABILITIES_CHOICES),
        default=CarrierCapabilities.get_capabilities,
        size=len(CAPABILITIES_CHOICES),
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
        return self.settings.carrier_name

    def _linked_settings(self):
        from karrio.server.providers.models import MODELS

        return next(
            (
                getattr(self, Model.__name__.lower())
                for Model in MODELS.values()
                if hasattr(self, Model.__name__.lower())
            ),
            None,
        )

    @property
    def settings(self):
        return self._linked_settings()

    @property
    def data(self) -> CarrierSettings:
        _extra: Dict = dict()

        if hasattr(self.settings, "services"):
            _extra.update(
                services=[model_to_dict(s) for s in self.settings.services.all()]
            )

        return CarrierSettings.create(
            {
                "id": self.settings.id,
                "carrier_name": self.settings.carrier_name,
                **model_to_dict(self.settings),
                **_extra,
            }
        )

    @property
    def gateway(self) -> Gateway:
        from karrio.server.core import middleware

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", Tracer())
        _carrier_name = (
            "generic"
            if hasattr(self.settings, "custom_carrier_name")
            else self.settings.carrier_name
        )

        return gateway[_carrier_name].create({**self.data.to_dict()}, _tracer)


@register_model
class ServiceLevel(OwnedEntity):
    class Meta:
        db_table = "service-level"
        verbose_name = "Service Level"
        verbose_name_plural = "Service Levels"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="svc_"),
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
