from constance import config
from django.urls import path
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken


@login_required(login_url='/login')
def index(request: Request, *args, **kwargs):
    pair = RefreshToken.for_user(request.user)
    context = dict(
        refresh_token=str(pair),
        access_token=str(pair.access_token),
        GOOGLE_CLOUD_API_KEY=config.GOOGLE_CLOUD_API_KEY
    )
    template = loader.get_template('client/index.html')

    return HttpResponse(template.render(context, request))


urlpatterns = [
    path('', index, name='index'),
    path('api_logs', index, name='api_logs'),
    path('api_logs/<str:log_id>', index, name='api_logs'),
    path('buy_label/<str:id>', index, name='buy_label'),
    path('shipments/<str:id>', index, name='shipment_details'),
    path('configurations/<str:config_name>', index, name='configurations'),
    path('trackers', index, name='trackers'),
    path('settings/<str:settings_name>', index, name='settings'),
]
