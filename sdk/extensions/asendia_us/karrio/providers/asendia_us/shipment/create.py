import karrio.schemas.asendia_us.shipment_request as asendia
import karrio.schemas.asendia_us.shipment_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.asendia_us.error as error
import karrio.providers.asendia_us.utils as provider_utils
import karrio.providers.asendia_us.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if response.get("packageLabel") is not None
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponseType, data)
    label: dict = (
        next(iter(data.get("packageLabel", {}).get("labels") or []), None) or {}
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.packageID,
        label_type=label.get("type"),
        docs=models.Documents(label=label.get("content")),
        meta=dict(package_id=shipment.packageID),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )

    request = asendia.ShipmentRequestType(
        accountNumber=settings.account_number,
        subAccountNumber=settings.connection_config.sub_account_number.state,
        processingLocation=settings.connection_config.processing_location.state,
        includeRates=True,
        labelType=payload.label_type,
        orderNumber=options.order_number.state,
        dispatchNumber=options.dispatch_number.state,
        packageID=(payload.reference or options.package_id.state),
        recipientTaxID=payload.recipient.tax_id,
        returnFirstName=payload.shipper.person_name,
        returnLastName=payload.shipper.person_name,
        returnCompanyName=payload.shipper.company_name,
        returnAddressLine1=payload.shipper.address_line1,
        returnAddressLine2=payload.shipper.address_line2,
        returnAddressLine3=None,
        returnCity=payload.shipper.city,
        returnProvince=payload.shipper.state_code,
        returnPostalCode=payload.shipper.postal_code,
        returnCountryCode=payload.shipper.country_code,
        returnPhone=payload.shipper.phone_number,
        returnEmail=payload.shipper.email,
        recipientFirstName=payload.recipient.person_name,
        recipientLastName=payload.recipient.person_name,
        recipientBusinessName=payload.recipient.company_name,
        recipientAddressLine1=payload.recipient.address_line1,
        recipientAddressLine2=payload.recipient.address_line2,
        recipientAddressLine3=None,
        recipientCity=payload.recipient.city,
        recipientProvince=payload.recipient.state_code,
        recipientPostalCode=payload.recipient.postal_code,
        recipientCountryCode=payload.recipient.country_code,
        recipientPhone=payload.recipient.phone_number,
        recipientEmail=payload.recipient.email,
        totalPackageWeight=package.weight.value,
        weightUnit=package.weight_unit.value,
        currencyType=(
            options.currency.state or settings.connection_config.currency.state
        ),
        productCode=service,
        customerReferenceNumber1=payload.reference,
        customerReferenceNumber2=options.customer_reference_number2.state,
        customerReferenceNumber3=options.customer_reference_number3.state,
        contentType=package.packaging_type,
        packageContentDescription=package.description,
        vatNumber=options.vat_number.state,
        sellerName=payload.shipper.company_name or payload.shipper.person_name,
        sellerAddressLine1=payload.shipper.address_line1,
        sellerAddressLine2=payload.shipper.address_line2,
        sellerAddressLine3=None,
        sellerCity=payload.shipper.city,
        sellerProvince=payload.shipper.state_code,
        sellerPostalCode=payload.shipper.postal_code,
        sellerCountryCode=payload.shipper.country_code,
        sellerPhone=payload.shipper.phone_number,
        sellerEmail=payload.shipper.email,
        items=[
            asendia.ItemType(
                sku=item.sku,
                itemDescription=item.description,
                unitPrice=item.value_amount,
                quantity=item.quantity,
                unitWeight=item.weight,
                countryOfOrigin=item.origin_country,
                htsNumber=item.metadata.get("hts_number"),
            )
            for item in package.items
        ],
    )

    return lib.Serializable(request)
