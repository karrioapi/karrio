"""
purplship server orgs module urls
"""
from django.urls import include, path
from organizations.backends import invitation_backend


urlpatterns = [
    path('invite/', include(invitation_backend().get_urls())),
]
