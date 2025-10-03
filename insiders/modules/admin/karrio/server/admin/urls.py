"""
karrio server admin module urls
"""
from django.urls import path, include


app_name = "karrio.server.admin"
urlpatterns = [
    path("", include("karrio.server.admin.views")),
]
