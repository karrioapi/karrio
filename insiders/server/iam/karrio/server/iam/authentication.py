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
