import purplship.core.units
from purplship.core.utils import DP
from purplship.core.units import Country, Currency, CountryState, PaymentType

from purpleserver.providers.models import MODELS
from purpleserver.core.serializers import CustomsContentType, Incoterm


def import_pkg(pkg: str):
    *_, carrier, name = pkg.split(".")
    if any(model_name for model_name in MODELS.keys() if carrier in model_name):
        return __import__(pkg, fromlist=[name])
    return None


TYPE_MAPPING = {
    float: 'float',
    str: 'string',
    object: 'object'
}

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
        key: {c.name: DP.to_dict(c.value) for c in list(getattr(mapper['package'], mapper['package_presets']))}
        for key, mapper in PACKAGE_MAPPERS.items()
        if 'package_presets' in mapper and mapper.get('package') is not None
    }
}
