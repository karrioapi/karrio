from django.db import models
from django.contrib.postgres import search
from rest_framework_tracking.models import APIRequestLog

from karrio.server.core.models.base import ControlledAccessModel


class APILog(APIRequestLog, ControlledAccessModel):
    class Meta:
        ordering = ["-requested_at"]
        proxy = True
        indexes = [
            models.Index(
                search.SearchVectorField("response__id"),
                condition=models.Q(response__isnull=False),
                name="response_object_idx",
            ),
        ]

    @property
    def object_type(self):
        return "log"
