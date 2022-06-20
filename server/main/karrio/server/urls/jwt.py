from django.urls import path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, exceptions
from rest_framework_simplejwt import views as jwt_views, serializers as jwt
from two_factor.utils import default_device
from django_otp.oath import totp

import karrio.server.conf as conf
import karrio.server.core.utils as utils

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
User = get_user_model()


class AccessToken(serializers.Serializer):
    access = serializers.CharField()


class TokenPair(AccessToken):
    refresh = serializers.CharField()


class TokenObtainPairSerializer(jwt.TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["org_id"] = serializers.CharField(
            required=False,
            help_text="""
            **should be specified only in a multi-org deployment.**

            Note the first org related to the user is selected by default.
            """,
        )

    @classmethod
    def get_token(cls, user, org: str = None):
        token = super().get_token(user)

        # Set is_verified to False if the user has Two Factor enabled
        token["is_verified"] = False if default_device(user) else True

        if hasattr(org, "id"):
            token["org_id"] = org.id

        return token

    def validate(self, attrs):
        if not settings.MULTI_ORGANIZATIONS:
            return super().validate(attrs)

        from karrio.server.orgs.models import Organization

        data = super().validate(attrs)
        org_id = attrs.get("org_id")

        orgs = Organization.objects.filter(users__id=self.user.id)
        self.org = (
            orgs.filter(id=org_id).first()
            if (any(org_id or "") and orgs.filter(id=org_id).exists())
            else orgs.first()
        )

        if self.org is not None and not self.org.is_active:
            raise exceptions.AuthenticationFailed(
                _("Organization is inactive"), code="organization_inactive"
            )

        if self.org is None and any(org_id or ""):
            raise exceptions.AuthenticationFailed(
                _("No active organization found with the given credentials"),
                code="organization_invalid",
            )

        refresh = self.get_token(self.user, self.org)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if jwt.api_settings.UPDATE_LAST_LOGIN:
            jwt.update_last_login(None, self.user)

        # Factor is enabled if False, so we need to send the token to the user
        if not refresh["is_verified"]:
            default_device(self.user).generate_challenge()

        return data


class TokenRefreshSerializer(jwt.TokenRefreshSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["org_id"] = serializers.CharField(
            required=False,
            help_text="""
            **should be specified only in a multi-org deployment.**
            """,
        )

    def validate(self, attrs: dict):
        refresh = jwt.RefreshToken(attrs["refresh"])

        if not refresh["is_verified"]:
            raise exceptions.AuthenticationFailed(
                {"refresh": _("This refresh token is not verified.")},
                code="unverified_refresh_token",
            )

        if settings.MULTI_ORGANIZATIONS and attrs.get("org_id") is not None:
            from karrio.server.orgs.models import Organization

            org = Organization.objects.filter(
                id=attrs.get("org_id"), users__id=refresh.payload["user_id"]
            ).first()

            if org is not None and not org.is_active:
                raise exceptions.AuthenticationFailed(
                    _("Organization is inactive"), code="organization_inactive"
                )

            if org is None:
                raise exceptions.AuthenticationFailed(
                    _("No active organization found with the given credentials"),
                    code="organization_invalid",
                )

            refresh.payload["org_id"] = attrs.get("org_id")

        data = {"access": str(refresh.access_token), "refresh": str(refresh)}

        if jwt.api_settings.ROTATE_REFRESH_TOKENS:
            if jwt.api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)

        return data


class VerifiedTokenObtainPairSerializer(jwt.TokenRefreshSerializer):
    otp_token = serializers.CharField(
        required=True,
        help_text="""
        The OTP (One Time Password) token received by the user from the
        configured Two Factor Authentication method.
        """,
    )

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        user = User.objects.get(id=refresh["user_id"])
        refresh["is_verified"] = self._validate_otp(attrs["otp_token"], user)

        data = {"access": str(refresh.access_token), "refresh": str(refresh)}

        if jwt.api_settings.ROTATE_REFRESH_TOKENS:
            if jwt.api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data

    def _validate_otp(self, otp_token, user) -> bool:
        device = default_device(user)
        if device is None:
            raise exceptions.ValidationError(
                _("Two Factor authentication is not enabled for this user"),
                code="otp_invalid",
            )

        if device.verify_token(otp_token):
            return True

        raise exceptions.ValidationError(
            {"otp_token": _("Invalid or Expired OTP token")}, code="otp_invalid"
        )


class TokenObtainPair(jwt_views.TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["API"],
        operation_id=f"{ENDPOINT_ID}authenticate",
        operation_summary="Obtain auth token pair",
        operation_description="Authenticate the user and return a token pair",
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"
        return response


class TokenRefresh(jwt_views.TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        tags=["API"],
        operation_id=f"{ENDPOINT_ID}refresh_token",
        operation_summary="Refresh auth token",
        operation_description="Authenticate the user and return a token pair",
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"
        return response


class TokenVerify(jwt_views.TokenVerifyView):
    @swagger_auto_schema(
        tags=["API"],
        operation_id=f"{ENDPOINT_ID}verify_token",
        operation_summary="Verify token",
        operation_description="Verify an existent authentication token",
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True)
        },
    )
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"
        return response


class VerifiedTokenPair(jwt_views.TokenVerifyView):
    serializer_class = VerifiedTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["API"],
        operation_id=f"{ENDPOINT_ID}get_verified_token",
        operation_summary="Get verified JWT token",
        operation_description="""
        Get a verified JWT token pair by submitting a Two-Factor authentication code.
        """,
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"
        return response


urlpatterns = [
    path("api/token", TokenObtainPair.as_view(), name="jwt-obtain-pair"),
    path("api/token/refresh", TokenRefresh.as_view(), name="jwt-refresh"),
    path("api/token/verify", TokenVerify.as_view(), name="jwt-verify"),
    path("api/token/verified", VerifiedTokenPair.as_view(), name="verified-jwt-pair"),
]
