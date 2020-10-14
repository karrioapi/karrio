"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.conf import settings

from purpleserver.client.views import index
from purpleserver.client.views.user import UserAPI
from purpleserver.client.views.token import TokenAPI

urlpatterns = [
    path('', index, name='index'),
    path('settings', index, name='settings'),
    path('carrier_connections', index, name='carrier_connections'),

    path('', include('django.contrib.auth.urls')),
    path('', include(settings.CLIENT_REGISTRATION_VIEWS)),
    path('token', TokenAPI.as_view(), name='token'),
    path('user_info', UserAPI.as_view(), name='user_info'),
]
