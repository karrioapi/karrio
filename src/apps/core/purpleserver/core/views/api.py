from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from rest_framework_tracking.mixins import LoggingMixin


class GenericAPIView(LoggingMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
