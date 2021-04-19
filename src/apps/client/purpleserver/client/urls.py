"""
purplship server accounts module urls
"""
from django.urls import include, path


urlpatterns = [
    path('', include('purpleserver.client.views.app')),
    path('', include('purpleserver.client.views.tracking')),
]
