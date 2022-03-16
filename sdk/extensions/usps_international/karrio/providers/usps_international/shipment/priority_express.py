import time
from typing import Tuple, List
from usps_lib.evs_express_mail_intl_response import eVSExpressMailIntlResponse
from usps_lib.evs_express_mail_intl_request import (
    eVSExpressMailIntlRequest,
    ImageParametersType,
    ShippingContentsType,
    ItemDetailType,
)
from karrio.core.utils import Serializable, Element, XP, DF, Location
from karrio.core.units import (
    CustomsInfo,
    Packages,
    Options,
    Weight,
    WeightUnit,
    CompleteAddress,
)
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    Message,
    Customs,
    Address,
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
    shipment = XP.to_object(eVSExpressMailIntlResponse, response)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.BarcodeNumber,
        shipment_identifier=shipment.BarcodeNumber,
        docs=Documents(label=shipment.LabelImage),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[eVSExpressMailIntlRequest]:
    package = Packages(payload.parcels, max_weight=Weight(70, WeightUnit.LB)).single
    options = Options(payload.options, ShipmentOption)

    label_format = LabelFormat[payload.label_type or "usps_6_x_4_label"].value
    customs = CustomsInfo(payload.customs or Customs(commodities=[]))
    insurance = getattr(
        (options["usps_insurance_express_mail_international"]),
        "value",
        options.insurance,
    )
    # Gets the first provided non delivery option or default to "RETURN"
    non_delivery = next(
        (option.value for name, option in options if "non_delivery" in name), "RETURN"
    )
    redirect_address = CompleteAddress.map(
        Address(**(options["usps_option_redirect_non_delivery"] or {}))
    )

    request = eVSExpressMailIntlRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Option=None,
        Revision=2,
        ImageParameters=ImageParametersType(ImageParameter=label_format),
        FromFirstName=customs.signer or payload.shipper.person_name or "N/A",
        FromLastName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line2,
        FromAddress2=payload.shipper.address_line1,
        FromUrbanization=None,
        FromCity=payload.shipper.city,
        FromZip5=Location(payload.shipper.postal_code).as_zip5,
        FromZip4=Location(payload.shipper.postal_code).as_zip4 or "",
        FromPhone=payload.shipper.phone_number,
        FromCustomsReference=None,
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
        ImportersReferenceNumber=None,
        NonDeliveryOption=non_delivery,
        RedirectName=redirect_address.person_name,
        RedirectEmail=redirect_address.email,
        RedirectSMS=redirect_address.phone_number,
        RedirectAddress=redirect_address.address_line,
        RedirectCity=redirect_address.city,
        RedirectState=redirect_address.state_code,
        RedirectZipCode=redirect_address.postal_code,
        RedirectZip4=Location(redirect_address.postal_code).as_zip4 or "",
        Container=None,
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
                for item in customs.commodities
            ]
        ),
        InsuredAmount=insurance,
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        ContentType=ContentType[customs.content_type or "other"].value,
        ContentTypeOther=customs.content_description or "N/A",
        Agreement=("Y" if customs.certify else "N"),
        Comments=customs.content_description,
        LicenseNumber=customs.license_number,
        CertificateNumber=customs.certificate_number,
        InvoiceNumber=customs.invoice,
        ImageType="PDF",
        ImageLayout="ALLINONEFILE",
        InsuredNumber=None,
        CustomerRefNo=None,
        CustomerRefNo2=None,
        POZipCode=None,
        LabelDate=DF.fdatetime(
            (options.shipment_date or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        EMCAAccount=None,
        HoldForManifest=None,
        EELPFC=customs.eel_pfc,
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
        Machinable=options.usps_option_machinable_item or False,
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
    )

    return Serializable(request, XP.export)
