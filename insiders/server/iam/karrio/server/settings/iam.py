from karrio.server.settings.base import *

OIDC_RSA_PRIVATE_KEY = config("OIDC_RSA_PRIVATE_KEY", default="").replace("\\n", "\n")

INSTALLED_APPS += ["oauth2_provider", "karrio.server.iam"]

NAMESPACED_URLS += [
    ("oauth/", "oauth2_provider.urls", "oauth2_provider"),
]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "karrio.server.iam.authentication.OAuth2Authentication",
    *REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"],
)

AUTHENTICATION_METHODS += ["karrio.server.iam.authentication.OAuth2Authentication"]
OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth2_provider.Application"

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
    "SCOPES": {
        "read": "Reading scope",
        "write": "Writing scope",
        "openid": "OpenID connect",
    },
    "OAUTH2_VALIDATOR_CLASS": "karrio.server.iam.oauth_validators.CustomOAuth2Validator",
}
