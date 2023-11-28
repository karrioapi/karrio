"""
karrio server documents module urls
"""
from django.urls import include, path

app_name = "karrio.server.documents"
urlpatterns = [
    path("", include("karrio.server.documents.views")),
]
