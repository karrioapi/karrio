from usps_lib.evs_response import eVSResponse
from usps_lib.evs_request import (
    eVSRequest,
    ImageParametersType,
    LabelSequenceType,
    ShippingContentsType,
    ItemDetailType,
    ExtraServicesType,
)

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps.error as provider_error
import karrio.providers.usps.units as provider_units
import karrio.providers.usps.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, errors


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(eVSResponse, response)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.BarcodeNumber,
        shipment_identifier=shipment.BarcodeNumber,
        docs=models.Documents(label=shipment.LabelImage),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[eVSRequest]:
    if (
        payload.shipper.country_code is not None
        and payload.shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    if (
        payload.recipient.country_code is not None
        and payload.recipient.country_code != units.Country.US.name
    ):
        raise errors.DestinationNotServicedError(payload.recipient.country_code)

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

    request = eVSRequest(
        USERID=settings.username,
        Option=None,
        Revision="1",
        ImageParameters=ImageParametersType(
            ImageParameter=label_format,
            LabelSequence=LabelSequenceType(PackageNumber=1, TotalPackages=1),
        ),
        FromName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line2,
        FromAddress2=payload.shipper.address_line1,
        FromCity=payload.shipper.city,
        FromState=payload.shipper.state_code,
        FromZip5=lib.to_zip5(payload.shipper.postal_code) or "",
        FromZip4=lib.to_zip4(payload.shipper.postal_code) or "",
        FromPhone=payload.shipper.phone_number,
        POZipCode=None,
        AllowNonCleansedOriginAddr=False,
        ToName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line2,
        ToAddress2=payload.recipient.address_line1,
        ToCity=payload.recipient.city,
        ToState=payload.recipient.state_code,
        ToZip5=lib.to_zip5(payload.recipient.postal_code) or "",
        ToZip4=lib.to_zip4(payload.recipient.postal_code) or "",
        ToPhone=payload.recipient.phone_number,
        POBox=None,
        ToContactPreference=None,
        ToContactMessaging=payload.recipient.email,
        ToContactEmail=payload.recipient.email,
        AllowNonCleansedDestAddr=False,
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
        ShipDate=options.shipment_date.state,
        CustomerRefNo=None,
        ExtraServices=(
            ExtraServicesType(
                ExtraService=[option.code for _, option in options.items()]
            )
            if any(options.items())
            else None
        ),
        CRID=settings.customer_registration_id,
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        SenderName=(payload.shipper.person_name or payload.shipper.company_name),
        SenderEMail=payload.shipper.email,
        RecipientName=(payload.recipient.person_name or payload.recipient.company_name),
        RecipientEMail=payload.recipient.email,
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
            ShippingContentsType(
                ItemDetail=[
                    ItemDetailType(
                        Description=item.description,
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
