from typing import List, Tuple, Optional
from pycanpar.CanshipBusinessService import (
    processShipment,
    ProcessShipmentRq,
    Shipment,
    Address,
    Package,
)
from purplship.core.models import (
    Message,
    ShipmentRequest,
    ShipmentDetails,
)
from purplship.core.utils import (
    Serializable,
    Element,
    create_envelope,
    Envelope
)
from purplship.core.units import Packages
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer
from purplship.providers.canpar.units import WeightUnit, DimensionUnit, Option, Service


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    detail: ShipmentDetails = None

    return detail, parse_error_response(response, settings)


def _extract_tracking_details(node: Element, settings: Settings) -> ShipmentDetails:

    return ShipmentDetails()


def process_shipment(payload: ShipmentRequest, settings: Settings) -> Serializable[List[Envelope]]:
    packages = Packages(payload.parcels)
    service_type: Optional[str] = (
        Service[payload.service] if payload.service in Service.__members__ else None
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
        body_content=processShipment(
            request=ProcessShipmentRq(
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
