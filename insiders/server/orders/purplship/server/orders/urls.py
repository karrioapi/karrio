"""
purplship server orders module urls
"""
from django.urls import include, path
from purplship.server.orders.views import router

app_name = "purplship.server.orders"
urlpatterns = [
    path("v1/", include(router.urls)),
]
