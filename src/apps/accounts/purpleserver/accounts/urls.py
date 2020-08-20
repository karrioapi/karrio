"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.contrib.auth import urls
from purpleserver.accounts.views import SignUp

urlpatterns = [
    path('', include(urls), name="accounts"),
    path('signup', SignUp.as_view(), name='signup'),
]
