"""Karrio DPD France shipment create.

Multi-piece strategy: cargoNET's `CreateMultiShipmentBc` op does NOT return
labels (no `WithLabels` variant exists in the WSDL) and excludes Predict /
Relais / Retour services per Shipping PDF §8.3. We use Pattern B (per-package)
— issue N parallel `CreateShipmentWithLabelsBc` calls and aggregate via
`lib.to_multi_piece_shipment`. Single-parcel requests are a 1-element list
and traverse the same code path.
"""

import base64
import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.error as error
import karrio.providers.dpd_france.units as provider_units
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.eprintwebservice as dpd_france


def parse_shipment_response(
    _responses: lib.Deserializable[typing.List[lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    responses = _responses.deserialize()
    if not isinstance(responses, list):
        responses = [responses]

    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    package_shipments = [
        (f"{idx}", _extract_details(response, settings)) for idx, response in enumerate(responses, start=1)
    ]
    package_shipments = [(idx, ship) for idx, ship in package_shipments if ship is not None]

    shipment = lib.to_multi_piece_shipment(package_shipments) if package_shipments else None

    return shipment, messages


def _extract_details(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails | None:
    shipments = lib.find_element("ShipmentBc", response, dpd_france.ShipmentBc)
    labels = lib.find_element("Label", response, dpd_france.Label)
    if not shipments:
        return None

    primary = shipments[0]
    bc = getattr(primary, "Shipment", None)
    if bc is None:
        return None

    label = labels[0] if labels else None
    label_data = getattr(label, "label", None) if label is not None else None
    label_type_raw = getattr(label, "type_", None) if label is not None else None

    label_type = (
        "PNG"
        if label_type_raw == provider_units.LabelType.Default.value
        else (provider_units.LabelType.map(label_type_raw).value if label_type_raw else None)
    )

    encoded_label = base64.b64encode(label_data).decode("utf-8") if label_data else None

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=bc.BarCode,
        shipment_identifier=bc.BarcodeId,
        label_type=label_type,
        docs=models.Documents(label=encoded_label) if encoded_label else models.Documents(),
        meta={},
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value or "PDF"

    envelopes = [
        _build_envelope(shipper, recipient, package, label_type, payload.reference, settings) for package in packages
    ]

    return lib.Serializable(
        envelopes,
        lambda envs: [_serialize(env) for env in envs],
    )


def _build_envelope(
    shipper,
    recipient,
    package,
    label_type: str,
    reference: str | None,
    settings: provider_utils.Settings,
) -> lib.Envelope:
    request = dpd_france.CreateShipmentWithLabelsBc(
        request=dpd_france.StdShipmentLabelRequest(
            customer_countrycode=settings.customer_country_code,
            customer_centernumber=settings.customer_center_number,
            customer_number=settings.customer_number,
            shipperaddress=dpd_france.Address(
                countryPrefix=shipper.country_code,
                zipCode=shipper.postal_code,
                city=shipper.city,
                street=(shipper.street or "")[:35],
                name=(shipper.company_name or shipper.person_name),
                phoneNumber=shipper.phone_number,
            ),
            receiveraddress=dpd_france.Address(
                countryPrefix=recipient.country_code,
                zipCode=recipient.postal_code,
                city=recipient.city,
                street=(recipient.street or "")[:35],
                name=(recipient.company_name or recipient.person_name),
                phoneNumber=recipient.phone_number,
            ),
            weight=package.weight.KG,
            referencenumber=reference,
            labelType=dpd_france.LabelType(type_=label_type),
        )
    )

    return lib.Envelope(
        Header=lib.Header(
            dpd_france.UserCredentials(
                userid=settings.userid,
                password=settings.password,
            )
        ),
        Body=lib.Body(request),
    )


def _serialize(envelope: lib.Envelope) -> str:
    return lib.envelope_serializer(
        envelope,
        namespace=(
            'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software"'
        ),
        prefixes={
            "Envelope": "soapenv",
            "UserCredentials": "imt",
            "CreateShipmentWithLabelsBc": "imt",
        },
    )
