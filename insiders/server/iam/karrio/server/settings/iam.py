# type: ignore
from karrio.server.settings.base import *

INSTALLED_APPS += ["oauth2_provider", "karrio.server.iam"]

NAMESPACED_URLS += [
    ("oauth/", "oauth2_provider.urls", "oauth2_provider"),
]

AUTHENTICATION_CLASSES += ["karrio.server.iam.authentication.OAuth2Authentication"]
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "karrio.server.iam.authentication.OAuth2Authentication",
    *REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"],
)

OIDC_RSA_PRIVATE_KEY = config("OIDC_RSA_PRIVATE_KEY", default="").replace("\\n", "\n")
OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth2_provider.Application"
OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": False,
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
    "SCOPES": {
        "read": "Reading scope",
        "write": "Writing scope",
        "openid": "OpenID connect",
    },
    "OAUTH2_VALIDATOR_CLASS": "karrio.server.iam.oauth_validators.CustomOAuth2Validator",
}
