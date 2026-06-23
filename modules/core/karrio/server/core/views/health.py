import asyncio

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from health_check.views import HealthCheckView


class StatusView(HealthCheckView):
    """Liveness/readiness endpoint that runs the configured health checks but
    returns only a status code — never the infra detail (hostnames, paths,
    Redis coordinates, resource metrics) that django-health-check's default
    response leaks on this unauthenticated endpoint. See issue #581.

    Overriding get() means the ?format= query param and Accept header are
    ignored, so no format (json/text/atom/rss/openmetrics) can reach the
    leaky renderers.
    """

    @method_decorator(never_cache)
    async def get(self, request, *args, **kwargs):
        results = await asyncio.gather(*(check.get_result() for check in self.get_checks()))
        if any(result.error for result in results):
            return HttpResponse("unavailable", status=500, content_type="text/plain")
        return HttpResponse("OK", status=200, content_type="text/plain")
