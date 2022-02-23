from purplship.server.settings.base import *
import os

OIDC_RSA_PRIVATE_KEY = config("OIDC_RSA_PRIVATE_KEY", default="").replace("\\n", "\n")

INSTALLED_APPS += ["oauth2_provider", "purplship.server.iam"]

NAMESPACED_URLS += [
    ("oauth/", "oauth2_provider.urls", "oauth2_provider"),
]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "purplship.server.iam.authentication.OAuth2Authentication",
    *REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"],
)

SESSION_ACCESS_MIXIN = "purplship.server.iam.authentication.AccessMixin"

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
    "SCOPES": {
        "read": "Reading scope",
        "write": "Writing scope",
        "openid": "OpenID connect",
    },
    "OAUTH2_VALIDATOR_CLASS": "purplship.server.iam.oauth_validators.CustomOAuth2Validator",
}
