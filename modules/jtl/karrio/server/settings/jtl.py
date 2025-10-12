"""
JTL Hub SSO Settings

This module provides JTL Hub-specific configuration and middleware setup.
It extends the base Karrio settings with JTL Hub OAuth authentication.
"""

# Ensure JTL Hub authentication is always first
# This prioritizes JTL Hub SSO for all authentication attempts
if "karrio.server.jtl.authentication.JTLHubAuthentication" not in AUTHENTICATION_CLASSES:
    AUTHENTICATION_CLASSES.insert(0, "karrio.server.jtl.authentication.JTLHubAuthentication")

# JTL Hub Feature Flags
JTL_HUB_SSO_ENABLED = True
JTL_HUB_AUTO_PROVISION_USERS = True
JTL_HUB_AUTO_PROVISION_ORGS = True

# JTL Hub JWKS Configuration (for dynamic key fetching)
# These defaults point to production; override via environment variables for other environments
JTL_HUB_JWKS_URL = config(
    "JTL_HUB_JWKS_URL",
    default="https://auth.jtl-cloud.com/.well-known/jwks.json"
)
JTL_HUB_ISSUER = config(
    "JTL_HUB_ISSUER",
    default="https://auth.jtl-cloud.com"
)

# Logging configuration for JTL Hub
LOGGING["loggers"]["karrio.server.jtl"] = {
    "handlers": ["file", "console"],
    "level": LOG_LEVEL,
    "propagate": False,
}
