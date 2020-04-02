"""PurplShip Sendle rate mapper module."""

from purplship.core.models import RateRequest
from purplship.core.units import Package
from purplship.core.utils.helpers import concat_str
from purplship.core.errors import RequiredFieldError
from pysendle.quotes import InternationalParcelQuote
from purplship.carriers.sendle.units import Plan, PackagePresets


def international_quote_request(payload: RateRequest) -> InternationalParcelQuote:
    parcel_preset = PackagePresets[payload.parcel.package_preset].value if payload.parcel.package_preset else None
    package = Package(payload.parcel, parcel_preset)

    if package.weight.value is None:
        raise RequiredFieldError("parcel.weight")

    plan = next(
        (Plan[s].value for s in payload.parcel.services if s in Plan.__members__),
        None
    )
    return InternationalParcelQuote(
        pickup_suburb=concat_str(
            payload.shipper.address_line1, payload.shipper.address_line2, join=True
        ),
        pickup_postcode=payload.shipper.postal_code,
        delivery_country=payload.recipient.country_code,
        kilogram_weight=str(package.weight.KG),
        cubic_metre_volume=str(package.volume.value) if package.volume.value else None,
        plan_name=plan,
    )
