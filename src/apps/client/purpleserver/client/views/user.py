from purpleserver.core.utils import SerializerDecorator
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer, CharField
from django.conf import settings


class UserSerializer(Serializer):
    first_name = CharField(required=False)
    email = CharField(required=False)
    username = CharField(required=False)

    def update(self, instance: settings.AUTH_USER_MODEL, validated_data: dict) -> settings.AUTH_USER_MODEL:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request: Request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request: Request):
        user = SerializerDecorator[UserSerializer](request.user, data=request.data).save().instance
        return Response(UserSerializer(user).data)

    def delete(self, request: Request):
        request.user.is_active = False
        request.user.save()
        return Response({"message": "account deactivated"})
