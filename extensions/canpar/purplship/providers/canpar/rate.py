from typing import List, Tuple, Optional
from pycanpar.CanparRatingService import (
    rateShipment,
    RateShipmentRq,
    Shipment,
    Package,
    Address,
)
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message
)
from purplship.core.units import Packages
from purplship.core.utils import Serializable, Envelope, create_envelope, Element
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer
from purplship.providers.canpar.units import WeightUnit, DimensionUnit, Option, Service


def parse_rate_shipment_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    rates = []
    return rates, parse_error_response(response, settings)


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    extra_charges = []

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=None,
        transit_days=None,
        service=None,
        discount=None,
        base_charge=None,
        total_charge=None,
        duties_and_taxes=None,
        extra_charges=extra_charges,
    )


def rate_shipment_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels)
    service_type: Optional[str] = next(
        (Service[key].value for key in payload.services if key in Service.__members__),
        None
    )
    options = {
        Option[key].name: Option[key].value for key in payload.options.keys()
        if key in Option.__members__
    }
    premium: Optional[bool] = next((True for option in options.keys() if option in [
        Option.canpar_ten_am.value,
        Option.canpar_noon.value,
        Option.canpar_saturday.value,
    ]), None)

    request = create_envelope(
        body_content=rateShipment(
            request=RateShipmentRq(
                apply_association_discount=False,
                apply_individual_discount=False,
                apply_invoice_discount=False,
                password=settings.password,
                shipment=Shipment(
                    cod_type=options.get('canpar_cash_on_delivery'),
                    delivery_address=Address(
                        address_line_1=payload.recipient.address_line1,
                        address_line_2=payload.recipient.address_line2,
                        address_line_3=None,
                        attention=payload.recipient.person_name,
                        city=payload.recipient.city,
                        country=payload.recipient.country_code,
                        email=payload.recipient.email,
                        extension=None,
                        name=payload.recipient.company_name,
                        phone=payload.recipient.phone_number,
                        postal_code=payload.recipient.postal_code,
                        province=payload.recipient.state_code,
                        residential=payload.recipient.residential,
                    ),
                    description=None,
                    dg=options.get('canpar_dangerous_goods'),
                    dimention_unit=DimensionUnit.IN.value,
                    handling=None,
                    handling_type=None,
                    instruction=None,
                    nsr=(
                        options.get('canpar_no_signature_required') or options.get('canpar_not_no_signature_required')
                    ),
                    packages=[
                        Package(
                            alternative_reference=None,
                            cod=None,
                            cost_centre=None,
                            declared_value=None,
                            height=pkg.height.CM,
                            length=pkg.length.CM,
                            lg=None,
                            reference=None,
                            reported_weight=pkg.weight.LB,
                            store_num=None,
                            width=pkg.width.CM,
                            xc=None
                        ) for pkg in packages
                    ],
                    pickup_address=Address(
                        address_line_1=payload.shipper.address_line1,
                        address_line_2=payload.shipper.address_line2,
                        address_line_3=None,
                        attention=payload.shipper.person_name,
                        city=payload.shipper.city,
                        country=payload.shipper.country_code,
                        email=payload.shipper.email,
                        extension=None,
                        name=payload.shipper.company_name,
                        phone=payload.shipper.phone_number,
                        postal_code=payload.shipper.postal_code,
                        province=payload.shipper.state_code,
                        residential=payload.shipper.residential,
                    ),
                    premium=premium,
                    proforma=None,
                    reported_weight_unit=WeightUnit.LB.value,
                    send_email_to_delivery=payload.recipient.email,
                    send_email_to_pickup=payload.shipper.email,
                    service_type=service_type,
                    shipper_num=None,
                    shipping_date=None,
                    subtotal=None,
                    subtotal_with_handling=None,
                    total=None,
                    total_with_handling=None,
                    user_id=None,
                ),
                user_id=settings.user_id
            )
        )
    )

    return Serializable(request, default_request_serializer)
