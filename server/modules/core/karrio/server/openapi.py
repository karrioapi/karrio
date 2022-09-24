from drf_spectacular.types import *
from drf_spectacular.utils import *
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAuthentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.JWTAuthentication'
    name = 'JWTAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT"
        }

class TokenBasicAuthentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.TokenBasicAuthentication'
    name = 'TokenBasicAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Token"
        }

class OAuth2Authentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.OAuth2Authentication'
    name = 'OAuth2Authentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Oauth2"
        }
