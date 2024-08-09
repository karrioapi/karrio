import karrio.schemas.usps_wt.evs_request as usps
import karrio.schemas.usps_wt.evs_response as shipping

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_wt.error as provider_error
import karrio.providers.usps_wt.units as provider_units
import karrio.providers.usps_wt.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element], settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    details = (
        _extract_details(response, settings)
        if len(lib.find_element("BarcodeNumber", response)) > 0
        else None
    )

    return details, errors


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.eVSResponse, response)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.BarcodeNumber,
        shipment_identifier=shipment.BarcodeNumber,
        docs=models.Documents(label=shipment.LabelImage),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(shipment.BarcodeNumber),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    if (
        shipper.country_code is not None
        and shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(shipper.country_code)

    if (
        recipient.country_code is not None
        and recipient.country_code != units.Country.US.name
    ):
        raise errors.DestinationNotServicedError(recipient.country_code)

    package = lib.to_packages(
        payload.parcels, package_option_type=provider_units.ShippingOption
    ).single
    service = provider_units.ServiceType.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    customs = lib.to_customs_info(payload.customs or models.Customs(commodities=[]))
    label_format = provider_units.LabelFormat[
        payload.label_type or "usps_6_x_4_label"
    ].value
    redirect_address = models.Address(
        **(options.usps_option_redirect_non_delivery.state or {})
    )

    request = usps.eVSRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Option=None,
        Revision="1",
        ImageParameters=usps.ImageParametersType(
            ImageParameter=label_format,
            LabelSequence=usps.LabelSequenceType(PackageNumber=1, TotalPackages=1),
        ),
        FromName=shipper.person_name,
        FromFirm=shipper.company_name or "N/A",
        FromAddress1=shipper.address_line2 or "",
        FromAddress2=shipper.street,
        FromCity=shipper.city,
        FromState=shipper.state_code,
        FromZip5=lib.to_zip5(shipper.postal_code) or "",
        FromZip4=lib.to_zip4(shipper.postal_code) or "",
        FromPhone=provider_utils.parse_phone_number(shipper.phone_number),
        POZipCode=None,
        AllowNonCleansedOriginAddr=(
            options.usps_option_allow_non_cleansed_origin_addr.state
            if options.usps_option_allow_non_cleansed_origin_addr.state is not None
            else True
        ),
        ToName=recipient.person_name,
        ToFirm=recipient.company_name or "N/A",
        ToAddress1=recipient.address_line2 or "",
        ToAddress2=recipient.street,
        ToCity=recipient.city,
        ToState=recipient.state_code,
        ToZip5=lib.to_zip5(recipient.postal_code) or "",
        ToZip4=lib.to_zip4(recipient.postal_code) or "",
        ToPhone=provider_utils.parse_phone_number(recipient.phone_number),
        POBox=None,
        ToContactPreference=None,
        ToContactMessaging=recipient.email,
        ToContactEmail=recipient.email,
        AllowNonCleansedDestAddr=(
            lib.to_json(options.usps_option_allow_non_cleansed_dest_addr.state)
            if options.usps_option_allow_non_cleansed_dest_addr.state is not None
            else True
        ),
        WeightInOunces=package.weight.OZ,
        ServiceType=service,
        Container=provider_units.PackagingType[
            package.packaging_type or "variable"
        ].value,
        Width=package.width.IN,
        Length=package.length.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        Machinable=options.usps_option_machinable_item.state,
        ProcessingCategory=None,
        PriceOptions=None,
        InsuredAmount=provider_units.ShippingOption.insurance_from(options),
        AddressServiceRequested=None,
        ExpressMailOptions=None,
        ShipDate=lib.fdatetime(
            (options.shipment_date.state or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        CustomerRefNo=None,
        # ExtraServices=(
        #     usps.ExtraServicesType(
        #         ExtraService=[option.code for _, option in options.items()]
        #     )
        #     if any(options.items())
        #     else None
        # ),
        CRID=settings.customer_registration_id,
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        SenderName=shipper.contact,
        SenderEMail=shipper.email,
        RecipientName=recipient.contact,
        RecipientEMail=recipient.email,
        ReceiptOption="SEPARATE PAGE",
        ImageType="PDF",
        HoldForManifest=None,
        NineDigitRoutingZip=None,
        ShipInfo=options.usps_option_ship_info.state,
        CarrierRelease=None,
        DropOffTime=None,
        ReturnCommitments=None,
        PrintCustomerRefNo=None,
        Content=None,
        ShippingContents=(
            usps.ShippingContentsType(
                ItemDetail=[
                    usps.ItemDetailType(
                        Description=lib.text(item.description or item.title or "N/A"),
                        Quantity=item.quantity,
                        Value=item.value_amount,
                        NetPounds=0,
                        NetOunces=units.Weight(
                            item.weight, units.WeightUnit[item.weight_unit or "LB"]
                        ).OZ,
                        HSTariffNumber=item.hs_code or item.sku,
                        CountryOfOrigin=lib.to_country_name(item.origin_country),
                    )
                    for item in customs.commodities
                ]
            )
            if payload.customs is not None
            else None
        ),
        CustomsContentType=(
            provider_units.ContentType[customs.content_type or "other"].value
            if payload.customs is not None
            else None
        ),
        ContentComments=None,
        RestrictionType=None,
        RestrictionComments=None,
        AESITN=customs.options.aes.state,
        ImportersReference=None,
        ImportersContact=None,
        ExportersReference=None,
        ExportersContact=None,
        InvoiceNumber=customs.invoice,
        LicenseNumber=customs.options.license_number.state,
        CertificateNumber=customs.options.certificate_number.state,
        NonDeliveryOption=provider_units.ShippingOption.non_delivery_from(options),
        AltReturnAddress1=redirect_address.address_line1,
        AltReturnAddress2=redirect_address.address_line2,
        AltReturnAddress3=None,
        AltReturnAddress4=None,
        AltReturnAddress5=None,
        AltReturnAddress6=None,
        AltReturnCountry=None,
        LabelImportType=None,
        ChargebackCode=None,
        TrackingRetentionPeriod=None,
    )

    return lib.Serializable(request, lib.to_xml)
