from typing import Type
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.models import Insurance, COD, Notification
from purpleserver.core.router import router


TYPE_MAPPING = {
    float: 'float',
    str: 'string',
    object: 'object'
}


def format_type(data: Type):
    type_name = data.__name__ if hasattr(data, '__name__') else data
    props = [f"{type_name} | {TYPE_MAPPING.get(type(data), 'object')}"]
    if hasattr(data, '__annotations__'):
        for prop_, type_ in data.__annotations__.items():
            props.append(f"{data.__name__}.{prop_} | {TYPE_MAPPING.get(type_)}")

    return "\n".join(props)


MODELS_DOCUMENTATION = f"""
### Shipment Options

Name | Type | Description
--- | --- | ---
{format_type(Insurance)}
{format_type(COD)}
{format_type(Notification)}
{format_type('printing')}

"""


@swagger_auto_schema(
    methods=['get'],
    tags=['REFERENCE'],
    operation_description=MODELS_DOCUMENTATION,
    operation_id="Reference",
)
@api_view(['GET'])
def references(_):
    return Response({}, status=status.HTTP_200_OK)


router.urls.append(path('reference', references, name='Reference'))
