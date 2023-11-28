import karrio.schemas.bpost.shm_deep_integration_v5 as bpost
import uuid
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.bpost.error as error
import karrio.providers.bpost.utils as provider_utils
import karrio.providers.bpost.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings, _response.ctx)
        if _response.ctx.get("label") is not None
        else None
    )

    return shipment, messages


def _extract_details(
    _: lib.Element,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    labels = lib.to_object(bpost.LabelsType, ctx["label"])
    details = labels.label[0]
    label_type = "PDF" if "pdf" in details.mimeType else "PNG"
    label = lib.bundle_base64(
        [lib.encode_base64(_.bytes) for _ in labels.label], format=label_type
    )
    tracking_numbers: typing.List[str] = sum([_.barcode for _ in labels.label], [])
    tracking_number = tracking_numbers[0]
    shipment_identifier = ctx["reference"]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_identifier,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_url=settings.tracking_url.format(tracking_number),
            shipment_identifiers=[shipment_identifier],
            tracking_numbers=tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    reference = payload.parcels[0].reference_number or f"ref_{uuid.uuid4()}"
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    is_international = payload.shipper.country_code != payload.recipient.country_code
    method = provider_units.ShippingService.method(service, is_international)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        option_type=provider_units.ShippingOption,
        shipper=shipper,
        recipient=recipient,
    )
    hold_location = lib.to_address(
        options.hold_at_location_address.state or payload.recipient
    )
    lines = customs.commodities if any(customs.commodities) else packages.items
    label_format, label_header = (
        provider_units.LabelType.map(payload.label_type).value
        or provider_units.LabelType.PDF.value
    )

    request = bpost.OrderType(
        accountId=settings.account_id,
        reference=reference,
        costCenter=settings.connection_config.cost_center.state,
        orderLine=(
            [
                bpost.OrderLineType(
                    text=item.description or item.title,
                    nbOfItems=item.quantity,
                )
                for item in lines
            ]
            if any(lines)
            else None
        ),
        box=[
            bpost.BoxType(
                sender=bpost.Party(
                    name=shipper.contact,
                    company=shipper.company_name,
                    address=bpost.AddressType(
                        streetName=shipper.street_name,
                        addressLineTwo=shipper.address_line2,
                        number=shipper.street_number,
                        box=None,
                        postalCode=shipper.postal_code,
                        locality=shipper.city,
                        countryCode=shipper.country_code,
                    ),
                    emailAddress=shipper.email,
                    phoneNumber=shipper.phone_number,
                ),
                nationalBox=(
                    bpost.NationalBoxType(
                        atHome=(
                            bpost.atHome(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                weight=package.weight.G,
                                height=package.height.MM,
                                length=package.length.MM,
                                width=package.width.MM,
                                openingHours=None,
                                desiredDeliveryPlace=None,
                                receiver=bpost.Party(
                                    name=recipient.contact,
                                    company=recipient.company_name,
                                    address=bpost.AddressType(
                                        streetName=recipient.street_name,
                                        addressLineTwo=recipient.address_line2,
                                        number=recipient.street_number,
                                        box=None,
                                        postalCode=recipient.postal_code,
                                        locality=recipient.city,
                                        countryCode=recipient.country_code,
                                    ),
                                    emailAddress=recipient.email,
                                    phoneNumber=recipient.phone_number,
                                ),
                                requestedDeliveryDate=None,
                            )
                            if method == "atHome"
                            else None
                        ),
                        atBpost=(
                            bpost.atBpost(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                weight=package.weight.G,
                                height=package.height.MM,
                                length=package.length.MM,
                                width=package.width.MM,
                                openingHours=None,
                                desiredDeliveryPlace=None,
                                pugoId=options.pugo_id.state,
                                pugoName=options.pugo_name.state,
                                pugoAddress=bpost.AddressType(
                                    streetName=hold_location.street_name,
                                    addressLineTwo=hold_location.address_line2,
                                    number=hold_location.street_number,
                                    box=None,
                                    postalCode=hold_location.postal_code,
                                    locality=hold_location.city,
                                    countryCode=hold_location.country_code,
                                ),
                                receiverName=recipient.contact,
                                receiverCompany=recipient.company_name,
                                requestedDeliveryDate=None,
                                shopHandlingInstruction=None,
                            )
                            if method == "atBpost"
                            else None
                        ),
                        at24_7=(
                            bpost.at24_7(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                weight=package.weight.G,
                                height=package.height.MM,
                                length=package.length.MM,
                                width=package.width.MM,
                                openingHours=None,
                                desiredDeliveryPlace=None,
                                parcelsDepotId=options.parcels_depot_id.state,
                                parcelsDepotName=options.parcels_depot_name.state,
                                parcelsDepotAddress=bpost.AddressType(
                                    streetName=hold_location.street_name,
                                    addressLineTwo=hold_location.address_line2,
                                    number=hold_location.street_number,
                                    box=None,
                                    postalCode=hold_location.postal_code,
                                    locality=hold_location.city,
                                    countryCode=hold_location.country_code,
                                ),
                            )
                            if method == "at24_7"
                            else None
                        ),
                        bpostOnAppointment=None,
                    )
                    if not is_international
                    else None
                ),
                internationalBox=(
                    bpost.InternationalBoxType(
                        international=(
                            bpost.InternationalDeliveryMethodType(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                receiver=bpost.Party(
                                    name=recipient.contact,
                                    company=recipient.company_name,
                                    address=bpost.AddressType(
                                        streetName=recipient.street_name,
                                        addressLineTwo=recipient.address_line2,
                                        number=recipient.street_number,
                                        box=None,
                                        postalCode=recipient.postal_code,
                                        locality=recipient.city,
                                        countryCode=recipient.country_code,
                                    ),
                                    emailAddress=recipient.email,
                                    phoneNumber=recipient.phone_number,
                                ),
                                parcelWeight=package.weight.G,
                                parcelHeight=package.height.MM,
                                parcelLength=package.length.MM,
                                parcelWidth=package.width.MM,
                                customsInfo=bpost.CustomsType(
                                    parcelValue=(
                                        customs.duty.declared_value
                                        or options.declared_value.state
                                    ),
                                    contentDescription=customs.content_description,
                                    shipmentType=provider_units.CustomsContentType.map(
                                        customs.content_type
                                    ).value,
                                    parcelReturnInstructions=(
                                        options.bpost_parcel_return_instructions.state
                                        or "RTS"
                                    ),
                                    privateAddress=customs.duty_billing_address.residential,
                                    currency=(
                                        customs.duty.currency or options.currency.state
                                    ),
                                    amtPostagePaidByAddresse=None,
                                ),
                                parcelContents=(
                                    bpost.ParcelContentDetails(
                                        parcelContent=[
                                            bpost.ParcelContentDetail(
                                                numberOfItemType=item.quantity,
                                                valueOfItem=item.value_amount,
                                                itemDescription=(
                                                    item.title or item.description
                                                ),
                                                nettoWeight=item.weight,
                                                hsTariffCode=(item.hs_code or item.sku),
                                                originOfGoods=item.origin_country,
                                            )
                                            for item in (
                                                package.items
                                                if any(package.items)
                                                else customs.commodities
                                            )
                                        ],
                                    )
                                    if (any(package.items) or any(customs.commodities))
                                    else None
                                ),
                            )
                            if method == "international"
                            else None
                        ),
                        atIntlHome=(
                            bpost.InternationalDeliveryMethodType(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                receiver=bpost.Party(
                                    name=recipient.contact,
                                    company=recipient.company_name,
                                    address=bpost.AddressType(
                                        streetName=recipient.street_name,
                                        addressLineTwo=recipient.address_line2,
                                        number=recipient.street_number,
                                        box=None,
                                        postalCode=recipient.postal_code,
                                        locality=recipient.city,
                                        countryCode=recipient.country_code,
                                    ),
                                    emailAddress=recipient.email,
                                    phoneNumber=recipient.phone_number,
                                ),
                                parcelWeight=package.weight.G,
                                parcelHeight=package.height.MM,
                                parcelLength=package.length.MM,
                                parcelWidth=package.width.MM,
                                customsInfo=bpost.CustomsType(
                                    parcelValue=(
                                        customs.duty.declared_value
                                        or options.declared_value.state
                                    ),
                                    contentDescription=customs.content_description,
                                    shipmentType=provider_units.CustomsContentType.map(
                                        customs.content_type
                                    ).value,
                                    parcelReturnInstructions=(
                                        options.bpost_parcel_return_instructions.state
                                        or "RTS"
                                    ),
                                    privateAddress=customs.duty_billing_address.residential,
                                    currency=(
                                        customs.duty.currency or options.currency.state
                                    ),
                                    amtPostagePaidByAddresse=None,
                                ),
                                parcelContents=(
                                    bpost.ParcelContentDetails(
                                        parcelContent=[
                                            bpost.ParcelContentDetail(
                                                numberOfItemType=item.quantity,
                                                valueOfItem=item.value_amount,
                                                itemDescription=(
                                                    item.title or item.description
                                                ),
                                                nettoWeight=item.weight,
                                                hsTariffCode=(item.hs_code or item.sku),
                                                originOfGoods=item.origin_country,
                                            )
                                            for item in (
                                                package.items
                                                if any(package.items)
                                                else customs.commodities
                                            )
                                        ],
                                    )
                                    if (any(package.items) or any(customs.commodities))
                                    else None
                                ),
                            )
                            if method == "atIntlHome"
                            else None
                        ),
                        atIntlPugo=(
                            bpost.atIntlPugo(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                receiver=bpost.Party(
                                    name=recipient.contact,
                                    company=recipient.company_name,
                                    address=bpost.AddressType(
                                        streetName=recipient.street_name,
                                        addressLineTwo=recipient.address_line2,
                                        number=recipient.street_number,
                                        box=None,
                                        postalCode=recipient.postal_code,
                                        locality=recipient.city,
                                        countryCode=recipient.country_code,
                                    ),
                                    emailAddress=recipient.email,
                                    phoneNumber=recipient.phone_number,
                                ),
                                parcelWeight=package.weight.G,
                                parcelHeight=package.height.MM,
                                parcelLength=package.length.MM,
                                parcelWidth=package.width.MM,
                                customsInfo=bpost.CustomsType(
                                    parcelValue=(
                                        customs.duty.declared_value
                                        or options.declared_value.state
                                    ),
                                    contentDescription=customs.content_description,
                                    shipmentType=provider_units.CustomsContentType.map(
                                        customs.content_type
                                    ).value,
                                    parcelReturnInstructions=(
                                        options.bpost_parcel_return_instructions.state
                                        or "RTS"
                                    ),
                                    privateAddress=customs.duty_billing_address.residential,
                                    currency=(
                                        customs.duty.currency or options.currency.state
                                    ),
                                    amtPostagePaidByAddresse=None,
                                ),
                                parcelContents=(
                                    bpost.ParcelContentDetails(
                                        parcelContent=[
                                            bpost.ParcelContentDetail(
                                                numberOfItemType=item.quantity,
                                                valueOfItem=item.value_amount,
                                                itemDescription=(
                                                    item.title or item.description
                                                ),
                                                nettoWeight=item.weight,
                                                hsTariffCode=(item.hs_code or item.sku),
                                                originOfGoods=item.origin_country,
                                            )
                                            for item in (
                                                package.items
                                                if any(package.items)
                                                else customs.commodities
                                            )
                                        ],
                                    )
                                    if (any(package.items) or any(customs.commodities))
                                    else None
                                ),
                                pugoId=options.bpost_pugo_id.state,
                                pugoName=options.bpost_pugo_name.state,
                                pugoAddress=bpost.AddressType(
                                    streetName=hold_location.street_name,
                                    addressLineTwo=hold_location.address_line2,
                                    number=hold_location.street_number,
                                    box=None,
                                    postalCode=hold_location.postal_code,
                                    locality=hold_location.city,
                                    countryCode=hold_location.country_code,
                                ),
                            )
                            if method == "atIntlPugo"
                            else None
                        ),
                        atIntlParcelDepot=(
                            bpost.atIntlParcelDepot(
                                product=service,
                                options=(
                                    bpost.OptionsType(
                                        infoDistributed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_distributed.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoNextDay=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_info_next_day.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_next_day.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        infoReminder=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_info_reminder.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        keepMeInformed=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                (
                                                    options.bpost_keep_me_informed.state
                                                    or options.email_notification.state
                                                )
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        automaticSecondPresentation=(
                                            bpost.automaticSecondPresentationType()
                                            if options.bpost_auto_second_presentation.state
                                            else None
                                        ),
                                        fragile=(
                                            bpost.FragileType()
                                            if options.bpost_fragile.state
                                            else None
                                        ),
                                        insured=(
                                            bpost.InsuranceType(
                                                basicInsurance=options.bpost_insured.state,
                                                additionalInsurance=None,
                                            )
                                            if options.bpost_insured.state is not None
                                            else None
                                        ),
                                        signed=(
                                            bpost.SignatureType()
                                            if options.bpost_signed.state
                                            else None
                                        ),
                                        timeSlotDelivery=(
                                            bpost.TimeSlotDeliveryType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                                value=options.bpost_time_slot_delivery.state,
                                            )
                                            if (
                                                options.bpost_time_slot_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        saturdayDelivery=(
                                            bpost.SaturdayDeliveryType()
                                            if options.bpost_saturday_delivery.state
                                            else None
                                        ),
                                        sundayDelivery=(
                                            bpost.SundayDeliveryType()
                                            if options.bpost_sunday_delivery.state
                                            else None
                                        ),
                                        sameDayDelivery=(
                                            bpost.NotificationType(
                                                language=settings.connection_config.lang.state,
                                                emailAddress=(
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                ),
                                                phoneNumber=(
                                                    options.sms_notification_to.state
                                                    or recipient.phone_number
                                                ),
                                            )
                                            if (
                                                options.bpost_same_day_delivery.state
                                                and (
                                                    options.email_notification_to.state
                                                    or recipient.email
                                                    or options.sms_notification_to.state
                                                    or recipient.phone_number
                                                )
                                            )
                                            else None
                                        ),
                                        cod=(
                                            bpost.CodType(
                                                codAmount=options.bpost_cod.state,
                                                iban=None,
                                                bic=None,
                                            )
                                            if options.bpost_cod.state is not None
                                            else None
                                        ),
                                        preferredDeliveryWindow=options.bpost_preferred_delivery_window.state,
                                        fullService=(
                                            bpost.FullServiceType()
                                            if options.bpost_full_service.state
                                            else None
                                        ),
                                        doorStepPlusService=(
                                            bpost.DoorStepPlusServiceType()
                                            if options.bpost_door_step_plus_service.state
                                            else None
                                        ),
                                        ultraLateInEveningDelivery=(
                                            bpost.UltraLateInEveningDelivery()
                                            if options.bpost_ultra_late_in_evening_delivery.state
                                            else None
                                        ),
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                receiver=bpost.Party(
                                    name=recipient.contact,
                                    company=recipient.company_name,
                                    address=bpost.AddressType(
                                        streetName=recipient.street_name,
                                        addressLineTwo=recipient.address_line2,
                                        number=recipient.street_number,
                                        box=None,
                                        postalCode=recipient.postal_code,
                                        locality=recipient.city,
                                        countryCode=recipient.country_code,
                                    ),
                                    emailAddress=recipient.email,
                                    phoneNumber=recipient.phone_number,
                                ),
                                parcelWeight=package.weight.G,
                                parcelHeight=package.height.MM,
                                parcelLength=package.length.MM,
                                parcelWidth=package.width.MM,
                                customsInfo=bpost.CustomsType(
                                    parcelValue=(
                                        customs.duty.declared_value
                                        or options.declared_value.state
                                    ),
                                    contentDescription=customs.content_description,
                                    shipmentType=provider_units.CustomsContentType.map(
                                        customs.content_type
                                    ).value,
                                    parcelReturnInstructions=(
                                        options.bpost_parcel_return_instructions.state
                                        or "RTS"
                                    ),
                                    privateAddress=customs.duty_billing_address.residential,
                                    currency=(
                                        customs.duty.currency or options.currency.state
                                    ),
                                    amtPostagePaidByAddresse=None,
                                ),
                                parcelContents=(
                                    bpost.ParcelContentDetails(
                                        parcelContent=[
                                            bpost.ParcelContentDetail(
                                                numberOfItemType=item.quantity,
                                                valueOfItem=item.value_amount,
                                                itemDescription=(
                                                    item.title or item.description
                                                ),
                                                nettoWeight=item.weight,
                                                hsTariffCode=(item.hs_code or item.sku),
                                                originOfGoods=item.origin_country,
                                            )
                                            for item in (
                                                package.items
                                                if any(package.items)
                                                else customs.commodities
                                            )
                                        ],
                                    )
                                    if (any(package.items) or any(customs.commodities))
                                    else None
                                ),
                                parcelsDepotId=options.bpost_parcels_depot_id.state,
                                parcelsDepotName=options.bpost_parcels_depot_name.state,
                                parcelsDepotAddress=bpost.AddressType(
                                    streetName=hold_location.street_name,
                                    addressLineTwo=hold_location.address_line2,
                                    number=hold_location.street_number,
                                    box=None,
                                    postalCode=hold_location.postal_code,
                                    locality=hold_location.city,
                                    countryCode=hold_location.country_code,
                                ),
                            )
                            if method == "atIntlParcelDepot"
                            else None
                        ),
                    )
                    if is_international
                    else None
                ),
                remark=lib.text(payload.reference, max=50),
                additionalCustomerReference=None,
            )
            for package in packages
        ],
    )

    return lib.Serializable(
        request,
        lambda req: lib.to_xml(
            req,
            prefixes=dict(
                OrderType="tns",
                sender_children="common",
                receiver_children="common",
                options_children="common",
                pugoAddress_children="common",
                parcelsDepotAddress_children="common",
                nationalBox_children="",
                internationalBox_children="international",
            ),
            namespacedef_=(
                'xmlns="http://schema.post.be/shm/deepintegration/v5/national"'
                ' xmlns:common="http://schema.post.be/shm/deepintegration/v5/common"'
                ' xmlns:tns="http://schema.post.be/shm/deepintegration/v5/"'
                ' xmlns:international="http://schema.post.be/shm/deepintegration/v5/international"'
                ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ' xsi:schemaLocation="http://schema.post.be/shm/deepintegration/v5/"'
            ),
        ).replace("OrderType", "order"),
        dict(
            reference=reference,
            label_format=label_format,
            label_header=label_header,
        ),
    )
