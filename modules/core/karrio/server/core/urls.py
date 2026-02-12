"""
karrio server core module urls
"""
from django.urls import include, path
from django.conf import settings
from health_check.views import HealthCheckView
from karrio.server.core.views import metadata, router

app_name = "karrio.server.core"
urlpatterns = [
    path("", metadata.view, name="metadata"),
    path("v1/", include(router.urls), name="references"),
    path(
        "status/",
        HealthCheckView.as_view(checks=settings.HEALTH_CHECK_CHECKS),
        name="health_check",
    ),
]
