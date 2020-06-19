"""
purplship server proxy module urls
"""
from django.urls import include, path
from purpleserver.proxy.views import router

app_name = 'purpleserver.proxy'
urlpatterns = [
    path('v1/', include(router.urls)),
]
