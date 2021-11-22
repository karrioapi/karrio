from functools import partial

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

from purplship import gateway
from purplship.core.utils import Enum
from purplship.core.units import Country, Currency, DimensionUnit, WeightUnit
from purplship.api.gateway import Gateway
from purplship.server.core.models import OwnedEntity, uuid
from purplship.server.core.datatypes import CarrierSettings
from purplship.server.core.fields import MultiChoiceField


class CarrierCapabilities(Enum):
    pickup = "pickup"
    rating = "rating"
    shipping = "shipping"
    tracking = "tracking"

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
        from purplship.server.providers.models import MODELS

        return (
            super()
            .get_queryset()
            .prefetch_related(*[Model.__name__.lower() for Model in MODELS.values()])
        )


class Carrier(OwnedEntity):
    class Meta:
        ordering = ["test", "-created_at"]

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
    test = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
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
    )

    objects = CarrierManager()

    def __str__(self):
        return self.carrier_id

    def _linked_settings(self):
        from purplship.server.providers.models import MODELS

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
    def carrier_name(self):
        return self.settings.carrier_name

    @property
    def data(self) -> CarrierSettings:
        return CarrierSettings.create(
            {
                "id": self.settings.id,
                "carrier_name": self.settings.carrier_name,
                **model_to_dict(self.settings),
            }
        )

    @property
    def gateway(self) -> Gateway:
        return gateway[self.settings.carrier_name].create({**self.data.dict()})


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
    service_code = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)

    cost = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=4, choices=CURRENCIES, null=True)

    estimated_transit_days = models.IntegerField(blank=True, null=True)

    max_weight = models.FloatField(blank=True, null=True)
    max_width = models.FloatField(blank=True, null=True)
    max_height = models.FloatField(blank=True, null=True)
    max_length = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNITS, null=True)
    dimension_unit = models.CharField(max_length=2, choices=DIMENSION_UNITS, null=True)

    domicile = models.BooleanField(null=True)
    international = models.BooleanField(null=True)
