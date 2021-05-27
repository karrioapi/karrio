import importlib
from django.urls import path
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, exceptions
from rest_framework_simplejwt import views as jwt_views, serializers as jwt

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class AccessToken(serializers.Serializer):
    access = serializers.CharField()


class TokenPair(AccessToken):
    refresh = serializers.CharField()


class TokenObtainPairSerializer(jwt.TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['org_id'] = serializers.CharField(
            required=False, help_text="""
            **should be specified only in a multi-org deployment.**
            
            Note the first org related to the user is selected by default.
            """)

    @classmethod
    def get_token(cls, user, org = None):
        token = super().get_token(user)

        if hasattr(org, 'id'):
            token['org_id'] = org.id

        return token

    def validate(self, attrs):

        if importlib.util.find_spec('purpleserver.orgs') is None:
            return super().validate(attrs)

        from purpleserver.orgs.models import Organization

        data = super(jwt.TokenObtainPairSerializer, self).validate(attrs)
        org_id = attrs.get('org_id')

        orgs = Organization.objects.filter(users__id=self.user.id)
        self.org = orgs.filter(id=org_id).first() if any(org_id or '') else orgs.first()

        if self.org is not None and not self.org.is_active:
            raise exceptions.AuthenticationFailed(_('Organization is inactive'), code='organization_inactive')

        if self.org is None and any(org_id or ''):
            raise exceptions.AuthenticationFailed(
                _('No active organization found with the given credentials'), code='organization_invalid')

        refresh = self.get_token(self.user, self.org)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if jwt.api_settings.UPDATE_LAST_LOGIN:
            jwt.update_last_login(None, self.user)

        return data


class TokenObtainPair(jwt_views.TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        tags=['API'],
        operation_id=f"{ENDPOINT_ID}authenticate",
        operation_summary="Obtain auth token pair",
        operation_description="Authenticate the user and return a token pair",
        responses={201: TokenPair()}
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class TokenRefresh(jwt_views.TokenRefreshView):

    @swagger_auto_schema(
        tags=['API'],
        operation_id=f"{ENDPOINT_ID}refresh_token",
        operation_summary="Refresh auth token",
        operation_description="Authenticate the user and return a token pair",
        responses={200: AccessToken()}
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class TokenVerify(jwt_views.TokenVerifyView):

    @swagger_auto_schema(
        tags=['API'],
        operation_id=f"{ENDPOINT_ID}verify_token",
        operation_summary="Verify auth token",
        operation_description="Verify an existent authentication token",
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True)}
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


urlpatterns = [
    path('api/token', TokenObtainPair.as_view(), name='jwt-obtain-pair'),
    path('api/token/refresh', TokenRefresh.as_view(), name='jwt-refresh'),
    path('api/token/verify', TokenVerify.as_view(), name='jwt-verify'),
]
