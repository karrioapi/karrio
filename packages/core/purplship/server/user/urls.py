"""
purplship server user module urls
"""
from django.urls import include, path


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('purplship.server.user.views')),
]
