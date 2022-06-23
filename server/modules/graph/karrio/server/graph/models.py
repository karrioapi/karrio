from django.conf import settings
from django.db import models

from karrio.server.core.models import OwnedEntity, uuid, register_model
from karrio.server.manager.models import Customs, Parcel, Address


@register_model
class Template(OwnedEntity):
    HIDDEN_PROPS = (*(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),)

    class Meta:
        db_table = "template"
        ordering = ["-is_default", "-created_by"]

    id = models.CharField(max_length=50, primary_key=True, default=uuid, editable=False)
    label = models.CharField(max_length=50)
    is_default = models.BooleanField(blank=True, default=False)

    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    customs = models.OneToOneField(
        Customs, on_delete=models.CASCADE, null=True, blank=True
    )
    parcel = models.OneToOneField(
        Parcel, on_delete=models.CASCADE, null=True, blank=True
    )

    def delete(self, *args, **kwargs):
        attachment = next(
            (
                entity
                for entity in [self.address, self.customs, self.parcel]
                if entity is not None
            ),
            super(),
        )

        return attachment.delete(*args, **kwargs)

    @property
    def object_type(self):
        return "template"
