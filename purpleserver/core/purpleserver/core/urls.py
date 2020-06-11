"""
purplship server core module urls
"""
from django.urls import include, path
from purpleserver.core.views import router

app_name = 'purpleserver.core'
urlpatterns = [
    path('v1/', include(router.urls)),
]
