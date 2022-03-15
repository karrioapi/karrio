from django.contrib.auth import mixins
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication as BaseOAuth2Authentication,
)

from karrio.server.core.authentication import (
    JWTAuthentication,
    TokenAuthentication,
    get_request_org,
)


class OAuth2Authentication(BaseOAuth2Authentication):
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, _ = auth

            request.org = get_request_org(request, user)

        return auth


class AccessMixin(mixins.AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        try:
            auth = (
                OAuth2Authentication().authenticate(request)
                or JWTAuthentication().authenticate(request)
                or TokenAuthentication().authenticate(request)
            )

            if auth is not None:
                user, *_ = auth
                request.user = user

        finally:
            return super().dispatch(request, *args, **kwargs)
