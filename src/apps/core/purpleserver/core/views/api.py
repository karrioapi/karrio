from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog
from purplship.core.utils import jsonify


class PurplshipLoggingMixin(LoggingMixin):
    def handle_log(self):
        data = (
            None if 'data' not in self.log else
            jsonify(self.log['data'])
        )
        query_params = (
            None if 'query_params' not in self.log else
            jsonify(self.log['query_params'])
        )

        APIRequestLog(**{
            **self.log,
            'data': data,
            'query_params': query_params
        }).save()


class BaseView:
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]


class BaseGenericAPIView(generics.GenericAPIView, BaseView):
    pass


class GenericAPIView(PurplshipLoggingMixin, BaseGenericAPIView):
    pass


class APIView(views.APIView, PurplshipLoggingMixin, BaseView):
    pass
