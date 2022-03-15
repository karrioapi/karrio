"""
karrio server orders module urls
"""
from django.urls import include, path
from karrio.server.orders.views import router

app_name = "karrio.server.orders"
urlpatterns = [
    path("v1/", include(router.urls)),
]
