"""
purplship server accounts module urls
"""
from django.urls import include, path


urlpatterns = [
    path("", include("purplship.server.client.views.user")),
    path("", include("purplship.server.client.views.app")),
    path("", include("purplship.server.client.views.tracking")),
    path("test/", include("purplship.server.client.views.app")),
]
