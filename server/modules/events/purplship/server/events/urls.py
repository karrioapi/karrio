"""
purplship server events module urls
"""
from django.urls import include, path
from purplship.server.events.views import router

app_name = 'purplship.server.events'
urlpatterns = [
    path('v1/', include(router.urls)),
]
