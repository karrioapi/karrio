from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self):
        return {
            "name": lambda request: request.user.full_name,
            "email": lambda request: request.user.email,
        }
