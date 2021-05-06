from functools import partial

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

from purpleserver.core.models import OwnedEntity, OwnedEntityManager, uuid
from purpleserver.core.datatypes import CarrierSettings


class CarrierManager(OwnedEntityManager):
    def get_queryset(self):
        from purpleserver.providers.models import MODELS
        return super().get_queryset().prefetch_related(*[Model.__name__.lower() for Model in MODELS.values()])


class Carrier(OwnedEntity):
    class Meta:
        ordering = ['test', '-created_at']

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='car_'), editable=False)
    carrier_id = models.CharField(
        max_length=200, unique=True,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups..."
    )
    test = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, editable=False)

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
    def data(self) -> CarrierSettings:
        settings = self.settings
        return CarrierSettings.create({
            'id': settings.id,
            'carrier_name': settings.carrier_name,
            **model_to_dict(settings)
        })
