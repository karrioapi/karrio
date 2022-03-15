import time
from typing import Tuple, List
from usps_lib.evs_gxg_get_label_response import eVSGXGGetLabelResponse
from usps_lib.evs_gxg_get_label_request import (
    eVSGXGGetLabelRequest,
    ShippingContentsType,
    ItemDetailType,
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
    ShipmentOption,
    ContentType,
    PackagingType,
    Incoterm,
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
    shipment = XP.to_object(eVSGXGGetLabelResponse, response)
    tracking_number = shipment.USPSBarcodeNumber or shipment.FedExBarcodeNumber

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        docs=Documents(label=shipment.LabelImage),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[eVSGXGGetLabelRequest]:
    package = Packages(payload.parcels, max_weight=Weight(70, WeightUnit.LB)).single
    options = Options(payload.options, ShipmentOption)

    customs = CustomsInfo(payload.customs or Customs(commodities=[]))
    incoterm = Incoterm[customs.incoterm or "OTHER"].value
    insurance = getattr(
        (options.usps_insurance_global_express_guaranteed), "value", options.insurance
    )

    request = eVSGXGGetLabelRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Option=None,
        Revision=2,
        ImageParameters=None,
        FromFirstName=(customs.signer or payload.shipper.person_name or "N/A"),
        FromMiddleInitial=None,
        FromLastName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line1,
        FromAddress2=payload.shipper.address_line2,
        FromUrbanization=None,
        FromCity=payload.shipper.city,
        FromState=Location(payload.shipper.state_code, country="US").as_state_name,
        FromZIP5=Location(payload.shipper.postal_code).as_zip5,
        FromZIP4=Location(payload.shipper.postal_code).as_zip4,
        FromPhone=payload.shipper.phone_number,
        ShipFromZIP=None,
        ToFirstName=None,
        ToLastName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line1,
        ToAddress2=payload.recipient.address_line2,
        ToAddress3=None,
        ToPostalCode=payload.recipient.postal_code,
        ToPhone=payload.recipient.phone_number,
        RecipientEMail=payload.recipient.email,
        ToDPID="000",  # supposedly required test and find a solution
        ToProvince=payload.recipient.state_code,
        ToTaxID=(payload.recipient.federal_tax_id or payload.recipient.state_tax_id),
        Container=PackagingType[package.packaging_type or "package"].value,
        ContentType=("DOCUMENTS" if package.parcel.is_document else "NON-DOC"),
        ShippingContents=ShippingContentsType(
            ItemDetail=[
                ItemDetailType(
                    Description=item.description,
                    Commodity=item.description or "N/A",
                    Quantity=item.quantity,
                    UnitValue=item.value_amount,
                    NetPounds=Weight(
                        item.weight, WeightUnit[item.weight_unit or "LB"]
                    ).LB,
                    NetOunces=Weight(
                        item.weight, WeightUnit[item.weight_unit or "LB"]
                    ).OZ,
                    UnitOfMeasure=None,
                    HSTariffNumber=item.sku,
                    CountryofManufacture=Location(item.origin_country).as_country_name,
                )
                for item in customs.commodities
            ]
        ),
        PurposeOfShipment=ContentType[customs.content_type or "other"].value,
        PartiesToTransaction=None,
        Agreement=("N" if customs.certify else "Y"),
        Postage=None,
        InsuredValue=insurance,
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        Length=package.length.IN,
        Width=package.width.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        Shape=None,
        CIRequired=customs.commercial_invoice,
        InvoiceDate=DF.fdatetime(customs.invoice_date, output_format="%m/%d/%Y"),
        InvoiceNumber=customs.invoice,
        CustomerOrderNumber=None,
        CustOrderNumber=None,
        TermsDelivery=incoterm,
        TermsDeliveryOther=(
            (customs.incoterm or incoterm) if incoterm == "OTHER" else None
        ),
        PackingCost=None,
        CountryUltDest=Location(payload.recipient.country_code).as_country_name,
        CIAgreement=customs.commercial_invoice,
        ImageType="PDF",
        ImageLayout=None,
        CustomerRefNo=None,
        CustomerRefNo2=None,
        ShipDate=DF.fdatetime(
            (options.shipment_date or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        HoldForManifest=None,
        PriceOptions=None,
        CommercialShipment=customs.commercial_invoice,
        BuyerRecipient=(
            customs.commercial_invoice or None
        ),  # Consider recipient as buyer for commercial shipment
        TermsPayment=("Net 50" if customs.commercial_invoice else None),
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
        OverrideMID=None,
        ChargebackCode=None,
    )

    return Serializable(request, XP.export)
