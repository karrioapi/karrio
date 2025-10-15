"""
URL routing for JTL Hub integration.
"""

from django.urls import path
from .views import JTLTenantOnboardingView

app_name = 'karrio.server.jtl'

urlpatterns = [
    path("jtl/tenants/onboarding", JTLTenantOnboardingView.as_view(), name="jtl-onboarding"),
]
