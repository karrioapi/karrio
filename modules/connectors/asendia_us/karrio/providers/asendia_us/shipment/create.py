import karrio.schemas.asendia_us.shipping_request as asendia
import karrio.schemas.asendia_us.shipping_response as shipping
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
        tracking_number=shipment.packageLabel.trackingNumber,
        shipment_identifier=shipment.packageLabel.packageId,
        label_type=label.get("type"),
        docs=models.Documents(label=label.get("content")),
        meta=dict(package_id=shipment.packageLabel.packageId),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )

    request = asendia.ShippingRequestType(
        accountNumber=settings.account_number,
        subAccountNumber=settings.connection_config.sub_account_number.state,
        processingLocation=settings.connection_config.processing_location.state,
        includeRate=True,
        labelType=payload.label_type,
        orderNumber=options.order_number.state,
        dispatchNumber=options.dispatch_number.state,
        packageID=(payload.reference or options.package_id.state),
        recipientTaxID=recipient.tax_id,
        returnFirstName=shipper.person_name,
        returnLastName=shipper.person_name,
        returnCompanyName=shipper.company_name,
        returnAddressLine1=shipper.address_line1,
        returnAddressLine2=shipper.address_line2,
        returnAddressLine3=None,
        returnCity=shipper.city,
        returnProvince=shipper.state_code,
        returnPostalCode=shipper.postal_code,
        returnCountryCode=shipper.country_code,
        returnPhone=shipper.phone_number,
        returnEmail=shipper.email,
        recipientFirstName=recipient.person_name,
        recipientLastName=recipient.person_name,
        recipientBusinessName=recipient.company_name,
        recipientAddressLine1=recipient.address_line1,
        recipientAddressLine2=recipient.address_line2,
        recipientAddressLine3=None,
        recipientCity=recipient.city,
        recipientProvince=recipient.state_code,
        recipientPostalCode=recipient.postal_code,
        recipientCountryCode=recipient.country_code,
        recipientPhone=recipient.phone_number,
        recipientEmail=recipient.email,
        totalPackageWeight=package.weight.value,
        weightUnit=provider_units.WeightUnit.map(package.weight_unit.value).value,
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
        sellerName=shipper.company_name or shipper.person_name,
        sellerAddressLine1=shipper.address_line1,
        sellerAddressLine2=shipper.address_line2,
        sellerAddressLine3=None,
        sellerCity=shipper.city,
        sellerProvince=shipper.state_code,
        sellerPostalCode=shipper.postal_code,
        sellerCountryCode=shipper.country_code,
        sellerPhone=shipper.phone_number,
        sellerEmail=shipper.email,
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

    return lib.Serializable(request, lib.to_dict)
