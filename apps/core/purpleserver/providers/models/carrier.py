import typing
from functools import partial

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

from purplship import gateway
from purplship.core.utils import Enum
from purplship.core.units import Country
from purplship.api.gateway import Gateway
from purpleserver.core.models import OwnedEntity, uuid
from purpleserver.core.datatypes import CarrierSettings
from purpleserver.core.fields import MultiChoiceField


class CarrierCapabilities(Enum):
    pickup = 'pickup'
    rating = 'rating'
    shipping = 'shipping'
    tracking = 'tracking'

    @classmethod
    def get_capabilities(cls):
        return [c.name for c in list(cls)]


CAPABILITIES_CHOICES = [(c, c) for c in CarrierCapabilities.get_capabilities()]
COUNTRIES = [(c.name, c.name) for c in Country]



class CarrierManager(models.Manager):
    def get_queryset(self):
        from purpleserver.providers.models import MODELS
        return super().get_queryset().prefetch_related(*[Model.__name__.lower() for Model in MODELS.values()])


class Carrier(OwnedEntity):
    class Meta:
        ordering = ['test', '-created_at']

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='car_'), editable=False)
    carrier_id = models.CharField(
        max_length=200, help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups...")
    test = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, editable=False)
    active_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='active_users')
    capabilities = MultiChoiceField(
        models.CharField(max_length=50, choices=CAPABILITIES_CHOICES),
        default=CarrierCapabilities.get_capabilities,
        size=len(CAPABILITIES_CHOICES))

    objects = CarrierManager()

    def __str__(self):
        return f"{self.carrier_id} - {self.created_by or 'system'}"

    def _linked_settings(self):
        from purpleserver.providers.models import MODELS

        return next((
            getattr(self, Model.__name__.lower())
            for Model in MODELS.values()
            if hasattr(self, Model.__name__.lower())
        ), None)

    @property
    def settings(self):
        return self._linked_settings()

    @property
    def carrier_name(self):
        return self.settings.carrier_name

    @property
    def data(self) -> CarrierSettings:
        return CarrierSettings.create({
            'id': self.settings.id,
            'carrier_name': self.settings.carrier_name,
            **model_to_dict(self.settings)
        })

    @property
    def gateway(self) -> Gateway:
        return gateway[self.settings.carrier_name].create({**self.data.dict()})

