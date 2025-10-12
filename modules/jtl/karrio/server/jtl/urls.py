"""
URL routing for JTL Hub integration.
"""

from django.urls import path
from .views import JTLCallbackView

app_name = 'karrio.server.jtl'

urlpatterns = [
    path('auth/jtl/callback', JTLCallbackView.as_view(), name='jtl-callback'),
]
