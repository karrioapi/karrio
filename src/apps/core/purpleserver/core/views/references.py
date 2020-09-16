from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purpleserver.providers.models import MODELS
from purplship.core.utils import to_dict
from purplship.core.units import Country, Currency, CountryState
from purpleserver.core.router import router

line = "\n"

TYPE_MAPPING = {
    float: 'float',
    str: 'string',
    object: 'object'
}


def import_pkg(pkg: str):
    *_, carrier, name = pkg.split(".")
    if carrier in MODELS.keys():
        return __import__(pkg, fromlist=[name])
    return None


PACKAGE_MAPPERS = {
    'canadapost': {
        'label': "Canada Post",
        'package': import_pkg('purplship.providers.canadapost.units'),
        'services': "ServiceType",
        'options': "OptionCode",
        'packagePresets': "PackagePresets"
    },
    'dhl': {
        'label': "DHL",
        'package': import_pkg('purplship.providers.dhl.units'),
        'services': "Product",
        'options': "SpecialServiceCode",
        'packagePresets': "PackagePresets"
    },
    'fedex': {
        'label': "FedEx",
        'package': import_pkg('purplship.providers.fedex.units'),
        'services': "ServiceType",
        'options': "SpecialServiceType",
        'packagePresets': "PackagePresets"
    },
    'purolator': {
        'label': "Purolator",
        'package': import_pkg('purplship.providers.purolator.units'),
        'services': "Product",
        'options': "Service",
        'packagePresets': "PackagePresets"
    },
    'ups': {
        'label': "UPS",
        'package': import_pkg('purplship.providers.ups.units'),
        'services': "ShippingServiceCode",
        'options': "ServiceOption",
        'packagePresets': "PackagePresets"
    },
    'freightcom': {
        'label': "Freightcom",
        'package': import_pkg('purplship.providers.freightcom.units'),
        'services': "Service",
        'options': "Option",
    },
    'eshipper': {
        'label': "eShipper",
        'package': import_pkg('purplship.providers.eshipper.units'),
        'services': "Service",
        'options': "Option",
    }
}


REFERENCE_MODELS = {
    "countries": {c.name: c.value for c in list(Country)},
    "currencies": {c.name: c.value for c in list(Currency)},
    "states": {c.name: {s.name: s.value for s in list(c.value)} for c in list(CountryState)},
    "services": {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['services']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'services' in mapper and mapper.get('package') is not None
    },
    "options": {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['options']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'options' in mapper and mapper.get('package') is not None
    },
    "packagePresets": {
        key: {c.name: to_dict(c.value) for c in list(getattr(mapper['package'], mapper['packagePresets']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'packagePresets' in mapper and mapper.get('package') is not None
    }
}


MODELS_DOCUMENTATION = f"""
# Countries

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in REFERENCE_MODELS["countries"].items()])}

</details><br/>


# States and Provinces

<details>

{f"{line}".join([f'''
## {Country[key].value}

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["states"].items() 
])}

</details><br/>

# Currencies

<details>

Code | Name 
--- | --- 
{f"{line}".join([f"{code} | {name}" for code, name in REFERENCE_MODELS["currencies"].items()])}

</details><br/>


# Package Preset

<details>

{f"{line}".join([f'''
## {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Dimensions | Note
--- | --- | ---
{f"{line}".join([
    f"{code} | {f' x '.join([str(d) for d in dim.values() if isinstance(d, float)])} | {f' x '.join([k for k in dim.keys() if isinstance(dim[k], float)])}"
    for code, dim in value.items()
])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["packagePresets"].items() 
])}

</details><br/>


# Shipment Options

<details>

{f"{line}".join([f'''
## {PACKAGE_MAPPERS[key]["label"]}

<details>

Code | Identifier
--- | ---
{f"{line}".join([f"{code} | {name}" for code, name in value.items()])}

</details><br/>
'''
for key, value in REFERENCE_MODELS["options"].items() 
])}

</details><br/>


# Shipment Services

<details>

{f"{line}".join([f'''
## {PACKAGE_MAPPERS[key]["label"]}

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


@swagger_auto_schema(
    methods=['get'],
    tags=['Utils'],
    operation_id="all_references",
    operation_summary="Get all References",
    operation_description=MODELS_DOCUMENTATION,
    responses={
        200: openapi.Response(
            schema=openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True),
            description="Data references for countries, currencies, services and more..."
        )
    }
)
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def references(_):
    return Response(REFERENCE_MODELS, status=status.HTTP_200_OK)


router.urls.append(path('references', references))
