"""
purplship server events module urls
"""
from django.urls import include, path
from purpleserver.events.views import router

app_name = 'purpleserver.events'
urlpatterns = [
    path('v1/', include(router.urls)),
]
