"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.contrib.auth import urls
from purpleserver.client.views import SignUp, index, TokenAPI

urlpatterns = [
    path('', index, name='index'),
    path('settings', index, name='index'),
    path('providers', index, name='index'),

    path('', include(urls)),
    path('signup', SignUp.as_view(), name='signup'),
    path('token', TokenAPI.as_view(), name='token'),
]
