import importlib
from constance import config
from django.urls import path
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request

from purpleserver.user.serializers import TokenSerializer
import purpleserver.core.models as core
import purpleserver.manager.models as manager

FEATURE_FLAGS = dict(
    ADDRESS_AUTO_COMPLETE=any(config.GOOGLE_CLOUD_API_KEY or ""),
    MULTI_ORGANIZATIONS=importlib.util.find_spec('purpleserver.orgs') is not None
)
ENTITY_ACCESS_VIEWS = {
    '/api_logs/': core.APILog,
    '/shipments/': manager.Shipment,
}


@login_required(login_url='/login')
def index(request: Request, *args, **kwargs):

    if FEATURE_FLAGS['MULTI_ORGANIZATIONS'] and any(k in request.path for k, _ in ENTITY_ACCESS_VIEWS.items()):
        model = next((m for k, m in ENTITY_ACCESS_VIEWS.items() if k in request.path))
        user_key = 'created_by' if hasattr(model, 'created_by') else 'user'
        orgs = getattr(
            model.objects.get(
                Q(id=kwargs['id'], org__users__id=request.user.id) |
                Q(**{"id": kwargs['id'], f"{user_key}__id": request.user.id})
            ),
            'org', None
        )
        request.org = orgs.first() if orgs.exists() else getattr(request, 'org', None)

    token = TokenSerializer.retrieve_token(request)
    if FEATURE_FLAGS['MULTI_ORGANIZATIONS']:
        request.org = token.organization

    context = dict(
        api_token=f'Token {token.key}',
        GOOGLE_CLOUD_API_KEY=config.GOOGLE_CLOUD_API_KEY,
        FEATURE_FLAGS=FEATURE_FLAGS,
    )
    template = loader.get_template('client/index.html')

    return HttpResponse(template.render(context, request))


urlpatterns = [
    path('', index, name='index'),
    path('trackers', index, name='trackers'),
    path('api_logs', index, name='api_logs'),
    path('api_logs/<str:id>', index, name='api_logs'),
    path('settings/<str:id>', index, name='settings'),
    path('buy_label/<str:id>', index, name='buy_label'),
    path('shipments/<str:id>', index, name='shipment_details'),
    path('configurations/<str:id>', index, name='configurations'),
]
