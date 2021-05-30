from rest_framework_tracking.models import APIRequestLog

from purpleserver.core.models.base import ControlledAccessModel


class APILog(APIRequestLog, ControlledAccessModel):
    class Meta:
        ordering = ["-requested_at"]
        proxy = True

