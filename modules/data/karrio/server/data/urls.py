"""
karrio server data module urls
"""
from django.urls import include, path

app_name = "karrio.server.data"
urlpatterns = [
    path("v1/", include("karrio.server.data.views.data")),
    path("v1/", include("karrio.server.data.views.batch")),
    path("v1/", include("karrio.server.data.views.batch_order")),
    path("v1/", include("karrio.server.data.views.batch_shipment")),
    path("v1/", include("karrio.server.data.views.batch_tracking")),
]
