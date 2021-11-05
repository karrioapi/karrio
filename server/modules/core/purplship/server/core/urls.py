"""
purplship server core module urls
"""
from django.urls import include, path
from purplship.server.core.views import router

app_name = 'purplship.server.core'
urlpatterns = [
    path('v1/', include(router.urls)),
]
