"""Karrio Hermes shipment API implementation. See SPECS.md for the mapping."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.hermes.error as error
import karrio.providers.hermes.units as provider_units
import karrio.providers.hermes.utils as provider_utils
import karrio.schemas.hermes.shipment_request as hermes_req
import karrio.schemas.hermes.shipment_response as hermes_res


def _split_name(name: str | None) -> tuple[str, str]:
    """Split full name into firstname and lastname for Hermes API."""
    if not name:
        return (None, None)
    parts = name.split()
    firstname = parts[0] if parts else None
    lastname = " ".join(parts[1:]) if len(parts) > 1 else firstname
    return (firstname, lastname)


def parse_shipment_response(
    _response: lib.Deserializable[list[dict]],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails | None, list[models.Message]]:
    """Parse Hermes shipment response for single or multi-piece shipments."""
    responses = _response.deserialize()

    messages: list[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    shipment_details = [
        (
            f"{idx}",
            _extract_details(response, settings),
        )
        for idx, response in enumerate(responses, start=1)
        if isinstance(response, dict) and (response.get("shipmentID") or response.get("shipmentOrderID"))
    ]

    shipment = lib.to_multi_piece_shipment(shipment_details) if shipment_details else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from Hermes response."""
    response = lib.to_object(hermes_res.ShipmentResponseType, data)

    tracking_number = response.shipmentID or ""
    shipment_order_id = response.shipmentOrderID or ""
    label_image = response.labelImage or ""
    invoice_image = response.commInvoiceImage or ""

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
    """Build Hermes shipment request(s), one per package. See SPECS.md."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
        service=payload.service,
    )
    customs = payload.customs

    recipient_firstname, recipient_lastname = _split_name(recipient.person_name)
    shipper_firstname, shipper_lastname = _split_name(shipper.person_name)

    is_multi_piece = len(packages) > 1
    number_of_parts = len(packages) if is_multi_piece else None

    requests = [
        hermes_req.ShipmentRequestType(
            clientReference=lib.text(options.hermes_customer_reference_1.state or payload.reference, max=20) or "",
            clientReference2=lib.text(
                options.hermes_customer_reference_2.state or (payload.options or {}).get("clientReference2"),
                max=20,
            ),
            receiverName=hermes_req.ErNameType(
                title=None,
                gender=None,
                firstname=recipient_firstname,
                middlename=None,
                lastname=recipient_lastname,
            ),
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
            receiverContact=lib.identity(
                hermes_req.ReceiverContactType(
                    phone=lib.text(recipient.phone_number, max=20),
                    mobile=None,
                    mail=recipient.email,
                )
                if recipient.phone_number or recipient.email
                else None
            ),
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
            parcel=hermes_req.ParcelType(
                parcelClass=options.hermes_parcel_class.state,
                parcelHeight=lib.to_int(package.height.MM),
                parcelWidth=lib.to_int(package.width.MM),
                parcelDepth=lib.to_int(package.length.MM),
                parcelWeight=lib.to_int(package.weight.G),
                parcelVolume=None,
                productType=provider_units.PackagingType.map(package.packaging_type or "your_packaging").value,
            ),
            service=lib.identity(
                hermes_req.ServiceType(
                    tanService=options.hermes_tan_service.state,
                    multipartService=(
                        hermes_req.MultipartServiceType(
                            partNumber=index,
                            numberOfParts=number_of_parts,
                            parentShipmentOrderID=None,
                        )
                        if is_multi_piece
                        else (
                            hermes_req.MultipartServiceType(
                                partNumber=options.hermes_part_number.state or 1,
                                numberOfParts=options.hermes_number_of_parts.state,
                                parentShipmentOrderID=options.hermes_parent_shipment_order_id.state,
                            )
                            if options.hermes_number_of_parts.state
                            else None
                        )
                    ),
                    limitedQuantitiesService=options.hermes_limited_quantities.state,
                    cashOnDeliveryService=(
                        hermes_req.CashOnDeliveryServiceType(
                            amount=options.hermes_cod_amount.state,
                            currency=options.hermes_cod_currency.state or "EUR",
                            bankTransferAmount=options.hermes_cod_amount.state,
                            bankTransferCurrency=options.hermes_cod_currency.state or "EUR",
                        )
                        if options.hermes_cod_amount.state
                        else None
                    ),
                    bulkGoodService=options.hermes_bulk_goods.state,
                    statedTimeService=(
                        hermes_req.StatedTimeServiceType(
                            timeSlot=options.hermes_time_slot.state,
                        )
                        if options.hermes_time_slot.state
                        else None
                    ),
                    householdSignatureService=options.hermes_household_signature.state,
                    customerAlertService=(
                        hermes_req.CustomerAlertServiceType(
                            notificationType=options.hermes_notification_type.state or "EMAIL",
                            notificationEmail=options.hermes_notification_email.state,
                            notificationNumber=None,
                        )
                        if options.hermes_notification_email.state
                        else None
                    ),
                    parcelShopDeliveryService=(
                        hermes_req.ParcelShopDeliveryServiceType(
                            psCustomerFirstName=(
                                options.hermes_parcel_shop_customer_firstname.state or recipient_firstname
                            ),
                            psCustomerLastName=(
                                options.hermes_parcel_shop_customer_lastname.state or recipient_lastname
                            ),
                            psID=options.hermes_parcel_shop_id.state,
                            psSelectionRule=(
                                "SELECT_BY_ID" if options.hermes_parcel_shop_id.state else "SELECT_BY_RECEIVER_ADDRESS"
                            ),
                        )
                        if options.hermes_parcel_shop_id.state
                        or options.hermes_parcel_shop_selection_rule.state == "SELECT_BY_RECEIVER_ADDRESS"
                        else None
                    ),
                    identService=(
                        hermes_req.IdentServiceType(
                            identID=options.hermes_ident_id.state,
                            identType=options.hermes_ident_type.state,
                            identVerifyFsk=options.hermes_ident_fsk.state,
                            identVerifyBirthday=options.hermes_ident_birthday.state,
                        )
                        if options.hermes_ident_fsk.state or options.hermes_ident_id.state
                        else None
                    ),
                    statedDayService=(
                        hermes_req.StatedDayServiceType(
                            statedDay=options.hermes_stated_day.state,
                        )
                        if options.hermes_stated_day.state
                        else None
                    ),
                    nextDayService=options.hermes_next_day.state,
                    signatureService=options.hermes_signature.state,
                    redirectionProhibitedService=options.hermes_redirection_prohibited.state,
                    excludeParcelShopAuthorization=options.hermes_exclude_parcel_shop_auth.state,
                    lateInjectionService=options.hermes_late_injection.state,
                )
                if any(
                    [
                        options.hermes_tan_service.state,
                        is_multi_piece,
                        options.hermes_number_of_parts.state,
                        options.hermes_limited_quantities.state,
                        options.hermes_cod_amount.state,
                        options.hermes_bulk_goods.state,
                        options.hermes_time_slot.state,
                        options.hermes_household_signature.state,
                        options.hermes_notification_email.state,
                        options.hermes_parcel_shop_id.state,
                        options.hermes_parcel_shop_selection_rule.state,
                        options.hermes_ident_fsk.state,
                        options.hermes_ident_id.state,
                        options.hermes_stated_day.state,
                        options.hermes_next_day.state,
                        options.hermes_signature.state,
                        options.hermes_redirection_prohibited.state,
                        options.hermes_exclude_parcel_shop_auth.state,
                        options.hermes_late_injection.state,
                    ]
                )
                else None
            ),
            customsAndTaxes=(
                hermes_req.CustomsAndTaxesType(
                    currency=lib.identity(customs.duty.currency if customs.duty else "EUR"),
                    shipmentCost=None,
                    items=[
                        hermes_req.ItemType(
                            sku=item.sku,
                            category=None,
                            countryCodeOfManufacture=item.origin_country,
                            value=lib.to_int(item.value_amount * 100) if item.value_amount else None,
                            weight=lib.to_int(item.weight * 1000) if item.weight else None,
                            quantity=item.quantity or 1,
                            description=item.description or item.title,
                            exportDescription=None,
                            exportHsCode=None,
                            hsCode=item.hs_code,
                            url=None,
                        )
                        for item in (customs.commodities or [])
                    ]
                    or None,
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
                if customs
                else None
            ),
        )
        for index, package in enumerate(packages, start=1)
    ]

    return lib.Serializable(
        requests,
        lambda reqs: [lib.to_dict(req) for req in reqs],
        dict(is_multi_piece=is_multi_piece),
    )
