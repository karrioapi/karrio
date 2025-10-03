import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oauth2_provider.views import TokenView as BaseTokenView

logger = logging.getLogger(__name__)


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
        print(f"CustomTokenView called")
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request POST: {dict(request.POST)}")
        print(f"Request body: {request.body.decode('utf-8') if request.body else 'Empty'}")

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
        print(f"Original grant type after parsing: {original_grant_type}")

        if original_grant_type in grant_type_mapping:
            # Create a mutable copy of the POST data
            post_data = request.POST.copy()
            converted_grant_type = grant_type_mapping[original_grant_type]
            print(f"Converting grant type from '{original_grant_type}' to '{converted_grant_type}'")
            post_data['grant_type'] = converted_grant_type

            # Replace the request POST data
            request.POST = post_data
            request._post = post_data
            print(f"Updated grant type: {request.POST.get('grant_type')}")
        else:
            print(f"No conversion needed for grant type: {original_grant_type}")

        # Call the parent token view with converted grant type
        return super().post(request, *args, **kwargs)
