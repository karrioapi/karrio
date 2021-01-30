from typing import Tuple, List
from usps_lib.evs_request import (
    eVSRequest,
    ImageParametersType,
    LabelSequenceType,
)
from purplship.core.units import Packages
from purplship.core.utils import Serializable
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

from purplship.providers.usps.units import RateService, Container, LabelFormat
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.utils import Settings


def parse_shipment_response(response: dict, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    service = RateService[payload.service].value
    packages = Packages(payload.parcels)
    package = packages[0]

    request = eVSRequest(
        USERID=settings.username,
        Option=None,
        Revision="1",
        ImageParameters=ImageParametersType(
            ImageParameter=LabelFormat.usps_4_x_6_label.value,
            XCoordinate=None,
            YCoordinate=None,
            LabelSequence=LabelSequenceType(
                PackageNumber=1,
                TotalPackages=len(packages)
            ) if len(packages) > 1 else None
        ),
        FromName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name,
        FromAddress1=payload.shipper.address_line1,
        FromAddress2=payload.shipper.address_line2,
        FromCity=payload.shipper.city,
        FromState=payload.shipper.state_code,
        FromZip5=payload.shipper.postal_code,
        FromZip4=None,
        FromPhone=payload.shipper.phone_number,
        POZipCode=None,
        AllowNonCleansedOriginAddr=None,
        ToName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name,
        ToAddress1=payload.recipient.address_line1,
        ToAddress2=payload.recipient.address_line2,
        ToCity=payload.recipient.city,
        ToState=payload.recipient.state_code,
        ToZip5=payload.recipient.postal_code,
        ToZip4=None,
        ToPhone=payload.recipient.phone_number,
        POBox=None,
        ToContactMessaging=None,
        ToContactEmail=None,
        AllowNonCleansedDestAddr=None,
        WeightInOunces=package.weight.OZ,
        ServiceType=service,
        Container=Container[package.packaging_type].value,
        Width=package.width.IN,
        Length=package.length.IN,
        Height=package.height.IN,
        Machinable=('usps_machinable' in payload.options),
        ProcessingCategory=None,
        PriceOptions=None,
        InsuredAmount=None,
        AddressServiceRequested=None,
        ExpressMailOptions=None,
        ShipDate=None,
        CustomerRefNo=None,
        ExtraServices=None,
        HoldForPickup=None,
        OpenDistribute=None,
        PermitNumber=None,
        PermitZIPCode=None,
        PermitHolderName=None,
        CRID=None,
        MID=None,
        LogisticsManagerMID=None,
        VendorCode=None,
        VendorProductVersionNumber=None,
        SenderName=None,
        SenderEMail=None,
        RecipientName=None,
        RecipientEMail=None,
        ReceiptOption=None,
        ImageType=None,
        HoldForManifest=None,
        NineDigitRoutingZip=None,
        ShipInfo=None,
        CarrierRelease=None,
        DropOffTime=None,
        ReturnCommitments=None,
        PrintCustomerRefNo=None,
        Content=None,
        ShippingContents=None,
        CustomsContentType=None,
        ContentComments=None,
        RestrictionType=None,
        RestrictionComments=None,
        AESITN=None,
        ImportersReference=None,
        ImportersContact=None,
        ExportersReference=None,
        ExportersContact=None,
        InvoiceNumber=payload.customs.invoice,
        LicenseNumber=payload.customs.eel_pfc,
        CertificateNumber=payload.customs.certificate_number,
        NonDeliveryOption=None,
        AltReturnAddress1=None,
        AltReturnAddress2=None,
        AltReturnAddress3=None,
        AltReturnAddress4=None,
        AltReturnAddress5=None,
        AltReturnAddress6=None,
        AltReturnCountry=None,
        LabelImportType=None,
        ePostageMailerReporting=None,
        SenderFirstName=None,
        SenderLastName=None,
        SenderBusinessName=None,
        SenderAddress1=None,
        SenderCity=None,
        SenderState=None,
        SenderZip5=None,
        SenderPhone=None,
        ChargebackCode=None,
        TrackingRetentionPeriod=None,
    )

    return Serializable(request)
