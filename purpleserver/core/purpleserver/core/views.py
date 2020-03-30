import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purplship.core.utils import to_dict
from purpleserver.core.serializers import CarrierSettingsList
from purpleserver.core.gateway import get_carriers

logger = logging.getLogger(__name__)
router = DefaultRouter(trailing_slash=False)


@swagger_auto_schema(
    methods=['get'],
    responses={200: CarrierSettingsList()},
    operation_description="""
    GET /v1/carriers?carrier=[carrier]&carrier_name=[carrier_name]&test=[true/false]
    """,
    operation_id="GetConfiguredCarriers",
    manual_parameter=[
        openapi.Parameter(
            'carrier',
            openapi.IN_QUERY,
            description="specific shipping carrier type",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'carrier_name',
            openapi.IN_QUERY,
            description="shipment name",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'test',
            openapi.IN_QUERY,
            description="test mode",
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
def carriers_settings(request):
    try:
        try:
            query = request.query_params
            response = get_carriers(
                carrier_type=query.get('carrier'),
                carrier_name=query.get('carrier_name'),
                test=query.get('test'),
            )
            return Response(to_dict(response), status=status.HTTP_200_OK)
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('carriers', carriers_settings, name='Carriers'))
