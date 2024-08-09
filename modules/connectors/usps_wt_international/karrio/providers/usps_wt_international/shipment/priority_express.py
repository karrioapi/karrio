from karrio.schemas.usps_wt.evs_express_mail_intl_response import (
    eVSExpressMailIntlResponse,
)
from karrio.schemas.usps_wt.evs_express_mail_intl_request import (
    eVSExpressMailIntlRequest,
    ImageParametersType,
    ShippingContentsType,
    ItemDetailType,
)

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_wt_international.error as provider_error
import karrio.providers.usps_wt_international.units as provider_units
import karrio.providers.usps_wt_international.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    details = (
        _extract_details(response, settings)
        if len(lib.find_element("BarcodeNumber", response)) > 0
        else None
    )

    return details, errors


def _extract_details(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(eVSExpressMailIntlResponse, response)

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
    customs = lib.to_customs_info(payload.customs or models.Customs(commodities=[]))
    redirect_address = lib.to_address(
        models.Address(**(options.usps_option_redirect_non_delivery.state or {}))
    )

    request = eVSExpressMailIntlRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Option=None,
        Revision=2,
        ImageParameters=ImageParametersType(ImageParameter=label_format),
        FromFirstName=customs.signer or shipper.person_name or "N/A",
        FromLastName=shipper.person_name,
        FromFirm=shipper.company_name or "N/A",
        FromAddress1=shipper.address_line2 or "",
        FromAddress2=shipper.address_line1,
        FromUrbanization=None,
        FromCity=shipper.city,
        FromZip5=lib.to_zip5(shipper.postal_code),
        FromZip4=lib.to_zip4(shipper.postal_code) or "",
        FromPhone=shipper.phone_number,
        FromCustomsReference=None,
        ToName=None,
        ToFirstName=recipient.person_name,
        ToLastName=recipient.person_name,
        ToFirm=recipient.company_name or "N/A",
        ToAddress1=recipient.address_line2 or "",
        ToAddress2=recipient.address_line1,
        ToAddress3=None,
        ToCity=recipient.city,
        ToProvince=lib.to_state_name(
            recipient.state_code, country=recipient.country_code
        ),
        ToCountry=lib.to_country_name(recipient.country_code),
        ToPostalCode=recipient.postal_code,
        ToPOBoxFlag=None,
        ToPhone=recipient.phone_number,
        ToFax=None,
        ToEmail=recipient.email,
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
                    Description=lib.text(item.description or item.title or "N/A"),
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
        InsuredAmount=provider_units.ShippingOption.insurance_from(
            options, "express_mail"
        ),
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        ContentType=provider_units.ContentType[customs.content_type or "other"].value,
        ContentTypeOther=customs.content_description or "N/A",
        Agreement=("Y" if customs.certify else "N"),
        Comments=customs.content_description,
        LicenseNumber=customs.options.license_number.state,
        CertificateNumber=customs.options.certificate_number.state,
        InvoiceNumber=customs.invoice,
        ImageType="PDF",
        ImageLayout="ALLINONEFILE",
        InsuredNumber=None,
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
        LabelTime=None,
        MeterPaymentFlag=None,
        ActionCode=None,
        OptOutOfSPE=None,
        PermitNumber=None,
        AccountZipCode=None,
        ImportersReferenceType=None,
        ImportersTelephoneNumber=None,
        ImportersFaxNumber=None,
        ImportersEmail=None,
        Machinable=options.usps_option_machinable_item.state or False,
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
    )

    return lib.Serializable(request, lib.to_xml)
