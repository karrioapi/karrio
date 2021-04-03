"""
purplship server graph module urls
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from graphene_django.views import GraphQLView


class CustomJWTAuthMixin(LoginRequiredMixin, JWTAuthentication):
    def dispatch(self, request, *args, **kwargs):
        try:
            user, *_ = self.authenticate(request)
            request.user = user

            return super(AccessMixin, self).dispatch(request, *args, **kwargs)
        except:
            return super().dispatch(request, *args, **kwargs)


class PurplshipGraphQLView(CustomJWTAuthMixin, GraphQLView):
    pass


app_name = 'purpleserver.graph'
urlpatterns = [
    path("graphql", csrf_exempt(PurplshipGraphQLView.as_view(graphiql=True))),
]
