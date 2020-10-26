from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from purpleserver.core.utils import SerializerDecorator

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'is_staff']
        read_only_fields = ['is_staff']

    def update(self, instance: User, validated_data: dict) -> User:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    swagger_schema = None

    def get(self, request: Request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request: Request):
        user = SerializerDecorator[UserSerializer](request.user, data=request.data).save().instance
        return Response(UserSerializer(user).data)

    def delete(self, request: Request):
        request.user.is_active = False
        request.user.save()
        return Response({"message": "account deactivated"})
