"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.contrib.auth import urls
from purpleserver.client.views import SignUp, index

urlpatterns = [
    path('', index, name='index'),
    path('', include(urls)),
    path('signup', SignUp.as_view(), name='signup'),
]
