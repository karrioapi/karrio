from functools import partial
from django.db import models

from purpleserver.core.models.entity import Entity, uuid


class Carrier(Entity):
    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='car_'), editable=False)
    carrier_id = models.CharField(
        max_length=200, unique=True,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups..."
    )
    test = models.BooleanField(default=True)

    def __str__(self):
        return self.carrier_id

    def settings(self):
        for field in [f for f in self._meta.get_fields() if isinstance(f, models.OneToOneRel)]:
            try:
                return getattr(self, field.get_accessor_name())
            except:
                pass
        return None
