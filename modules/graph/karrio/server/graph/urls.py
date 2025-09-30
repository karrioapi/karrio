"""
karrio server graph module urls
"""
from django.urls import path, include


app_name = "karrio.server.graph"
urlpatterns = [
    path("", include("karrio.server.graph.views")),
]
