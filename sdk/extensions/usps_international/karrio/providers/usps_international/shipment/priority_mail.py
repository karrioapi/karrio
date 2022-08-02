from usps_lib.evs_priority_mail_intl_response import eVSPriorityMailIntlResponse
from usps_lib.evs_priority_mail_intl_request import (
    eVSPriorityMailIntlRequest,
    ImageParametersType,
    ShippingContentsType,
    ItemDetailType,
    ExtraServicesType,
)

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_international.error as provider_error
import karrio.providers.usps_international.units as provider_units
import karrio.providers.usps_international.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, errors


def _extract_details(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(eVSPriorityMailIntlResponse, response)

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
) -> lib.Serializable[eVSPriorityMailIntlRequest]:
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
        max_weight=units.Weight(70, units.WeightUnit.LB),
    ).single
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    label_format = provider_units.LabelFormat[
        payload.label_type or "usps_6_x_4_label"
    ].value
    insurance = provider_units.ShippingOption.insurance_from(options, "priority_mail")
    customs = lib.to_customs_info(payload.customs or models.Customs(commodities=[]))
    redirect_address = lib.to_address(
        models.Address(**(options.usps_option_redirect_non_delivery.state or {}))
    )

    request = eVSPriorityMailIntlRequest(
        USERID=settings.username,
        Option=None,
        Revision=2,
        ImageParameters=ImageParametersType(ImageParameter=label_format),
        FromFirstName=customs.signer or payload.shipper.person_name or "N/A",
        FromMiddleInitial=None,
        FromLastName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line2,
        FromAddress2=payload.shipper.address_line1,
        FromUrbanization=None,
        FromCity=payload.shipper.city,
        FromState=lib.to_state_name(payload.shipper.state_code, country="US"),
        FromZip5=lib.to_zip5(payload.shipper.postal_code),
        FromZip4=lib.to_zip4(payload.shipper.postal_code) or "",
        FromPhone=payload.shipper.phone_number,
        FromCustomsReference=None,
        ToName=None,
        ToFirstName=payload.recipient.person_name,
        ToLastName=None,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line2,
        ToAddress2=payload.recipient.address_line1,
        ToAddress3=None,
        ToCity=payload.recipient.city,
        ToProvince=lib.to_state_name(
            payload.recipient.state_code, country=payload.recipient.country_code
        ),
        ToCountry=lib.to_country_name(payload.recipient.country_code),
        ToPostalCode=payload.recipient.postal_code,
        ToPOBoxFlag=None,
        ToPhone=payload.recipient.phone_number,
        ToFax=None,
        ToEmail=payload.recipient.email,
        ImportersReferenceNumber=None,
        NonDeliveryOption=provider_units.ShippingOption.non_delivery_from(options),
        RedirectName=redirect_address.person_name,
        RedirectEmail=redirect_address.email,
        RedirectSMS=redirect_address.phone_number,
        RedirectAddress=redirect_address.address_line,
        RedirectCity=redirect_address.city,
        RedirectState=redirect_address.state_code,
        RedirectZipCode=redirect_address.postal_code,
        RedirectZip4=lib.to_zip4(redirect_address.postal_code) or "",
        Container=None,
        ShippingContents=ShippingContentsType(
            ItemDetail=[
                ItemDetailType(
                    Description=item.description,
                    Quantity=item.quantity,
                    Value=item.value_amount,
                    NetPounds=units.Weight(
                        item.weight, units.WeightUnit[item.weight_unit or "LB"]
                    ).LB,
                    NetOunces=units.Weight(
                        item.weight, units.WeightUnit[item.weight_unit or "LB"]
                    ).OZ,
                    HSTariffNumber=item.hs_code or item.sku,
                    CountryOfOrigin=lib.to_country_name(item.origin_country),
                )
                for item in customs.commodities
            ]
        ),
        Insured=("N" if insurance is None else "Y"),
        InsuredAmount=insurance,
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        ContentType=provider_units.ContentType[customs.content_type or "other"].value,
        ContentTypeOther=customs.content_description or "N/A",
        Agreement=("N" if customs.certify else "Y"),
        Comments=customs.content_description,
        LicenseNumber=customs.options.license_number.state,
        CertificateNumber=customs.options.certificate_number.state,
        InvoiceNumber=customs.invoice,
        ImageType="PDF",
        ImageLayout="ALLINONEFILE",
        CustomerRefNo=None,
        CustomerRefNo2=None,
        POZipCode=None,
        LabelDate=lib.fdatetime(
            (options.shipment_date.state or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        EMCAAccount=None,
        HoldForManifest=None,
        EELPFC=customs.options.eel_pfc.state,
        PriceOptions=None,
        Length=package.length.IN,
        Width=package.width.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        ExtraServices=(
            ExtraServicesType(
                ExtraService=[option.code for _, option in options.items()]
            )
            if any(options.items())
            else None
        ),
        ActionCode=None,
        OptOutOfSPE=None,
        PermitNumber=None,
        AccountZipCode=None,
        ImportersReferenceType=None,
        ImportersTelephoneNumber=None,
        ImportersFaxNumber=None,
        ImportersEmail=None,
        Machinable=(options.usps_option_machinable_item.state or False),
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        ChargebackCode=None,
    )

    return lib.Serializable(request, lib.to_xml)
