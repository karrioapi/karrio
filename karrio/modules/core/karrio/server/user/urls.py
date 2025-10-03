"""
karrio server user module urls
"""
from django.urls import include, path
from django_email_verification import urls as mail_urls

urlpatterns = [
    path("email/", include(mail_urls)),
    path("", include("karrio.server.user.views")),
]
