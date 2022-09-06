import yaml # type: ignore
import pydoc
import logging
import functools
from django.db.utils import ProgrammingError
from django.conf import settings
from django.contrib.auth import mixins, get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from rest_framework import status
from rest_framework import exceptions
from rest_framework.authentication import (
    TokenAuthentication as BaseTokenAuthentication,
    BasicAuthentication as BaseBasicAuthentication,
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as BaseJWTAuthentication,
)
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication as BaseOAuth2Authentication,
)
from django_otp.middleware import OTPMiddleware

logger = logging.getLogger(__name__)
UserModel = get_user_model()
AUTHENTICATION_CLASSES = getattr(settings, "AUTHENTICATION_CLASSES", [])


def catch_auth_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.AuthenticationFailed:
            from karrio.server.core.exceptions import APIException

            raise APIException(
                "Given token not valid for any token type",
                code="invalid_token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    return wrapper


class TokenAuthentication(BaseTokenAuthentication):
    def get_model(self):
        if self.model is not None:
            return self.model
        from karrio.server.user.models import Token

        return Token

    @catch_auth_exception
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, token = auth
            request.token = token
            request.test_mode = token.test_mode
            request.org = SimpleLazyObject(
                functools.partial(
                    get_request_org,
                    request,
                    user,
                    default_org=token.organization,
                )
            )

        return auth


class TokenBasicAuthentication(BaseBasicAuthentication):
    @catch_auth_exception
    def authenticate(self, request):
        auth = super(TokenBasicAuthentication, self).authenticate(request)

        if auth is not None:
            user, token = auth
            request.token = token
            request.test_mode = token.test_mode
            request.org = SimpleLazyObject(
                functools.partial(
                    get_request_org,
                    request,
                    user,
                    default_org=token.organization,
                )
            )

        return auth

    def authenticate_credentials(self, api_key, *args, **kwargs):
        """
        Authenticate the api token with optional request for context.
        """
        from karrio.server.user.models import Token

        token = Token.objects.filter(key=api_key).first()
        user = getattr(token, "user", None)

        if user is None:
            raise exceptions.AuthenticationFailed(_("Invalid username/password."))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return (user, token)


class JWTAuthentication(BaseJWTAuthentication):
    @catch_auth_exception
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, token = auth

            request.user = user
            request.token = token
            request.test_mode = get_request_test_mode(request)
            request.otp_is_verified = token.get("is_verified") or False
            request.org = SimpleLazyObject(
                functools.partial(
                    get_request_org,
                    request,
                    user,
                    org_id=request.META.get("HTTP_X_ORG_ID"),
                )
            )

            if not token.get("is_verified"):
                raise exceptions.AuthenticationFailed(
                    _("Authentication token not verified"), code="otp_not_verified"
                )

        return auth


class OAuth2Authentication(BaseOAuth2Authentication):
    @catch_auth_exception
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, token = auth

            request.token = token
            request.test_mode = get_request_test_mode(request)
            request.org = SimpleLazyObject(
                functools.partial(
                    get_request_org,
                    request,
                    user,
                    org_id=request.META.get("HTTP_X_ORG_ID"),
                )
            )

        return auth


class TwoFactorAuthenticationMiddleware(OTPMiddleware):
    pass


class AccessMixin(mixins.AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            authenticate_user(request)

        request.user = SimpleLazyObject(
            functools.partial(get_request_user, request, request.user)
        )

        return super().dispatch(request, *args, **kwargs)


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    def process_response(self, request, response):
        if getattr(request, "org", None) is not None:
            response.set_cookie("org_id", getattr(request.org, "id", None))
            response["X-org-id"] = getattr(request.org, "id", None)

        if getattr(request, "test_mode", None) is not None:
            response.set_cookie("test_mode", request.test_mode)
            response["X-test-mode"] = request.test_mode

        return response

    def process_request(self, request):
        super().process_request(request)

        request = authenticate_user(request)

        if hasattr(request, "user") and getattr(request, "org", None) is None:
            request.org = self._get_organization(request)

        if not hasattr(request, "test_mode"):
            request.test_mode = get_request_test_mode(request)

    def _get_organization(self, request):
        """
        Attempts to find and return an organization using the given validated token.
        """
        if settings.MULTI_ORGANIZATIONS:
            try:
                from karrio.server.orgs.models import Organization

                org_id = request.META.get("HTTP_X_ORG_ID")
                orgs = Organization.objects.filter(users__id=request.user.id)
                org = (
                    orgs.filter(id=org_id).first()
                    if org_id is not None
                    else orgs.filter(is_active=True).first()
                )

                # org was found but is not active
                if (org is not None) and (not org.is_active):
                    raise exceptions.AuthenticationFailed(
                        _("Organization is inactive"), code="organization_inactive"
                    )

                return org
            except ProgrammingError:
                pass

        return None


def authenticate_user(request):
    def authenticate(request, authenticator):
        if request.user.is_authenticated is False:
            auth = pydoc.locate(authenticator)().authenticate(request)

            if auth is not None:
                user, token = auth
                request.user = user
                request.token = token

        return request

    try:
        return functools.reduce(authenticate, AUTHENTICATION_CLASSES, request)
    except Exception:
        return request


def get_request_org(request, user, org_id: str = None, default_org=None):
    """
    Attempts to find and return an organization.
    """
    if settings.MULTI_ORGANIZATIONS:
        try:
            from karrio.server.orgs.models import Organization

            if default_org is not None:
                org = default_org

            else:
                orgs = Organization.objects.filter(users__id=user.id)
                org = (
                    orgs.filter(id=org_id).first()
                    if org_id is not None
                    else orgs.filter(is_active=True).first()
                )

            if org is not None and not org.is_active:
                raise exceptions.AuthenticationFailed(
                    _("Organization is inactive"), code="inactive_organization"
                )

            if org is None and org_id is not None:
                raise exceptions.AuthenticationFailed(
                    _("No active organization found with the given credentials"),
                    code="invalid_organization",
                )

            return org
        except ProgrammingError:
            pass

        return None


def get_request_user(request, user):
    if not getattr(request, "otp_is_verified", True):
        raise exceptions.AuthenticationFailed(
            _("Authentication token not verified"), code="otp_not_verified"
        )

    user.otp_device = None
    user.is_verified = functools.partial(
        lambda _: getattr(request, "otp_is_verified", True), user
    )

    return user


def get_request_test_mode(request):
    return yaml.safe_load(request.META.get("HTTP_X_TEST_MODE", "")) or False
