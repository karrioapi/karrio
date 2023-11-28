"""
karrio server manager module urls
"""
from django.urls import include, path
from karrio.server.manager.views import router

app_name = "karrio.server.manager"
urlpatterns = [
    path("v1/", include(router.urls)),
]
