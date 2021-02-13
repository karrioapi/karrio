from functools import partial

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

from purpleserver.core.models import Entity, uuid
from purpleserver.core.datatypes import CarrierSettings


class Carrier(Entity):
    class Meta:
        unique_together = ['carrier_id', 'user']

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='car_'), editable=False)
    carrier_id = models.CharField(
        max_length=200,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups..."
    )
    test = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"{self.carrier_id} - {self.user or 'system'}"

    def _linked_settings(self):
        for field in [f for f in self._meta.get_fields() if isinstance(f, models.OneToOneRel)]:
            try:
                return getattr(self, field.get_accessor_name())
            except:
                pass
        return None

    @property
    def data(self) -> CarrierSettings:
        settings = self._linked_settings()
        return CarrierSettings.create({
            'id': settings.pk,
            'carrier_name': settings.carrier_name,
            **model_to_dict(settings)
        })
