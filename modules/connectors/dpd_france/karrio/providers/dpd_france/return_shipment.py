"""Karrio DPD France return shipment (CreateReverseInverseShipmentWithLabelsBc).

Mirrors `shipment/create.py` Pattern B — N parallel calls per parcel,
aggregated via `lib.to_multi_piece_shipment`. Uses the reverse-inverse
operation per Shipping PDF §8.5: the recipient becomes the original
shipper (the return destination), and the shipper is the customer
returning the parcel.
"""

import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.shipment.create as create
import karrio.providers.dpd_france.units as provider_units
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.eprintwebservice as dpd_france


def parse_return_shipment_response(
    _responses: lib.Deserializable[typing.List[lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    return create.parse_shipment_response(_responses, settings)


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value or "PDF"

    envelopes = [
        _build_return_envelope(shipper, recipient, package, label_type, payload.reference, settings)
        for package in packages
    ]

    return lib.Serializable(envelopes, lambda envs: [_serialize(env) for env in envs])


def _build_return_envelope(
    shipper,
    recipient,
    package,
    label_type: str,
    reference: str | None,
    settings: provider_utils.Settings,
) -> lib.Envelope:
    request = dpd_france.CreateReverseInverseShipmentWithLabelsBc(
        request=dpd_france.ReverseShipmentLabelRequest(
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
            "CreateReverseInverseShipmentWithLabelsBc": "imt",
        },
    )
