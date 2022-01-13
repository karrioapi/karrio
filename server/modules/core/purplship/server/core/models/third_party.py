from rest_framework_tracking.models import APIRequestLog

from purplship.server.core.models.base import ControlledAccessModel


class APILog(APIRequestLog, ControlledAccessModel):
    class Meta:
        ordering = ["-requested_at"]
        proxy = True

    @property
    def object_type(self):
        return "log"
