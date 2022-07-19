from django.db import models
from rest_framework_tracking.models import APIRequestLog

from karrio.server.core.models.base import ControlledAccessModel


class APILog(APIRequestLog, ControlledAccessModel):
    class Meta:
        ordering = ["-requested_at"]
        proxy = True

    @property
    def object_type(self):
        return "log"


class APILogIndex(APILog):
    entity_id = models.CharField(max_length=50, null=True, db_index=True)
