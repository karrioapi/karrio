"""
karrio server providers module urls
"""

from django.urls import include, path

app_name = "karrio.server.providers"
urlpatterns = [
    path("v1/", include("karrio.server.providers.views.carriers")),
    path("v1/", include("karrio.server.providers.views.connections")),
]
