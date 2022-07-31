import amazon_mws_lib.purchase_shipment_request as amazon
from amazon_mws_lib.purchase_shipment_response import LabelResult

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.amazon_mws.error as provider_error
import karrio.providers.amazon_mws.units as provider_units
import karrio.providers.amazon_mws.utils as provider_utils


def parse_shipment_response(
    response: dict, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
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
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options)

    request = amazon.PurchaseShipmentRequest(
        clientReferenceId=payload.reference or payload.id,
        shipFrom=amazon.Ship(
            name=payload.shipper.person_name,
            city=payload.shipper.city,
            addressLine1=payload.shipper.address_line1,
            addressLine2=payload.shipper.address_line2,
            stateOrRegion=payload.shipper.state_code,
            email=payload.shipper.email,
            phoneNumber=payload.shipper.phone_number,
        ),
        shipTo=amazon.Ship(
            name=payload.recipient.person_name,
            city=payload.recipient.city,
            addressLine1=payload.recipient.address_line1,
            addressLine2=payload.recipient.address_line2,
            stateOrRegion=payload.recipient.state_code,
            email=payload.recipient.email,
            phoneNumber=payload.recipient.phone_number,
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
                        title=item.description,
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
