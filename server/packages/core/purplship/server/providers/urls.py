"""
purplship server providers module urls
"""
from django.urls import include, path
from purplship.server.providers.views import router

app_name = 'purplship.server.providers'
urlpatterns = [
    path('v1/', include(router.urls)),
]
