from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class TokenAPI(ObtainAuthToken):
    swagger_schema = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def put(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token_exists = Token.objects.filter(user=user).exists()

        if token_exists is False:
            return self.post(request, *args, **kwargs)

        user.auth_token.delete()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})