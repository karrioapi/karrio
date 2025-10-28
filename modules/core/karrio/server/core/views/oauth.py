from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oauth2_provider.views import TokenView as BaseTokenView
from karrio.server.core.logging import logger


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenView(BaseTokenView):
    """
    Custom OAuth2 token view that handles grant type format conversion.

    django-oauth-toolkit stores grant types with hyphens (e.g., 'authorization-code')
    but OAuth2 spec uses underscores (e.g., 'authorization_code').
    This view converts the format before processing.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle token requests with grant type conversion.
        """
        logger.debug("CustomTokenView called")
        logger.debug("Processing token request",
                    method=request.method,
                    content_type=request.content_type,
                    post_data=dict(request.POST),
                    body=request.body.decode('utf-8') if request.body else 'Empty')

        # Parse the request body if POST data is empty
        if not request.POST and request.body:
            from django.http import QueryDict
            import urllib.parse

            # Parse the form data from the request body
            body_data = urllib.parse.parse_qs(request.body.decode('utf-8'))
            # Convert to single values (parse_qs returns lists)
            parsed_data = {k: v[0] if v else '' for k, v in body_data.items()}

            # Create a QueryDict from the parsed data
            post_data = QueryDict('', mutable=True)
            for key, value in parsed_data.items():
                post_data[key] = value

            # Replace the request POST data
            request.POST = post_data
            request._post = post_data

        # Convert OAuth2 spec grant types to django-oauth-toolkit format
        grant_type_mapping = {
            'authorization_code': 'authorization-code',
            'client_credentials': 'client-credentials',
            'refresh_token': 'refresh-token',
            'password': 'password',
        }

        original_grant_type = request.POST.get('grant_type')
        logger.debug("Grant type parsed", grant_type=original_grant_type)

        if original_grant_type in grant_type_mapping:
            # Create a mutable copy of the POST data
            post_data = request.POST.copy()
            converted_grant_type = grant_type_mapping[original_grant_type]
            logger.debug("Converting grant type",
                        original=original_grant_type,
                        converted=converted_grant_type)
            post_data['grant_type'] = converted_grant_type

            # Replace the request POST data
            request.POST = post_data
            request._post = post_data
            logger.debug("Grant type updated", grant_type=request.POST.get('grant_type'))
        else:
            logger.debug("No grant type conversion needed", grant_type=original_grant_type)

        # Call the parent token view with converted grant type
        return super().post(request, *args, **kwargs)
