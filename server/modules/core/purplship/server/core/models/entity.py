from django.db import models
from django.conf import settings
from karrio.server.core.models.base import uuid, ControlledAccessModel


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.CharField(max_length=50, primary_key=True, default=uuid, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class OwnedEntity(ControlledAccessModel, Entity):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
