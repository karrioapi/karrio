"""
karrio server admin module urls
"""

from django.urls import include, path

app_name = "karrio.server.admin"
urlpatterns = [
    path("", include("karrio.server.admin.views")),
]
