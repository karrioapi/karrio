import logging

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import CarrierSettings
from purpleserver.providers.serializers import CarrierSerializer

logger = logging.getLogger(__name__)


class ConnectionList(GenericAPIView):
    swagger_schema = None
    logging_methods = []
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = LimitOffsetPagination
    default_limit = 20

    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        connections = request.user.carrier_set.all().order_by('-created_at')
        response = self.paginate_queryset([connection.data.__dict__ for connection in connections])
        return self.get_paginated_response(response)

    def post(self, request: Request):
        """
        Connect a carrier account.
        """
        connection = SerializerDecorator[CarrierSerializer](data=request.data).save(user=request.user).instance
        return Response(CarrierSettings(connection).data, status=status.HTTP_201_CREATED)


class ConnectionDetails(GenericAPIView):
    swagger_schema = None
    logging_methods = []
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def patch(self, request: Request, pk: str):
        """
        Update a carrier connection details.
        """
        connection = request.user.carrier_set.get(pk=pk)

        SerializerDecorator[CarrierSerializer](connection, data=request.data).save()
        return Response(connection.data.__dict__)

    def delete(self, request: Request, pk: str):
        """
        Disconnect a carrier connection.
        """
        carrier = request.user.carrier_set.get(pk=pk)
        carrier.delete()
        return Response(dict(success=True, message="Carrier successfully disconnected."))
