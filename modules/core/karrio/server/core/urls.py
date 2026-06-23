"""
karrio server core module urls
"""

from django.conf import settings
from django.urls import include, path
from karrio.server.core.views import health, metadata, router

app_name = "karrio.server.core"
urlpatterns = [
    path("", metadata.view, name="metadata"),
    path("v1/", include(router.urls), name="references"),
    path(
        "status/",
        health.StatusView.as_view(checks=settings.HEALTH_CHECK_CHECKS),
        name="health_check",
    ),
]
