from typing import Tuple, List, Union, Type
import pyusps.evs_express_mail_intl_request as evs_express
import pyusps.evs_priority_mail_intl_request as evs_priority
import pyusps.evs_first_class_mail_intl_request as evs_first_class
from purplship.core.utils import Serializable, export
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.utils import Settings

eVSREquest = Type[Union[
    evs_express.eVSExpressMailIntlRequest,
    evs_priority.eVSPriorityMailIntlRequest,
    evs_first_class.eVSFirstClassMailIntlRequest,
]]


def parse_shipment_response(response: dict, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[eVSREquest]:
    service = None

    data = dict(
    # data = evs_express.eVSExpressMailIntlRequest(
    # data = evs_priority.eVSPriorityMailIntlRequest(
    # data = evs_first_class.eVSFirstClassMailIntlRequest(
        USERID=settings.username,
        Option=None,
        Revision=None,
        ImageParameters=None,
        FromFirstName=None,
        FromMiddleInitial=None,
        FromLastName=None,
        FromFirm=None,
        FromAddress1=None,
        FromAddress2=None,
        FromUrbanization=None,
        FromCity=None,
        FromState=None,
        FromZip5=None,
        FromZip4=None,
        FromPhone=None,
        FromCustomsReference=None,
        ToName=None,
        ToFirstName=None,
        ToLastName=None,
        ToFirm=None,
        ToAddress1=None,
        ToAddress2=None,
        ToAddress3=None,
        ToCity=None,
        ToProvince=None,
        ToCountry=None,
        ToPostalCode=None,
        ToPOBoxFlag=None,
        ToPhone=None,
        ToFax=None,
        ToEmail=None,
        FirstClassMailType=None,
        ImportersReferenceNumber=None,
        NonDeliveryOption=None,
        RedirectName=None,
        RedirectEmail=None,
        RedirectSMS=None,
        RedirectAddress=None,
        RedirectCity=None,
        RedirectState=None,
        RedirectZipCode=None,
        RedirectZip4=None,
        Container=None,
        ShippingContents=None,
        Insured=None,
        InsuredNumber=None,
        InsuredAmount=None,
        Postage=None,
        GrossPounds=None,
        GrossOunces=None,
        ContentType=None,
        ContentTypeOther=None,
        Agreement=None,
        Comments=None,
        LicenseNumber=None,
        CertificateNumber=None,
        InvoiceNumber=None,
        ImageType=None,
        ImageLayout=None,
        CustomerRefNo=None,
        CustomerRefNo2=None,
        POZipCode=None,
        LabelDate=None,
        EMCAAccount=None,
        HoldForManifest=None,
        EELPFC=None,
        PriceOptions=None,
        Length=None,
        Width=None,
        Height=None,
        Girth=None,
        ExtraServices=None,
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
        Machinable=None,
        DestinationRateIndicator=None,
        MID=None,
        LogisticsManagerMID=None,
        CRID=None,
        VendorCode=None,
        VendorProductVersionNumber=None,
        ePostageMailerReporting=None,
        SenderFirstName=None,
        SenderLastName=None,
        SenderBusinessName=None,
        SenderAddress1=None,
        SenderCity=None,
        SenderState=None,
        SenderZip5=None,
        SenderPhone=None,
        SenderEmail=None,
        RemainingBarcodes=None,
        ChargebackCode=None,
    )

    if 'first_class' in service:
        request = evs_first_class.eVSFirstClassMailIntlRequest(**data)
    elif 'express' in service:
        request = evs_express.eVSExpressMailIntlRequest(**data)
    else:
        request = evs_priority.eVSPriorityMailIntlRequest(**data)

    return Serializable(request, export)
