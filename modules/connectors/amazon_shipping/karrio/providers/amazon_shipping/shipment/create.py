import karrio.schemas.amazon_shipping.purchase_shipment_request as amazon
from karrio.schemas.amazon_shipping.purchase_shipment_response import LabelResult

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.amazon_shipping.error as provider_error
import karrio.providers.amazon_shipping.units as provider_units
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[dict], settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    errors: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(data, settings)
            for data in response.get("errors", [])
        ],
        [],
    )
    shipment = lib.to_multi_piece_shipment(
        [
            (index, _extract_details(data, data.get("shipmentId"), settings))
            for index, data in enumerate(response.get("labelResults", []))
        ]
    )

    return shipment, errors


def _extract_details(
    data: dict,
    shipment_identifier: str,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    result = lib.to_object(LabelResult, data)
    label = lib.image_to_pdf(result.label.labelStream)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=result.trackingId,
        shipment_identifier=shipment_identifier,
        label_type="PDF",
        docs=models.Documents(label=label),
        meta=dict(
            containerReferenceId=result.containerReferenceId,
        ),
    )


def shipment_request(payload: models.ShipmentRequest, _) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options)

    request = amazon.PurchaseShipmentRequest(
        clientReferenceId=payload.reference or payload.id,
        shipFrom=amazon.Ship(
            name=shipper.person_name,
            city=shipper.city,
            addressLine1=shipper.street,
            addressLine2=shipper.address_line2,
            stateOrRegion=shipper.state_code,
            email=shipper.email,
            phoneNumber=shipper.phone_number,
        ),
        shipTo=amazon.Ship(
            name=recipient.person_name,
            city=recipient.city,
            addressLine1=recipient.street,
            addressLine2=recipient.address_line2,
            stateOrRegion=recipient.state_code,
            email=recipient.email,
            phoneNumber=recipient.phone_number,
        ),
        shipDate=lib.fdatetime(options.shipment_date.state, "%Y-%m-%d"),
        serviceType=provider_units.Service.map(payload.service).name_or_key,
        containers=[
            amazon.Container(
                containerType="PACKAGE",
                containerReferenceId=package.parcel.id,
                dimensions=amazon.Dimensions(
                    height=package.height.IN,
                    length=package.length.IN,
                    width=package.width.IN,
                    unit="IN",
                ),
                weight=amazon.UnitWeight(
                    value=package.weight.LB,
                    unit="LB",
                ),
                items=[
                    amazon.Item(
                        quantity=item.quantity,
                        title=lib.text(item.title or item.description, max=35),
                        unitPrice=amazon.UnitPrice(
                            value=item.value_amount,
                            unit=item.value_currency,
                        ),
                        unitWeight=amazon.UnitWeight(
                            value=units.Weight(item.weight, item.weight_unit).LB,
                            unit="LB",
                        ),
                    )
                    for item in package.parcel.items
                ],
            )
            for package in packages
        ],
        labelSpecification=amazon.LabelSpecification(
            labelFormat="PNG",
            labelStockSize="4X6",
        ),
    )

    return lib.Serializable(request, lib.to_dict)
