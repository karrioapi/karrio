from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer

from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from purpleserver.providers.models import MODELS
from purplship.core.utils import to_dict
import purplship.core.units
from purplship.core.units import Country, Currency, CountryState, PaymentType
from purpleserver.core.router import router
from purpleserver.core.serializers import PlainDictField, CustomsContentType, Incoterm

line = "\n"

TYPE_MAPPING = {
    float: 'float',
    str: 'string',
    object: 'object'
}


def import_pkg(pkg: str):
    *_, carrier, name = pkg.split(".")
    if any(model_name for model_name in MODELS.keys() if carrier in model_name):
        return __import__(pkg, fromlist=[name])
    return None


PACKAGE_MAPPERS = {
    'universal': {
        'label': "Multi-carrier (purplship)",
        'package': purplship.core.units,
        'packaging_types': "PackagingUnit"
    },
    'canadapost': {
        'label': "Canada Post",
        'package': import_pkg('purplship.providers.canadapost.units'),
        'services': "ServiceType",
        'options': "OptionCode",
        'package_presets': "PackagePresets",
    },
    'dhl_express': {
        'label': "DHL Express",
        'package': import_pkg('purplship.providers.dhl_express.units'),
        'services': "Product",
        'options': "SpecialServiceCode",
        'package_presets': "PackagePresets",
        'packaging_types': "DCTPackageType"
    },
    'fedex_express': {
        'label': "FedEx Express",
        'package': import_pkg('purplship.providers.fedex.units'),
        'services': "ServiceType",
        'options': "SpecialServiceType",
        'package_presets': "PackagePresets",
        'packaging_types': "PackagingType"
    },
    'purolator_courier': {
        'label': "Purolator Courier",
        'package': import_pkg('purplship.providers.purolator.units'),
        'services': "Product",
        'options': "Service",
        'package_presets': "PackagePresets",
        'packaging_types': "PackagingType"
    },
    'ups_package': {
        'label': "UPS Package",
        'package': import_pkg('purplship.providers.ups.units'),
        'services': "ShippingServiceCode",
        'options': "ServiceOption",
        'package_presets': "PackagePresets",
        'packaging_types': "RatingPackagingType"
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
    "carriers": {k: v['label'] for k, v in PACKAGE_MAPPERS.items() if k in MODELS},
    "payment_types": {c.name: c.value for c in list(PaymentType)},
    "incoterms": {c.name: c.value for c in list(Incoterm)},
    "customs_content_type": {c.name: c.value for c in list(CustomsContentType)},
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
    "packaging_types": {
        key: {c.name: c.value for c in list(getattr(mapper['package'], mapper['packaging_types']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'packaging_types' in mapper and mapper.get('package') is not None
    },
    "package_presets": {
        key: {c.name: to_dict(c.value) for c in list(getattr(mapper['package'], mapper['package_presets']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'package_presets' in mapper and mapper.get('package') is not None
    }
}

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
