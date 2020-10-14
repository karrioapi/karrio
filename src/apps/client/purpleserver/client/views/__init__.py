from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request
from rest_framework.authtoken.models import Token


@login_required(login_url='/login')
def index(request: Request):
    token, created = Token.objects.get_or_create(user=request.user)
    context = dict(token=token)
    template = loader.get_template('client/index.html')

    return HttpResponse(template.render(context, request))
