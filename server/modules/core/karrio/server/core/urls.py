"""
karrio server core module urls
"""
from django.urls import include, path
from karrio.server.core.views import metadata, router

app_name = "karrio.server.core"
urlpatterns = [
    path("", metadata.view, name="metadata"),
    path("v1/", include(router.urls), name="references"),
    path("status/", include("health_check.urls")),
]
