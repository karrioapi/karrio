"""
purplship server proxy module urls
"""
from django.urls import include, path
from purplship.server.proxy.views import router

app_name = 'purplship.server.proxy'
urlpatterns = [
    path('v1/', include(router.urls)),
]
