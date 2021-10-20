from typing import List, Tuple
from ics_courier_lib.services import (
    AddressInfo,
    ArrayOfPieceInfo,
    Authenticate,
    CreateShipment,
    PackageInfo,
    PieceInfo,
    ArrayOfString,
    CreateShipmentResponse
    
)
from purplship.core.models import (
    Message,
    ShipmentRequest,
    ShipmentDetails,
)
from purplship.core.utils import (
    create_envelope,
    Serializable,
    Element,
    Envelope,
    XP,
)
from purplship.core.units import Packages, Options
from purplship.providers.ics_courier.error import parse_error_response
from purplship.providers.ics_courier.utils import Settings
from purplship.providers.ics_courier.units import Service, Option


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    package = XP.find("PackageID", response, ArrayOfString, first=True)
    label = XP.find("label", response, first=True)
    details = (
        _extract_details((package.string[0], str(label.text)), settings)
        if getattr(package, 'string', [None])[0] is not None else None
    )

    return details, parse_error_response(response, settings)


def _extract_details(response: Tuple[str, str], settings: Settings) -> ShipmentDetails:
    package_id, label = response

    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        label=label,
        tracking_number=package_id,
        shipment_identifier=package_id,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels)
    options = Options(payload.options, Option)
    product = Service.map(payload.service).value_or_key

    request = create_envelope(
        body_content=CreateShipment(
            AuthenicateAccount=Authenticate(
                AccountID=settings.account_id,
                Password=settings.password,
            ),
            ConsigneeInfo=AddressInfo(
                ID=payload.recipient.id,
                Name=payload.recipient.company_name,
                Address1=payload.recipient.address_line1,
                Address2=payload.recipient.address_line2,
                City=payload.recipient.city,
                Province=payload.recipient.state_code,
                Postcode=payload.recipient.postal_code,
                Contact=payload.recipient.person_name,
                Phone=payload.recipient.phone_number,
            ),
            PackageInfo=PackageInfo(
                Product=product,
                Pieces=ArrayOfPieceInfo(
                    PieceInfo=[
                        PieceInfo(
                            Weight=piece.weight.value,
                            WeightUnit=piece.weight.unit,
                            Length=piece.length.value,
                            Width=piece.width.value,
                            Height=piece.height.value,
                            DeclaredValue=None,
                        )
                        for piece in packages
                    ]
                ),
                Contact=payload.shipper.person_name,
                Phone=payload.shipper.phone_number,
                CostCenter=options.ics_courier_cost_center,
                Refereces=(
                    ArrayOfString(string=[payload.reference])
                    if payload.reference is not None 
                    else payload.reference
                ),
                NotificationEmail=(
                    options.email_notification_to or payload.recipient.email_address
                    if options.email_notification and any(
                        [options.email_notification_to or payload.recipient.email_address]
                    ) else None
                ),
                SpecialInstruction=options.ics_courier_special_instruction,
                NoSignatureRequired=options.ics_courier_no_signature_required,
                ShipDate=options.ship_date,
            )
        ),
    )

    return Serializable(request)
