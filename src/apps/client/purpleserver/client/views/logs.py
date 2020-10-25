import json
from more_itertools import unique_everseen
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_tracking.models import APIRequestLog

from purpleserver.core.views.api import BaseGenericAPIView
from purpleserver.core.serializers import Shipment


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIRequestLog
        exclude = ['user']


class LogsAPI(BaseGenericAPIView):
    swagger_schema = None
    pagination_class = LimitOffsetPagination
    default_limit = 20

    def get(self, request: Request):
        logs = request.user.apirequestlog_set.all().order_by('-requested_at')
        response = self.paginate_queryset(LogSerializer(logs, many=True).data)
        return self.get_paginated_response(response)


class LogDetailsAPI(BaseGenericAPIView):
    swagger_schema = None

    def get(self, request: Request, log_id: str):
        log = request.user.apirequestlog_set.get(id=log_id)
        return Response(LogSerializer(log).data)


class ShipmentsLogsAPI(LogsAPI):

    def get(self, request: Request):
        logs = request.user.apirequestlog_set.filter(
            Q(path__in=['/v1/proxy/shipping', '/v1/shipments']) |
            Q(path__startswith='/v1/shipments', path__endswith='/rates') |
            Q(path__startswith='/v1/shipments', path__endswith='/options') |
            Q(path__startswith='/v1/shipments', path__endswith='/purchase'),
            Q(status_code__in=[200, 201]),
            Q(method='POST')
        ).order_by('-requested_at').values('response')

        def get_shipment(response: dict):
            return response.get('shipment', response)

        shipments = unique_everseen([
            get_shipment(json.loads(log['response']))
            for log in logs
        ], key=lambda s: s['id'])
        response = self.paginate_queryset(Shipment(shipments, many=True).data)
        return self.get_paginated_response(response)
