"""
purplship server manager module urls
"""
from django.urls import include, path
from purpleserver.manager.views import router

app_name = 'purpleserver.manager'
urlpatterns = [
    path('v1/', include(router.urls)),
]
