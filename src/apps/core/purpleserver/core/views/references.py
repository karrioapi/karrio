from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purplship.core.units import Country
from purpleserver.core.router import router
from purpleserver.core.serializers import PlainDictField
from purpleserver.core.dataunits import REFERENCE_MODELS, PACKAGE_MAPPERS

line = "\n"

MODELS_DOCUMENTATION = f"""
## Countries

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in REFERENCE_MODELS["countries"].items()])}

</details><br/>


## States and Provinces

<details>

{f"{line}".join([f'''
### {Country[key].value}

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["states"].items() 
])}

</details><br/>

## Currencies

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in REFERENCE_MODELS["currencies"].items()])}

</details><br/>


## Packaging Types

<details>

{f"{line}".join([f'''
### {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Identifier
--- | ---
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["packaging_types"].items() 
])}

</details><br/>


## Package Preset

<details>

{f"{line}".join([f'''
### {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Dimensions | Note
--- | --- | ---
{f"{line}".join([
    f"{code} | {f' x '.join([str(d) for d in dim.values() if isinstance(d, float)])} | {f' x '.join([k for k in dim.keys() if isinstance(dim[k], float)])}"
    for code, dim in value.items()
])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["package_presets"].items() 
])}

</details><br/>


## Shipment Options

<details>

{f"{line}".join([f'''
### {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Identifier
--- | ---
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["options"].items() 
])}

</details><br/>


## Shipment Services

<details>

{f"{line}".join([f'''
### {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Identifier
--- | ---
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["services"].items() 
])}

</details><br/>

"""


class References(Serializer):
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
    tags=['Utils'],
    operation_id="references",
    operation_summary="Data References",
    operation_description=MODELS_DOCUMENTATION,
    responses={200: References()}
)
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def references(_):
    return Response(REFERENCE_MODELS, status=status.HTTP_200_OK)


router.urls.append(path('references', references))
