from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.router import router
from purpleserver.core.serializers import PlainDictField, CharField
from purpleserver.core.dataunits import REFERENCE_MODELS

ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class References(Serializer):
    APP_NAME = CharField()
    APP_VERSION = CharField()

    countries = PlainDictField()
    currencies = PlainDictField()
    carriers = PlainDictField()
    customs_content_type = PlainDictField()
    incoterms = PlainDictField()
    states = PlainDictField()
    services = PlainDictField()
    options = PlainDictField()
    package_presets = PlainDictField()
    packaging_types = PlainDictField()
    payment_types = PlainDictField()


@swagger_auto_schema(
    methods=['get'],
    tags=['API'],
    operation_id=f"{ENDPOINT_ID}data",
    operation_summary="Data References",
    responses={200: References()}
)
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def references(_):
    return Response(REFERENCE_MODELS, status=status.HTTP_200_OK)


router.urls.append(path('references', references))
