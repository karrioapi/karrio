import logging
from django.urls import path

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.serializers import Operation
from purpleserver.client.serializers import TemplateSerializer

logger = logging.getLogger(__name__)


class TemplateList(GenericAPIView):
    swagger_schema = None
    logging_methods = []
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = LimitOffsetPagination
    default_limit = 20

    def post(self, request: Request):
        """
        Create a new template.
        """
        template = SerializerDecorator[TemplateSerializer](data=request.data).save(user=request.user).instance
        return Response(TemplateSerializer(template).data, status=status.HTTP_201_CREATED)


class TemplateDetails(TemplateList):

    def patch(self, request: Request, pk: str):
        """
        Update a template.
        """
        template = request.user.template_set.get(pk=pk)
        SerializerDecorator[TemplateSerializer](template, data=request.data).save(user=request.user)

        return Response(TemplateSerializer(template).data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, pk: str):
        """
        Remove a template.
        """
        template = request.user.template_set.get(pk=pk)
        template.delete()
        serializer = Operation(dict(operation="Remove template", success=True))

        return Response(serializer.data)


class CustomsTemplateList(TemplateList):

    def get(self, request: Request):
        """
        Returns the list of customs info templates
        """
        templates = request.user.template_set.filter(customs__isnull=False).order_by('-created_at')
        response = self.paginate_queryset(TemplateSerializer(templates, many=True).data)

        return self.get_paginated_response(response)


class AddressTemplateList(TemplateList):

    def get(self, request: Request):
        """
        Returns the list of address templates
        """
        templates = request.user.template_set.filter(address__isnull=False).order_by('-created_at')
        response = self.paginate_queryset(TemplateSerializer(templates, many=True).data)

        return self.get_paginated_response(response)


class ParcelTemplateList(TemplateList):

    def get(self, request: Request):
        """
        Returns the list of parcel templates
        """
        templates = request.user.template_set.filter(parcel__isnull=False).order_by('-created_at')
        response = self.paginate_queryset(TemplateSerializer(templates, many=True).data)

        return self.get_paginated_response(response)


templates_urlpatterns = [
    path('templates', TemplateList.as_view(), name='templates'),
    path('templates/<str:pk>', TemplateDetails.as_view(), name='templates-details'),
    path('parcels/templates', ParcelTemplateList.as_view(), name='parcel_templates'),
    path('addresses/templates', AddressTemplateList.as_view(), name='address_templates'),
    path('customs_infos/templates', CustomsTemplateList.as_view(), name='customs_info_templates'),
]
