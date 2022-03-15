import importlib
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_tracking.mixins import LoggingMixin

from karrio.core.utils import DP
from karrio.server.core.authentication import TokenAuthentication, JWTAuthentication
from karrio.server.core.models import APILog


class KarrioLoggingMixin(LoggingMixin):
    def handle_log(self):
        data = None if "data" not in self.log else DP.jsonify(self.log["data"])
        query_params = (
            None
            if "query_params" not in self.log
            else DP.jsonify(self.log["query_params"])
        )
        response = None if "response" not in self.log else DP.jsonify(self.log["response"])

        log = APILog(**{
            **self.log,
            "data": data,
            "response": response,
            "query_params": query_params
        })
        log.save()

        if (importlib.util.find_spec("karrio.server.orgs") is not None) and (
            getattr(self.request, "org", None) is not None
        ):
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
        if hasattr(self, "model") and getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return self.model.objects.none()

        if hasattr(self, "model") and hasattr(self.model, "access_by"):
            return self.model.access_by(self.request)

        return getattr(self, "queryset", None)


class GenericAPIView(KarrioLoggingMixin, BaseGenericAPIView):
    logging_methods = ["POST", "PUT", "PATCH", "DELETE"]


class APIView(KarrioLoggingMixin, views.APIView, BaseView):
    logging_methods = ["POST", "PUT", "PATCH", "DELETE"]
