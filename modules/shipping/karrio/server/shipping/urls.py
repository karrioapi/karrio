"""
karrio server shipping module urls
"""
from django.urls import include, path
from karrio.server.shipping.views import router

app_name = "karrio.server.shipping"
urlpatterns = [
    path("v1/", include(router.urls)),
]
