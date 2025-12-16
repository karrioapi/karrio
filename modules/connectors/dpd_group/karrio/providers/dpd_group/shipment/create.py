"""Karrio DPD Group shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils
import karrio.providers.dpd_group.units as provider_units
import karrio.core.errors as errors
import karrio.schemas.dpd_group.shipment_request as dpd_req
import karrio.schemas.dpd_group.shipment_response as dpd_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data
    has_shipment = "shipmentId" in response if isinstance(response, dict) else False

    shipment = _extract_details(response, settings) if has_shipment and not any(messages) else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from DPD META-API response."""
    shipment = lib.to_object(dpd_res.ShipmentResponseType, data)

    # Extract tracking number from parcelIds
    tracking_number = shipment.parcelIds[0]

    # Extract label data
    label_data = shipment.label.base64Data

    # Build tracking URL
    tracking_url = settings.tracking_url.format(tracking_number)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment.shipmentId,
        label_type="PDF",  # DPD returns PDF by default
        docs=models.Documents(label=label_data),
        meta=dict(
            network_shipment_id=shipment.networkShipmentId,
            network_parcel_ids=shipment.networkParcelIds,
            parcel_barcodes=lib.to_dict(shipment.parcelBarcodes) if shipment.parcelBarcodes else [],
            tracking_url=tracking_url,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a DPD META-API shipment request."""
    # DPD META-API requires sender.customerInfos identifiers (Swagger: sender.customerInfos.customerID/customerAccountNumber).
    # If we don't have these, DPD responds with errors like:
    # - COMMON_7 generalShipmentData.sender.customerNumber
    customer_id = settings.account_number
    customer_account = settings.customer_account_number or customer_id

    if not any(customer_id):
        raise errors.ShippingSDKError(
            "DPD shipment creation requires a sender customer number (customerInfos.customerID). "
            "Please set the DPD connection 'account_number' (and optionally 'customer_account_number')."
        )

    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get total weight in grams
    total_weight = sum(pkg.weight.value for pkg in packages)
    weight_in_grams = int(total_weight * 1000) if packages[0].weight.unit == "KG" else int(total_weight * 453.592)

    # Get first package dimensions
    first_package = packages[0]
    dimensions = None
    if first_package.length and first_package.width and first_package.height:
        dimensions = dpd_req.DimensionsType(
            length=int(first_package.length.value),
            width=int(first_package.width.value),
            height=int(first_package.height.value),
        )

    # Build shipment request
    request = dpd_req.ShipmentRequestType(
        numberOfParcels=str(len(packages)),
        shipmentInfos=dpd_req.ShipmentInfosType(
            productCode=service.value_or_key if service else "101",
            shipmentId=payload.reference or "",
            weight=str(weight_in_grams),
            dimensions=dimensions,
        ),
        sender=dpd_req.SenderType(
            customerInfos=dpd_req.CustomerInfosType(
                customerID=customer_id,
                customerAccountNumber=customer_account,
            ),
            address=dpd_req.AddressType(
                companyName=shipper.company_name or "",
                name1=shipper.person_name or "",
                street=shipper.street_name or shipper.address_line1 or "",
                houseNumber=shipper.street_number or "",
                zipCode=shipper.postal_code,
                city=shipper.city,
                country=shipper.country_code,
            ),
            contact=dpd_req.ContactType(
                phone1=shipper.phone_number or "",
                email=shipper.email or "",
            ),
        ),
        receiver=dpd_req.ReceiverType(
            address=dpd_req.AddressType(
                name1=recipient.person_name or "",
                companyName=recipient.company_name or "",
                street=recipient.street_name or recipient.address_line1 or "",
                houseNumber=recipient.street_number or "",
                zipCode=recipient.postal_code,
                city=recipient.city,
                country=recipient.country_code,
            ),
            contact=dpd_req.ContactType(
                phone1=recipient.phone_number or "",
                email=recipient.email or "",
            ),
        ),
        parcel=[
            dpd_req.ParcelType(
                parcelInfos=dpd_req.ParcelInfosType(
                    weight=int(pkg.weight.value * 1000) if pkg.weight.unit == "KG" else int(pkg.weight.value * 453.592),
                    dimensions=dpd_req.DimensionsType(
                        length=int(pkg.length.value),
                        width=int(pkg.width.value),
                        height=int(pkg.height.value),
                    ) if pkg.length and pkg.width and pkg.height else None,
                ),
                parcelContent=pkg.description or payload.reference or "Goods",
            )
            for pkg in packages
        ],
    )

    # DPD META-API /shipment expects an array at the root (even for a single shipment).
    # See: validation error "Instance type (object) ... allowed: ['array']"
    return lib.Serializable(
        [request],
        lib.to_dict,
        dict(label_format=options.label_format.state or "PDF"),
    )
