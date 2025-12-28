"""Karrio Hermes shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.hermes.error as error
import karrio.providers.hermes.utils as provider_utils
import karrio.providers.hermes.units as provider_units
import karrio.schemas.hermes.shipment_request as hermes_req
import karrio.schemas.hermes.shipment_response as hermes_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse Hermes shipment response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data (shipmentID indicates success)
    shipment = None
    if response.get("shipmentID") or response.get("shipmentOrderID"):
        shipment = _extract_details(response, settings)

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from Hermes response."""
    response = lib.to_object(hermes_res.ShipmentResponseType, data)

    # Hermes uses shipmentID as tracking number (14 or 20 characters)
    tracking_number = response.shipmentID or ""
    shipment_order_id = response.shipmentOrderID or ""

    # Label is returned as base64 encoded image
    label_image = response.labelImage or ""

    # Commercial invoice for international shipments
    invoice_image = response.commInvoiceImage or ""

    # Label media type
    label_type = response.labelMediatype or "PDF"

    documents = models.Documents(label=label_image)
    if invoice_image:
        documents.invoice = invoice_image

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_order_id,
        label_type=label_type,
        docs=documents,
        meta=dict(
            shipment_id=tracking_number,
            shipment_order_id=shipment_order_id,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a Hermes shipment request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    package = packages.single  # Hermes handles one parcel per request
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Determine product type
    product_type = provider_units.PackagingType.map(
        package.packaging_type or "your_packaging"
    ).value

    # Build services object based on options
    service = _build_service(options)

    # Build customs for international shipments
    customs = None
    if payload.customs:
        customs = _build_customs(payload.customs, shipper)

    # Create the request using generated schema types
    request = hermes_req.ShipmentRequestType(
        clientReference=payload.reference or "",
        clientReference2=options.get("clientReference2") or None,
        # Receiver name
        receiverName=hermes_req.ErNameType(
            title=None,
            gender=None,
            firstname=recipient.person_name.split()[0] if recipient.person_name else None,
            middlename=None,
            lastname=" ".join(recipient.person_name.split()[1:]) if recipient.person_name and len(recipient.person_name.split()) > 1 else recipient.person_name,
        ),
        # Receiver address
        receiverAddress=hermes_req.ErAddressType(
            street=recipient.street,
            houseNumber=recipient.street_number or "",
            zipCode=recipient.postal_code,
            town=recipient.city,
            countryCode=recipient.country_code,
            addressAddition=recipient.address_line2 or None,
            addressAddition2=None,
            addressAddition3=recipient.company_name or None,
        ),
        # Receiver contact
        receiverContact=hermes_req.ReceiverContactType(
            phone=recipient.phone_number or None,
            mobile=None,
            mail=recipient.email or None,
        ) if recipient.phone_number or recipient.email else None,
        # Sender (divergent sender if different from account default)
        senderName=hermes_req.ErNameType(
            title=None,
            gender=None,
            firstname=shipper.person_name.split()[0] if shipper.person_name else None,
            middlename=None,
            lastname=" ".join(shipper.person_name.split()[1:]) if shipper.person_name and len(shipper.person_name.split()) > 1 else shipper.person_name,
        ) if shipper.person_name else None,
        senderAddress=hermes_req.ErAddressType(
            street=shipper.street,
            houseNumber=shipper.street_number or "",
            zipCode=shipper.postal_code,
            town=shipper.city,
            countryCode=shipper.country_code,
            addressAddition=shipper.address_line2 or shipper.company_name or None,
            addressAddition2=None,
            addressAddition3=None,
        ) if shipper.street else None,
        # Parcel details (weight in grams)
        parcel=hermes_req.ParcelType(
            parcelClass=None,  # Optional, calculated from dimensions
            parcelHeight=lib.to_int(package.height.MM) if package.height else None,
            parcelWidth=lib.to_int(package.width.MM) if package.width else None,
            parcelDepth=lib.to_int(package.length.MM) if package.length else None,
            parcelWeight=lib.to_int(package.weight.G),  # Weight in grams
            parcelVolume=None,  # Optional
            productType=product_type,
        ),
        # Services
        service=service if any([
            getattr(service, attr) for attr in dir(service)
            if not attr.startswith('_') and getattr(service, attr) is not None
        ]) else None,
        # Customs for international
        customsAndTaxes=customs,
    )

    return lib.Serializable(request, lib.to_dict)


def _build_service(options: units.ShippingOptions) -> hermes_req.ServiceType:
    """Build Hermes service object from shipping options."""
    # Cash on delivery
    cod_service = None
    if options.hermes_cod_amount.state:
        cod_service = hermes_req.CashOnDeliveryServiceType(
            amount=options.hermes_cod_amount.state,
            currency=options.hermes_cod_currency.state or "EUR",
            bankTransferAmount=options.hermes_cod_amount.state,
            bankTransferCurrency=options.hermes_cod_currency.state or "EUR",
        )

    # Customer alert service
    alert_service = None
    if options.hermes_notification_email.state:
        alert_service = hermes_req.CustomerAlertServiceType(
            notificationType=options.hermes_notification_type.state or "EMAIL",
            notificationEmail=options.hermes_notification_email.state,
            notificationNumber=None,
        )

    # Ident service
    ident_service = None
    if options.hermes_ident_fsk.state or options.hermes_ident_id.state:
        ident_service = hermes_req.IdentServiceType(
            identID=options.hermes_ident_id.state,
            identType=options.hermes_ident_type.state,
            identVerifyFsk=options.hermes_ident_fsk.state,
            identVerifyBirthday=options.hermes_ident_birthday.state,
        )

    # Parcel shop delivery
    parcel_shop_service = None
    if options.hermes_parcel_shop_id.state:
        parcel_shop_service = hermes_req.ParcelShopDeliveryServiceType(
            psCustomerFirstName=options.hermes_parcel_shop_customer_firstname.state,
            psCustomerLastName=options.hermes_parcel_shop_customer_lastname.state,
            psID=options.hermes_parcel_shop_id.state,
            psSelectionRule=options.hermes_parcel_shop_selection_rule.state or "SELECT_BY_ID",
        )

    # Stated day service
    stated_day_service = None
    if options.hermes_stated_day.state:
        stated_day_service = hermes_req.StatedDayServiceType(
            statedDay=options.hermes_stated_day.state,
        )

    # Stated time service
    stated_time_service = None
    if options.hermes_time_slot.state:
        stated_time_service = hermes_req.StatedTimeServiceType(
            timeSlot=options.hermes_time_slot.state,
        )

    # Multipart service
    multipart_service = None
    if options.hermes_number_of_parts.state:
        multipart_service = hermes_req.MultipartServiceType(
            partNumber=options.hermes_part_number.state or 1,
            numberOfParts=options.hermes_number_of_parts.state,
            parentShipmentOrderID=options.hermes_parent_shipment_order_id.state,
        )

    return hermes_req.ServiceType(
        tanService=options.hermes_tan_service.state,
        multipartService=multipart_service,
        limitedQuantitiesService=options.hermes_limited_quantities.state,
        cashOnDeliveryService=cod_service,
        bulkGoodService=options.hermes_bulk_goods.state,
        statedTimeService=stated_time_service,
        householdSignatureService=options.hermes_household_signature.state,
        customerAlertService=alert_service,
        parcelShopDeliveryService=parcel_shop_service,
        compactParcelService=options.hermes_compact_parcel.state,
        identService=ident_service,
        statedDayService=stated_day_service,
        nextDayService=options.hermes_next_day.state,
        signatureService=options.hermes_signature.state,
        redirectionProhibitedService=options.hermes_redirection_prohibited.state,
        excludeParcelShopAuthorization=options.hermes_exclude_parcel_shop_auth.state,
        lateInjectionService=options.hermes_late_injection.state,
    )


def _build_customs(
    customs: models.Customs,
    shipper: lib.Address,
) -> hermes_req.CustomsAndTaxesType:
    """Build customs and taxes for international shipments."""
    items = [
        hermes_req.ItemType(
            sku=item.sku or None,
            category=None,
            countryCodeOfManufacture=item.origin_country or None,
            value=lib.to_int(item.value_amount * 100) if item.value_amount else None,  # In cents
            weight=lib.to_int(item.weight * 1000) if item.weight else None,  # In grams
            quantity=item.quantity or 1,
            description=item.description or item.title or None,
            exportDescription=None,
            exportHsCode=None,
            hsCode=item.hs_code or None,
            url=None,
        )
        for item in customs.commodities or []
    ]

    return hermes_req.CustomsAndTaxesType(
        currency=customs.duty.currency if customs.duty else "EUR",
        shipmentCost=None,
        items=items if items else None,
        invoiceReferences=None,
        value=None,
        exportCustomsClearance=None,
        client=None,
        shipmentOriginAddress=hermes_req.ShipmentOriginAddressType(
            title=None,
            firstname=shipper.person_name.split()[0] if shipper.person_name else None,
            lastname=" ".join(shipper.person_name.split()[1:]) if shipper.person_name else None,
            company=shipper.company_name,
            street=shipper.street,
            houseNumber=shipper.street_number or "",
            zipCode=shipper.postal_code,
            town=shipper.city,
            state=shipper.state_code,
            countryCode=shipper.country_code,
            addressAddition=shipper.address_line2,
            addressAddition2=None,
            addressAddition3=None,
            phone=shipper.phone_number,
            fax=None,
            mobile=None,
            mail=shipper.email,
        ) if shipper else None,
    )
