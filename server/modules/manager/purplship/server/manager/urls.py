"""
purplship server manager module urls
"""
from django.urls import include, path
from purplship.server.manager.views import router

app_name = "purplship.server.manager"
urlpatterns = [
    path("v1/", include(router.urls)),
]
