
from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework_simplejwt import views as jwt_views

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class AccessToken(serializers.Serializer):
    access = serializers.CharField()


class TokenPair(AccessToken):
    refresh = serializers.CharField()


class TokenObtainPair(jwt_views.TokenObtainPairView):

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
