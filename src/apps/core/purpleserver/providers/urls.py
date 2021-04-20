"""
purplship server providers module urls
"""
from django.urls import include, path
from purpleserver.providers.views import router

app_name = 'purpleserver.providers'
urlpatterns = [
    path('v1/', include(router.urls)),
]
