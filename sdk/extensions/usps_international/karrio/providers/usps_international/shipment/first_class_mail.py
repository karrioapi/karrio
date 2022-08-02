from usps_lib.evs_first_class_mail_intl_response import eVSFirstClassMailIntlResponse
from usps_lib.evs_first_class_mail_intl_request import (
    eVSFirstClassMailIntlRequest,
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
    shipment = lib.to_object(eVSFirstClassMailIntlResponse, response)

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
) -> lib.Serializable[eVSFirstClassMailIntlRequest]:
    package = lib.to_packages(
        payload.parcels,
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

    request = eVSFirstClassMailIntlRequest(
        USERID=settings.username,
        Option=None,
        Revision=2,
        ImageParameters=ImageParametersType(ImageParameter=label_format),
        FromFirstName=customs.signer or payload.shipper.person_name,
        FromLastName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line2,
        FromAddress2=payload.shipper.address_line1,
        FromUrbanization=None,
        FromCity=payload.shipper.city,
        FromZip5=lib.to_zip5(payload.shipper.postal_code),
        FromZip4=lib.to_zip4(payload.shipper.postal_code) or "",
        FromPhone=payload.shipper.phone_number,
        ToName=None,
        ToFirstName=payload.recipient.person_name,
        ToLastName=payload.recipient.person_name,
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
        FirstClassMailType=None,
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
                for item in payload.customs.commodities
            ]
        ),
        Postage=None,
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
        HoldForManifest=None,
        EELPFC=customs.options.eel_pfc.state,
        Container=None,
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
        PriceOptions=None,
        ActionCode=None,
        OptOutOfSPE=None,
        PermitNumber=None,
        AccountZipCode=None,
        Machinable=(options.usps_option_machinable_item.state or False),
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        RemainingBarcodes=None,
        ChargebackCode=None,
    )

    return lib.Serializable(request, lib.to_xml)
