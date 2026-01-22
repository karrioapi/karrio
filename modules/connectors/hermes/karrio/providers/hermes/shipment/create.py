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


def _split_name(name: typing.Optional[str]) -> typing.Tuple[str, str]:
    """Split full name into firstname and lastname for Hermes API."""
    if not name:
        return (None, None)
    parts = name.split()
    firstname = parts[0] if parts else None
    lastname = " ".join(parts[1:]) if len(parts) > 1 else firstname
    return (firstname, lastname)


def parse_shipment_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse Hermes shipment response for single or multi-piece shipments."""
    responses = _response.deserialize()

    # Collect all messages from all responses
    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    # Extract shipment details from each valid response
    shipment_details = [
        (
            f"{idx}",
            _extract_details(response, settings),
        )
        for idx, response in enumerate(responses, start=1)
        if isinstance(response, dict)
        and (response.get("shipmentID") or response.get("shipmentOrderID"))
    ]

    # Use lib.to_multi_piece_shipment() to aggregate multi-piece shipments
    shipment = lib.to_multi_piece_shipment(shipment_details) if shipment_details else None

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

    # Label media type - convert MIME type to format (e.g., "application/pdf" -> "PDF")
    label_mediatype = response.labelMediatype or "application/pdf"
    label_type = label_mediatype.split("/")[-1].upper() if "/" in label_mediatype else label_mediatype

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
    """Create Hermes shipment request(s) for single or multi-piece shipments.

    For multi-piece shipments (Pattern B - Per-Package Request):
    - First package: partNumber=1, numberOfParts=N, no parentShipmentOrderID
    - Subsequent packages: partNumber=2,3,..., numberOfParts=N, parentShipmentOrderID=<first shipmentOrderID>

    The proxy handles the sequential API calls and injects parentShipmentOrderID
    from the first response into subsequent requests.
    """
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Build customs for international shipments (shared across all packages)
    customs = None
    if payload.customs:
        customs = _build_customs(payload.customs, shipper)

    # Split names for Hermes API
    recipient_firstname, recipient_lastname = _split_name(recipient.person_name)
    shipper_firstname, shipper_lastname = _split_name(shipper.person_name)

    # Determine if this is a multi-piece shipment
    is_multi_piece = len(packages) > 1
    number_of_parts = len(packages) if is_multi_piece else None

    # Create a request for each package
    requests = []
    for index, package in enumerate(packages, start=1):
        # Determine product type for this package
        product_type = provider_units.PackagingType.map(
            package.packaging_type or "your_packaging"
        ).value

        # Build services object based on options
        # For multi-piece: add multipartService with partNumber and numberOfParts
        service = _build_service(
            options,
            is_multi_piece=is_multi_piece,
            part_number=index if is_multi_piece else None,
            number_of_parts=number_of_parts,
            # parentShipmentOrderID will be injected by proxy for packages 2+
        )

        # Create the request using generated schema types
        # Field length limits per OpenAPI spec:
        # - street: 50, houseNumber: 5, town: 30
        # - addressAddition: 50, addressAddition2: 20, addressAddition3: 20
        # - clientReference: 20, clientReference2: 20, phone: 20
        request = hermes_req.ShipmentRequestType(
            clientReference=lib.text(payload.reference, max=20) or "",
            clientReference2=lib.text((payload.options or {}).get("clientReference2"), max=20),
            # Receiver name
            receiverName=hermes_req.ErNameType(
                title=None,
                gender=None,
                firstname=recipient_firstname,
                middlename=None,
                lastname=recipient_lastname,
            ),
            # Receiver address
            receiverAddress=hermes_req.ErAddressType(
                street=lib.text(recipient.street_name, max=50),
                houseNumber=lib.text(recipient.street_number, max=5) or "",
                zipCode=recipient.postal_code,
                town=lib.text(recipient.city, max=30),
                countryCode=recipient.country_code,
                addressAddition=lib.text(recipient.address_line2, max=50),
                addressAddition2=None,
                addressAddition3=lib.text(recipient.company_name, max=20),
            ),
            # Receiver contact
            receiverContact=lib.identity(
                hermes_req.ReceiverContactType(
                    phone=lib.text(recipient.phone_number, max=20),
                    mobile=None,
                    mail=recipient.email,
                )
                if recipient.phone_number or recipient.email
                else None
            ),
            # Sender (divergent sender if different from account default)
            senderName=lib.identity(
                hermes_req.ErNameType(
                    title=None,
                    gender=None,
                    firstname=shipper_firstname,
                    middlename=None,
                    lastname=shipper_lastname,
                )
                if shipper.person_name
                else None
            ),
            senderAddress=lib.identity(
                hermes_req.ErAddressType(
                    street=lib.text(shipper.street_name, max=50),
                    houseNumber=lib.text(shipper.street_number, max=5) or "",
                    zipCode=shipper.postal_code,
                    town=lib.text(shipper.city, max=30),
                    countryCode=shipper.country_code,
                    addressAddition=lib.text(shipper.address_line2, max=50),
                    addressAddition2=None,
                    addressAddition3=lib.text(shipper.company_name, max=20),
                )
                if shipper.street
                else None
            ),
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
            # Services (includes multipartService for multi-piece shipments)
            service=service if any([
                getattr(service, attr) for attr in dir(service)
                if not attr.startswith('_') and getattr(service, attr) is not None
            ]) else None,
            # Customs for international (same for all packages)
            customsAndTaxes=customs,
        )
        requests.append(request)

    return lib.Serializable(
        requests,
        lambda reqs: [lib.to_dict(req) for req in reqs],
        dict(is_multi_piece=is_multi_piece),
    )


def _build_service(
    options: units.ShippingOptions,
    is_multi_piece: bool = False,
    part_number: typing.Optional[int] = None,
    number_of_parts: typing.Optional[int] = None,
) -> hermes_req.ServiceType:
    """Build Hermes service object from shipping options.

    For multi-piece shipments:
    - is_multi_piece: True if shipment has multiple packages
    - part_number: 1, 2, 3, ... for each package
    - number_of_parts: Total number of packages
    - parentShipmentOrderID: Injected by proxy for packages 2+ (not passed here)
    """
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

    # Multipart service - built from multi-piece parameters or manual options
    multipart_service = None
    if is_multi_piece and part_number is not None and number_of_parts is not None:
        # Automatic multi-piece handling
        # Note: parentShipmentOrderID is injected by proxy for part_number > 1
        multipart_service = hermes_req.MultipartServiceType(
            partNumber=part_number,
            numberOfParts=number_of_parts,
            parentShipmentOrderID=None,  # Will be injected by proxy for parts 2+
        )
    elif options.hermes_number_of_parts.state:
        # Manual multi-piece via options (legacy support)
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
    shipper,
) -> hermes_req.CustomsAndTaxesType:
    """Build customs and taxes for international shipments."""
    items = [
        hermes_req.ItemType(
            sku=item.sku,
            category=None,
            countryCodeOfManufacture=item.origin_country,
            value=lib.to_int(item.value_amount * 100) if item.value_amount else None,  # In cents
            weight=lib.to_int(item.weight * 1000) if item.weight else None,  # In grams
            quantity=item.quantity or 1,
            description=item.description or item.title,
            exportDescription=None,
            exportHsCode=None,
            hsCode=item.hs_code,
            url=None,
        )
        for item in customs.commodities or []
    ]

    shipper_firstname, shipper_lastname = _split_name(shipper.person_name) if shipper else (None, None)

    return hermes_req.CustomsAndTaxesType(
        currency=lib.identity(customs.duty.currency if customs.duty else "EUR"),
        shipmentCost=None,
        items=items or None,
        invoiceReferences=None,
        value=None,
        exportCustomsClearance=None,
        client=None,
        shipmentOriginAddress=lib.identity(
            hermes_req.ShipmentOriginAddressType(
                title=None,
                firstname=shipper_firstname,
                lastname=shipper_lastname,
                company=shipper.company_name,
                street=shipper.street_name,
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
            )
            if shipper
            else None
        ),
    )
