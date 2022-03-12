"""
purplship server documents module urls
"""
from django.urls import include, path

app_name = "purplship.server.documents"
urlpatterns = [
    path("", include("purplship.server.documents.views")),
]
