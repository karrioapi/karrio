"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.contrib.auth import urls
from purpleserver.client.views import SignUp, index, TokenAPI
from purpleserver.client.views.user import UserAPI

urlpatterns = [
    path('', index, name='index'),
    path('settings', index, name='settings'),
    path('carrier_connections', index, name='carrier_connections'),

    path('', include(urls)),
    path('signup', SignUp.as_view(), name='signup'),
    path('token', TokenAPI.as_view(), name='token'),
    path('user_info', UserAPI.as_view(), name='user_info'),
]
