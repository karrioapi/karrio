"""
karrio server providers module urls
"""
from django.urls import include, path
from karrio.server.providers.views import router

app_name = 'karrio.server.providers'
urlpatterns = [
    path('v1/', include(router.urls)),
]
