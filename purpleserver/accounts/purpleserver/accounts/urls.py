"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.contrib.auth import urls
from purpleserver.accounts.views import SignUp

urlpatterns = [
    path('accounts/', include(urls), name="accounts"),
    path('accounts/signup', SignUp.as_view(), name='signup'),
]
