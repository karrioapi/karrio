from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class TokenAPI(ObtainAuthToken):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token_exists = Token.objects.filter(user=user).exists()

        if token_exists is False:
            return self.post(request, *args, **kwargs)

        user.auth_token.delete()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


@login_required(login_url='/login')
def index(request: Request):
    token, created = Token.objects.get_or_create(user=request.user)
    context = dict(token=token)
    template = loader.get_template('client/index.html')

    return HttpResponse(template.render(context, request))
