from constance import config
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request
from rest_framework.authtoken.models import Token


@login_required(login_url='/login')
def index(request: Request, *args, **kwargs):
    token, created = Token.objects.get_or_create(user=request.user)
    context = dict(token=token, GOOGLE_CLOUD_API_KEY=config.GOOGLE_CLOUD_API_KEY)
    template = loader.get_template('client/index.html')

    return HttpResponse(template.render(context, request))
