"""
karrio server proxy module urls
"""
from django.urls import include, path
from karrio.server.proxy.views import router

app_name = 'karrio.server.proxy'
urlpatterns = [
    path('v1/', include(router.urls)),
]
