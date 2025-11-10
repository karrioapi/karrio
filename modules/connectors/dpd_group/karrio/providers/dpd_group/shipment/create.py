"""Karrio DPD Group shipment creation implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils
import karrio.providers.dpd_group.units as provider_units
import karrio.schemas.dpd_group.shipment_request as dpd_group_req
import karrio.schemas.dpd_group.shipment_response as dpd_group_res


def parse_shipment_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse DPD Group shipment response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Handle error responses
    if messages:
        return None, messages

    # Parse shipment response
    shipment_data = lib.to_object(dpd_group_res.ShipmentResponseType, response)

    # Extract tracking number from parcels
    tracking_number = None
    if hasattr(shipment_data, 'parcels') and shipment_data.parcels:
        first_parcel = shipment_data.parcels[0]
        tracking_number = (
            first_parcel.trackingNumber if hasattr(first_parcel, 'trackingNumber')
            else first_parcel.parcelNumber if hasattr(first_parcel, 'parcelNumber')
            else None
        )

    # Extract label content
    label_content = None
    if hasattr(shipment_data, 'label') and shipment_data.label:
        label_content = shipment_data.label.content if hasattr(shipment_data.label, 'content') else None

    shipment = models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_data.shipmentId if hasattr(shipment_data, 'shipmentId') else None,
        label_type="PDF",
        docs=models.Documents(label=label_content) if label_content else None,
        meta=dict(
            shipment_number=shipment_data.shipmentNumber if hasattr(shipment_data, 'shipmentNumber') else None,
            tracking_url=shipment_data.trackingUrl if hasattr(shipment_data, 'trackingUrl') else None,
            service_name=(
                shipment_data.services.productName if hasattr(shipment_data, 'services')
                and hasattr(shipment_data.services, 'productName')
                else None
            ),
        ),
    )

    return shipment, messages


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create DPD Group shipment request."""

    # Parse payload
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Determine service code
    service_code = service.value_or_key if service else provider_units.ShippingService.dpd_group_classic.value

    # Build request
    request = dpd_group_req.ShipmentRequestType(
        shipperAddress=dpd_group_req.ErAddressType(
            name=shipper.person_name or shipper.company_name,
            company=shipper.company_name,
            street=shipper.street_name or shipper.address_line1,
            houseNumber=shipper.street_number,
            postalCode=shipper.postal_code,
            city=shipper.city,
            country=shipper.country_code,
            email=shipper.email,
            phone=shipper.phone_number,
        ),
        receiverAddress=dpd_group_req.ErAddressType(
            name=recipient.person_name or recipient.company_name,
            company=recipient.company_name,
            street=recipient.street_name or recipient.address_line1,
            houseNumber=recipient.street_number,
            postalCode=recipient.postal_code,
            city=recipient.city,
            country=recipient.country_code,
            email=recipient.email,
            phone=recipient.phone_number,
        ),
        parcels=[
            dpd_group_req.ParcelType(
                weight=package.weight.value,
                length=package.length.value if package.length else None,
                width=package.width.value if package.width else None,
                height=package.height.value if package.height else None,
                content=package.description or "Goods",
                customerReferenceNumber1=package.package_id or payload.reference,
            )
            for package in packages
        ],
        productCode=service_code,
        orderNumber=payload.reference,
        shipmentDate=lib.fdate(payload.shipment_date) if payload.shipment_date else None,
        labelFormat=payload.label_type or "PDF",
        services=lib.identity(
            dpd_group_req.ServicesType(
                saturdayDelivery=options.saturday_delivery.state if options.saturday_delivery else False,
                insurance=lib.identity(
                    dpd_group_req.InsuranceType(
                        value=options.insurance.state,
                        currency=options.currency or "EUR",
                    ) if options.insurance else None
                ),
            ) if any([options.saturday_delivery, options.insurance]) else None
        ),
    )

    return lib.Serializable(request, lib.to_dict)
