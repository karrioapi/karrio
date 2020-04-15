import logging
from typing import List
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purpleserver.core.serializers import CarrierSettingsList
from purpleserver.core.gateway import get_carriers
from purpleserver.core.datatypes import CarrierSettings

logger = logging.getLogger(__name__)
router = DefaultRouter(trailing_slash=False)


@swagger_auto_schema(
    methods=['get'],
    responses={200: CarrierSettingsList()},
    operation_description=("""
    GET /v1/carriers?carrier=[carrier]&test=[true/false]
    
    GET /v1/carriers?carrier_name=[carrierName]
    
    GET /v1/carriers?carrier=[carrier]&carrierName=[carrierName]
    """),
    operation_id="GetConfiguredCarriers",
    manual_parameter=[
        openapi.Parameter(
            'carrier',
            openapi.IN_QUERY,
            description="specific shipping carrier type",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'carrierName',
            openapi.IN_QUERY,
            description="shipment name",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'test',
            openapi.IN_QUERY,
            description="test mode",
            type=openapi.TYPE_BOOLEAN
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
            response: List[CarrierSettings] = get_carriers(
                carrier_type=query.get('carrier'),
                carrier_name=query.get('carrierName'),
                test=query.get('test'),
            )
            carriers = [
                dict(
                    carrier=carrier.carrier,
                    carrier_name=carrier.settings['carrier_name'],
                    test=carrier.settings['test']
                )
                for carrier in response
            ]
            return Response(carriers, status=status.HTTP_200_OK)
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('carriers', carriers_settings, name='Carriers'))
