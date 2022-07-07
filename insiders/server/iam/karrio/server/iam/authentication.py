import functools
from django.utils.functional import SimpleLazyObject
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication as BaseOAuth2Authentication,
)

from karrio.server.core import authentication


class OAuth2Authentication(BaseOAuth2Authentication):
    @authentication.catch_auth_exception
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is not None:
            user, _ = auth

            request.test_mode = authentication.get_request_test_mode(request)
            request.org = SimpleLazyObject(
                functools.partial(
                    authentication.get_request_org,
                    request,
                    user,
                    org_id=request.META.get("HTTP_X_ORG_ID"),
                )
            )

        return auth
