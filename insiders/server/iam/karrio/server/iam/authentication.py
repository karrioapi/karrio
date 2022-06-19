import functools
from django.utils.functional import SimpleLazyObject
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication as BaseOAuth2Authentication,
)

from karrio.server.core import authentication


class OAuth2Authentication(BaseOAuth2Authentication):
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, _ = auth
            request.org = SimpleLazyObject(
                functools.partial(authentication.get_request_org, request, user)
            )

        return auth


class AccessMixin(authentication.AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                auth = OAuth2Authentication().authenticate(request)

                if auth is not None:
                    user, *_ = auth
                    request.user = user

        finally:
            return super().dispatch(request, *args, **kwargs)
