from django.urls import path
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import serializers, exceptions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views, serializers as jwt
from two_factor.utils import default_device

import karrio.server.openapi as openapi

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
User = get_user_model()


# --- Cookie helpers (shared by all JWT views) ---

def get_cookie_config(include_max_age=True):
    """Build cookie configuration from Django settings."""
    config = dict(
        access_cookie_name=getattr(settings, "JWT_AUTH_COOKIE", "karrio_access_token"),
        refresh_cookie_name=getattr(settings, "JWT_REFRESH_COOKIE", "karrio_refresh_token"),
        secure=getattr(settings, "JWT_AUTH_COOKIE_SECURE", getattr(settings, "USE_HTTPS", False)),
        samesite=getattr(settings, "JWT_AUTH_COOKIE_SAMESITE", "Lax"),
        path=getattr(settings, "JWT_AUTH_COOKIE_PATH", "/"),
    )

    if include_max_age:
        jwt_config = getattr(settings, "SIMPLE_JWT", {})
        access_lifetime = jwt_config.get("ACCESS_TOKEN_LIFETIME")
        refresh_lifetime = jwt_config.get("REFRESH_TOKEN_LIFETIME")
        config.update(
            access_max_age=int(access_lifetime.total_seconds()) if access_lifetime else 1800,
            refresh_max_age=int(refresh_lifetime.total_seconds()) if refresh_lifetime else 259200,
        )

    return config


def set_auth_cookies(response, access_token, refresh_token):
    """Set HTTP-only cookies for access and refresh tokens on the response."""
    config = get_cookie_config()

    response.set_cookie(
        config["access_cookie_name"],
        access_token,
        max_age=config["access_max_age"],
        httponly=True,
        secure=config["secure"],
        samesite=config["samesite"],
        path=config["path"],
    )
    response.set_cookie(
        config["refresh_cookie_name"],
        refresh_token,
        max_age=config["refresh_max_age"],
        httponly=True,
        secure=config["secure"],
        samesite=config["samesite"],
        path=config["path"],
    )


def clear_auth_cookies(response):
    """Clear HTTP-only auth cookies by expiring them immediately."""
    config = get_cookie_config(include_max_age=False)

    for cookie_name in [config["access_cookie_name"], config["refresh_cookie_name"]]:
        response.set_cookie(
            cookie_name,
            "",
            max_age=0,
            httponly=True,
            secure=config["secure"],
            samesite=config["samesite"],
            path=config["path"],
        )


def get_refresh_token(request):
    """Get refresh token from cookie, falling back to request body."""
    cookie_name = getattr(settings, "JWT_REFRESH_COOKIE", "karrio_refresh_token")
    refresh_token = (
        request.COOKIES.get(cookie_name)
        or request.data.get("refresh")
    )

    if not refresh_token:
        raise exceptions.ValidationError(
            {"refresh": _("Refresh token is required.")}
        )

    return refresh_token


def _build_token_response(access_token, refresh_token):
    """Build a 201 token pair response with no-cache headers."""
    response = Response(
        {"access": access_token, "refresh": refresh_token},
        status=status.HTTP_201_CREATED,
    )
    response["Cache-Control"] = "no-store"
    response["CDN-Cache-Control"] = "no-store"
    return response


# --- Serializers ---

class AccessToken(serializers.Serializer):
    access = serializers.CharField()


class TokenPair(AccessToken):
    refresh = serializers.CharField()


class TokenObtainPairSerializer(jwt.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Set is_verified to False if the user has Two Factor enabled and confirmed
        token["is_verified"] = False if default_device(user) else True

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if jwt.api_settings.UPDATE_LAST_LOGIN:
            jwt.update_last_login(None, self.user)

        # Multi Factor is enabled if False, so we need to send the token to the user
        if not refresh["is_verified"]:
            default_device(self.user).generate_challenge()

        return data


class TokenRefreshSerializer(jwt.TokenRefreshSerializer):
    def validate(self, attrs: dict):
        refresh_token = attrs.get("refresh")
        if not refresh_token:
            raise exceptions.ValidationError(
                {"refresh": _("Refresh token is required.")}
            )

        refresh = jwt.RefreshToken(refresh_token)

        if not refresh["is_verified"]:
            raise exceptions.AuthenticationFailed(
                {"refresh": _("This refresh token is not verified.")},
                code="unverified_refresh_token",
            )

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
        help_text="""The OTP (One Time Password) token received by the user from the
        configured Two Factor Authentication method.
        """,
    )

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        if not refresh_token:
            raise exceptions.ValidationError(
                {"refresh": _("Refresh token is required.")}
            )

        refresh = self.token_class(refresh_token)
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


# --- Views ---

class TokenObtainPair(jwt_views.TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    @openapi.extend_schema(
        auth=[],
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}authenticate",
        summary="Obtain auth token pair",
        description="Authenticate the user and return a token pair. Tokens are stored in HTTP-only cookies.",
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        response = _build_token_response(data["access"], data["refresh"])
        set_auth_cookies(response, data["access"], data["refresh"])

        return response


class TokenRefresh(jwt_views.TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @openapi.extend_schema(
        auth=[],
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}refresh_token",
        summary="Refresh auth token",
        description="Refresh the authentication token. Tokens are stored in HTTP-only cookies.",
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        refresh_token = get_refresh_token(self.request)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        access = data["access"]
        refresh = data.get("refresh")

        response = _build_token_response(access, refresh or refresh_token)
        if refresh is not None:
            set_auth_cookies(response, access, refresh)

        return response


class TokenVerify(jwt_views.TokenVerifyView):

    @openapi.extend_schema(
        auth=[],
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}verify_token",
        summary="Verify token",
        description="Verify an existent authentication token",
        responses={200: openapi.OpenApiTypes.OBJECT},
    )
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"
        return response


class VerifiedTokenPair(jwt_views.TokenVerifyView):
    serializer_class = VerifiedTokenObtainPairSerializer

    @openapi.extend_schema(
        auth=[],
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}get_verified_token",
        summary="Get verified JWT token",
        description="Get a verified JWT token pair by submitting a Two-Factor authentication code. Tokens are stored in HTTP-only cookies.",
        responses={201: TokenPair()},
    )
    def post(self, *args, **kwargs):
        refresh_token = get_refresh_token(self.request)

        serializer = self.get_serializer(data={
            "refresh": refresh_token,
            "otp_token": self.request.data.get("otp_token"),
        })
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        access = data["access"]
        refresh = data.get("refresh")

        response = _build_token_response(access, refresh or refresh_token)
        if refresh is not None:
            set_auth_cookies(response, access, refresh)

        return response


class LogoutView(jwt_views.TokenVerifyView):
    """Logout view that clears HTTP-only auth cookies."""
    permission_classes = [AllowAny]

    @openapi.extend_schema(
        auth=[],
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}logout",
        summary="Logout",
        description="Clear authentication cookies and logout the user. Accessible without authentication.",
        responses={200: openapi.OpenApiTypes.OBJECT},
    )
    def post(self, *args, **kwargs):
        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )

        clear_auth_cookies(response)

        response["Cache-Control"] = "no-store"
        response["CDN-Cache-Control"] = "no-store"

        return response


urlpatterns = [
    path("api/token", TokenObtainPair.as_view(), name="jwt-obtain-pair"),
    path("api/token/refresh", TokenRefresh.as_view(), name="jwt-refresh"),
    path("api/token/verify", TokenVerify.as_view(), name="jwt-verify"),
    path("api/token/verified", VerifiedTokenPair.as_view(), name="verified-jwt-pair"),
    path("api/logout", LogoutView.as_view(), name="jwt-logout"),
]
