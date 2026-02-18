"""Canada Post Authorized Return shipment implementation.

Documentation:
    https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/createreturn.jsf

Schema source: schemas/authreturn.xsd (generated to karrio/schemas/canadapost/authreturn.py)

API Endpoint:
    POST /rs/{mailed-by-customer}/{mobo}/authorizedreturn
    Content-Type: application/vnd.cpc.authreturn-v2+xml
    Accept: application/vnd.cpc.authreturn-v2+xml
"""

import karrio.schemas.canadapost.authreturn as authreturn
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_return_shipment_response(
    _response: lib.Deserializable[typing.Tuple[lib.Element, str]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    element, label = response
    messages = provider_error.parse_error_response(element, settings)

    shipment = (
        _extract_details(element, label, settings)
        if len(lib.find_element("tracking-pin", element)) > 0
        else None
    )

    return shipment, messages


def _extract_details(
    element: lib.Element,
    label: str,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    info = lib.to_object(authreturn.AuthorizedReturnInfoType, element)
    tracking_number = info.tracking_pin

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        docs=models.Documents(label=label),
        label_type="PDF",
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            tracking_numbers=[tracking_number],
            shipment_identifiers=[tracking_number],
        ),
    )


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ServiceType.map(payload.service).value_or_key
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
    )
    package = packages[0]
    label_encoding, label_format = provider_units.LabelType.map(
        payload.label_type or "PDF_4x6"
    ).value

    request = authreturn.AuthorizedReturnType(
        service_code=service,
        returner=authreturn.ReturnerType(
            name=shipper.person_name,
            company=shipper.company_name,
            domestic_address=authreturn.DomesticAddressDetailsType(
                address_line_1=shipper.street,
                address_line_2=lib.text(shipper.address_line2),
                city=shipper.city,
                province=shipper.state_code,
                postal_code=provider_utils.format_ca_postal_code(
                    shipper.postal_code
                ),
            ),
        ),
        receiver=authreturn.ReceiverType(
            name=recipient.person_name,
            company=recipient.company_name or "Not Applicable",
            email=recipient.email,
            domestic_address=authreturn.DomesticAddressDetailsType(
                address_line_1=recipient.street,
                address_line_2=lib.text(recipient.address_line2),
                city=recipient.city,
                province=recipient.state_code,
                postal_code=provider_utils.format_ca_postal_code(
                    recipient.postal_code
                ),
            ),
        ),
        parcel_characteristics=authreturn.ParcelCharacteristicsType(
            weight=package.weight.map(provider_units.MeasurementOptions).KG,
            dimensions=(
                authreturn.dimensionsType(
                    length=package.length.map(provider_units.MeasurementOptions).CM,
                    width=package.width.map(provider_units.MeasurementOptions).CM,
                    height=package.height.map(provider_units.MeasurementOptions).CM,
                )
                if package.has_dimensions
                else None
            ),
        ),
        print_preferences=authreturn.PrintPreferencesType(
            output_format=label_format,
            encoding=label_encoding,
        ),
        settlement_info=authreturn.AuthSettlementInfoType(
            paid_by_customer=getattr(
                payload.payment, "account_number", settings.customer_number
            ),
            contract_id=settings.contract_id,
        ),
        references=(
            authreturn.ReferencesType(
                customer_ref_1=payload.reference,
            )
            if payload.reference
            else None
        ),
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_xml(
            _,
            name_="authorized-return",
            namespacedef_='xmlns="http://www.canadapost.ca/ws/authreturn-v2"',
        ),
        dict(label_type=label_encoding),
    )
