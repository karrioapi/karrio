"""
karrio server data module urls
"""
from django.urls import include, path

app_name = "karrio.server.data"
urlpatterns = [
    path("data/", include("karrio.server.data.views")),
]
