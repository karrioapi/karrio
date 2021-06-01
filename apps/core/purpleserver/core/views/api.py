import importlib
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_tracking.mixins import LoggingMixin

from purplship.core.utils import DP
from purpleserver.core.authentication import TokenAuthentication, JWTAuthentication
from purpleserver.core.models import APILog


class PurplshipLoggingMixin(LoggingMixin):
    def handle_log(self):
        data = (
            None if 'data' not in self.log else
            DP.jsonify(self.log['data'])
        )
        query_params = (
            None if 'query_params' not in self.log else
            DP.jsonify(self.log['query_params'])
        )

        log = APILog(**{
            **self.log,
            'data': data,
            'query_params': query_params
        })
        log.save()

        if ((importlib.util.find_spec('purpleserver.orgs') is not None) and (getattr(self.request, 'org', None) is not None)):
            log.link = log.__class__.link.related.related_model.objects.create(
                org=self.request.org, item=log
            )
            log.save()


class BaseView:
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [TokenAuthentication, JWTAuthentication]


class BaseGenericAPIView(generics.GenericAPIView, BaseView):
    def get_queryset(self):
        if (self.model is not None) and (getattr(self.model, 'access_by', None) is not None):
            return self.model.access_by(self.request)

        return None


class GenericAPIView(PurplshipLoggingMixin, BaseGenericAPIView):
    logging_methods = ['POST', 'PUT', 'PATCH', 'DELETE']


class APIView(PurplshipLoggingMixin, views.APIView, BaseView):
    logging_methods = ['POST', 'PUT', 'PATCH', 'DELETE']
