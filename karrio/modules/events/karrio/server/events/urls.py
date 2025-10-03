"""
karrio server events module urls
"""
from django.urls import include, path
from karrio.server.events.views import router

app_name = 'karrio.server.events'
urlpatterns = [
    path('v1/', include(router.urls)),
]
