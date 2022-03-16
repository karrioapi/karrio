import time
from typing import Tuple, List
from usps_lib.evs_first_class_mail_intl_response import eVSFirstClassMailIntlResponse
from usps_lib.evs_first_class_mail_intl_request import (
    eVSFirstClassMailIntlRequest,
    ImageParametersType,
    ShippingContentsType,
    ItemDetailType,
    ExtraServicesType,
)
from karrio.core.utils import Serializable, Element, XP, DF, Location
from karrio.core.units import CustomsInfo, Packages, Options, Weight, WeightUnit
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    Message,
    Customs,
)
from karrio.providers.usps_international.units import (
    LabelFormat,
    ShipmentOption,
    ContentType,
)
from karrio.providers.usps_international.error import parse_error_response
from karrio.providers.usps_international.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, errors


def _extract_details(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.to_object(eVSFirstClassMailIntlResponse, response)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.BarcodeNumber,
        shipment_identifier=shipment.BarcodeNumber,
        docs=Documents(label=shipment.LabelImage),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[eVSFirstClassMailIntlRequest]:
    package = Packages(payload.parcels, max_weight=Weight(70, WeightUnit.LB)).single
    options = Options(payload.options, ShipmentOption)

    label_format = LabelFormat[payload.label_type or "usps_6_x_4_label"].value
    extra_services = [
        getattr(option, "value", option)
        for key, option in options
        if key in ShipmentOption and "usps_option" not in key
    ]
    customs = CustomsInfo(payload.customs or Customs(commodities=[]))

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
        FromZip5=Location(payload.shipper.postal_code).as_zip5,
        FromZip4=Location(payload.shipper.postal_code).as_zip4 or "",
        FromPhone=payload.shipper.phone_number,
        ToName=None,
        ToFirstName=payload.recipient.person_name,
        ToLastName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line2,
        ToAddress2=payload.recipient.address_line1,
        ToAddress3=None,
        ToCity=payload.recipient.city,
        ToProvince=Location(
            payload.recipient.state_code, country=payload.recipient.country_code
        ).as_state_name,
        ToCountry=Location(payload.recipient.country_code).as_country_name,
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
                    NetPounds=Weight(
                        item.weight, WeightUnit[item.weight_unit or "LB"]
                    ).LB,
                    NetOunces=Weight(
                        item.weight, WeightUnit[item.weight_unit or "LB"]
                    ).OZ,
                    HSTariffNumber=item.sku,
                    CountryOfOrigin=Location(item.origin_country).as_country_name,
                )
                for item in payload.customs.commodities
            ]
        ),
        Postage=None,
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        ContentType=ContentType[customs.content_type or "other"].value,
        ContentTypeOther=customs.content_description or "N/A",
        Agreement=("N" if customs.certify else "Y"),
        Comments=customs.content_description,
        LicenseNumber=customs.license_number,
        CertificateNumber=customs.certificate_number,
        InvoiceNumber=customs.invoice,
        ImageType="PDF",
        ImageLayout="ALLINONEFILE",
        CustomerRefNo=None,
        CustomerRefNo2=None,
        POZipCode=None,
        LabelDate=DF.fdatetime(
            (options.shipment_date or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        HoldForManifest=None,
        EELPFC=customs.eel_pfc,
        Container=None,
        Length=package.length.IN,
        Width=package.width.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        ExtraServices=(
            ExtraServicesType(ExtraService=[s for s in extra_services])
            if any(extra_services)
            else None
        ),
        PriceOptions=None,
        ActionCode=None,
        OptOutOfSPE=None,
        PermitNumber=None,
        AccountZipCode=None,
        Machinable=(options.usps_option_machinable_item or False),
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        RemainingBarcodes=None,
        ChargebackCode=None,
    )

    return Serializable(request, XP.export)
