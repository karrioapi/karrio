from django.db import models

from purpleserver.core.models import OwnedEntity, uuid
from purpleserver.manager.models import Customs, Parcel, Address


class Template(OwnedEntity):
    class Meta:
        db_table = "template"
        ordering = ['-created_at']

    id = models.CharField(max_length=50, primary_key=True, default=uuid, editable=False)
    label = models.CharField(max_length=50)
    is_default = models.BooleanField(null=True)

    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    customs = models.OneToOneField(Customs, on_delete=models.CASCADE, null=True, blank=True)
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE, null=True, blank=True)

    def delete(self, *args, **kwargs):
        attachment = next(
            (entity for entity in [self.address, self.customs, self.parcel] if entity is not None),
            super()
        )

        return attachment.delete(*args, **kwargs)
