"""
karrio server automation module urls
"""
from django.urls import include, path
from karrio.server.automation.views import router

app_name = "karrio.server.automation"
urlpatterns = [
    path("v1/", include(router.urls)),
]
