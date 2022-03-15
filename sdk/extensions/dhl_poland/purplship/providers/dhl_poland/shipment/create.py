import time
from functools import partial
from typing import List, Tuple, Optional
from dhl_poland_lib.services import (
    Address,
    Addressat,
    ArrayOfCustomsitemdata,
    ArrayOfPackage,
    ArrayOfService,
    Billing,
    CreateShipmentRequest,
    CustomsAgreementData,
    CustomsData,
    CustomsItemData,
    Package,
    PreavisoContact,
    ReceiverAddress,
    ReceiverAddressat,
    Ship,
    ShipmentInfo,
    ShipmentTime,
    createShipment,
    Service as DhlService,
    CreateShipmentResponse,
)
from karrio.core.models import (
    Documents,
    Message,
    Payment,
    ShipmentRequest,
    ShipmentDetails,
)
from karrio.core.utils import (
    Serializable,
    Element,
    create_envelope,
    XP,
    DF,
)
from karrio.core.units import (
    CompleteAddress,
    CustomsInfo,
    Packages,
    Options,
    Weight,
    WeightUnit,
)
from karrio.providers.dhl_poland.error import parse_error_response
from karrio.providers.dhl_poland.utils import Settings
from karrio.providers.dhl_poland.units import (
    PackagingType,
    Option,
    Service,
    LabelType,
    PaymentType,
    CustomsContentType,
)


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if XP.find("createShipmentResult", response, first=True) is not None
        else None
    )

    return shipment, errors


def _extract_details(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.find(
        "createShipmentResult", response, CreateShipmentResponse, first=True
    )

    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.shipmentNotificationNumber,
        shipment_identifier=shipment.shipmentTrackingNumber,
        docs=Documents(
            label=shipment.label.labelContent,
            invoice=shipment.label.fvProformaContent,
        ),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[str]:
    packages = Packages(payload.parcels, required=["weight"])
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)
    options = Options(payload.options, Option)
    customs = CustomsInfo(payload.customs)

    is_international = shipper.country_code != recipient.country_code
    service_type = Service.map(payload.service).value_or_key or (
        Service.dhl_poland_polska.value
        if is_international
        else Service.dhl_poland_09.value
    )
    label_type = LabelType.map(payload.label_type or "PDF").value
    payment = payload.payment or Payment()
    quantity = len(customs.commodities or []) if customs.is_defined else 1

    request = create_envelope(
        body_content=createShipment(
            authData=settings.auth_data,
            shipment=CreateShipmentRequest(
                shipmentInfo=ShipmentInfo(
                    wayBill=None,
                    dropOffType="REGULAR_PICKUP",
                    serviceType=service_type,
                    billing=Billing(
                        shippingPaymentType=PaymentType[payment.paid_by].value,
                        billingAccountNumber=(
                            payment.account_number or settings.account_number
                        ),
                        paymentType="BANK_TRANSFER",
                        costsCenter=None,
                    ),
                    specialServices=(
                        ArrayOfService(
                            item=[
                                DhlService(
                                    serviceType=getattr(option, "key", option),
                                    serviceValue=getattr(option, "value", None),
                                    textInstruction=None,
                                    collectOnDeliveryForm=None,
                                )
                                for _, option in options
                            ]
                        )
                        if any(options)
                        else None
                    ),
                    shipmentTime=(
                        ShipmentTime(
                            shipmentDate=(
                                options.shipment_date or time.strftime("%Y-%m-%d")
                            ),
                            shipmentStartHour="10:00",
                            shipmentEndHour="10:00",
                        )
                    ),
                    labelType=label_type,
                ),
                content=payload.parcels[0].content or "N/A",
                comment=None,
                reference=payload.reference,
                ship=Ship(
                    shipper=Addressat(
                        preaviso=(
                            PreavisoContact(
                                personName=shipper.person_name,
                                phoneNumber=shipper.phone_number,
                                emailAddress=shipper.email,
                            )
                            if any(
                                [
                                    shipper.person_name,
                                    shipper.phone_number,
                                    shipper.email,
                                ]
                            )
                            else None
                        ),
                        contact=(
                            PreavisoContact(
                                personName=shipper.person_name,
                                phoneNumber=shipper.phone_number,
                                emailAddress=shipper.email,
                            )
                            if any(
                                [
                                    shipper.person_name,
                                    shipper.phone_number,
                                    shipper.email,
                                ]
                            )
                            else None
                        ),
                        address=Address(
                            name=(shipper.company_name or shipper.person_name),
                            postalCode=(shipper.postal_code or "").replace("-", ""),
                            city=shipper.city,
                            street=shipper.address_line,
                            houseNumber=(shipper.street_number or "N/A"),
                            apartmentNumber=shipper.suite,
                        ),
                    ),
                    receiver=ReceiverAddressat(
                        preaviso=(
                            PreavisoContact(
                                personName=recipient.person_name,
                                phoneNumber=recipient.phone_number,
                                emailAddress=recipient.email,
                            )
                            if any(
                                [
                                    recipient.person_name,
                                    recipient.phone_number,
                                    recipient.email,
                                ]
                            )
                            else None
                        ),
                        contact=(
                            PreavisoContact(
                                personName=recipient.person_name,
                                phoneNumber=recipient.phone_number,
                                emailAddress=recipient.email,
                            )
                            if any(
                                [
                                    recipient.person_name,
                                    recipient.phone_number,
                                    recipient.email,
                                ]
                            )
                            else None
                        ),
                        address=ReceiverAddress(
                            country=recipient.country_code,
                            isPackstation=None,
                            isPostfiliale=None,
                            postnummer=None,
                            addressType=("C" if recipient.residential else "B"),
                            name=(recipient.company_name or recipient.person_name),
                            postalCode=(recipient.postal_code or "").replace("-", ""),
                            city=recipient.city,
                            street=recipient.address_line,
                            houseNumber=(shipper.street_number or "N/A"),
                            apartmentNumber=shipper.suite,
                        ),
                    ),
                    neighbour=None,
                ),
                pieceList=ArrayOfPackage(
                    item=[
                        Package(
                            type_=PackagingType[
                                package.packaging_type or "your_packaging"
                            ].value,
                            euroReturn=None,
                            weight=package.weight.KG,
                            width=package.width.CM,
                            height=package.height.CM,
                            length=package.length.CM,
                            quantity=quantity,
                            nonStandard=None,
                            blpPieceId=None,
                        )
                        for package in packages
                    ]
                ),
                customs=(
                    CustomsData(
                        customsType="S",
                        firstName=getattr(
                            getattr(customs.duty, "bil_to", shipper.company_name),
                            "company_name",
                            "N/A",
                        ),
                        secondaryName=getattr(
                            getattr(customs.duty, "bil_to", shipper.person_name),
                            "person_name",
                            "N/A",
                        ),
                        costsOfShipment=getattr(
                            customs.duty or options, "declared_value", None
                        ),
                        currency=getattr(customs.duty or options, "currency", "EUR"),
                        nipNr=customs.nip_number,
                        eoriNr=customs.eori_number,
                        vatRegistrationNumber=customs.vat_registration_number,
                        categoryOfItem=CustomsContentType[
                            customs.content_type or "other"
                        ].value,
                        invoiceNr=customs.invoice,
                        invoice=None,
                        invoiceDate=customs.invoice_date,
                        countryOfOrigin=shipper.country_code,
                        additionalInfo=None,
                        grossWeight=packages.weight.KG,
                        customsItem=(
                            ArrayOfCustomsitemdata(
                                item=[
                                    CustomsItemData(
                                        nameEn=item.description or "N/A",
                                        namePl=item.description or "N/A",
                                        quantity=item.quantity,
                                        weight=Weight(
                                            item.weight,
                                            WeightUnit[item.weight_unit or "KG"],
                                        ).KG,
                                        value=item.value_amount,
                                        tariffCode=item.sku,
                                    )
                                    for item in customs.commodities
                                ]
                            )
                            if any(customs.commodities)
                            else None
                        ),
                        customAgreements=CustomsAgreementData(
                            notExceedValue=True,
                            notProhibitedGoods=True,
                            notRestrictedGoods=True,
                        ),
                    )
                    if customs.is_defined
                    else None
                ),
            ),
        )
    )

    return Serializable(
        request,
        lambda req: settings.serialize(req, "createShipment", settings.server_url),
    )
