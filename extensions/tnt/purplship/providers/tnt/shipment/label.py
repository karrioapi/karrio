from typing import cast
from tnt_lib.shipment_response import document, CREATE, PRICE
from tnt_lib.label_request import (
    labelRequest,
    labelConsignmentsType,
    consignmentIdentityType,
    nameAndAddressRequestType,
    contactType,
    productType,
    accountType,
    pieceLineType,
    pieceType,
    measurementsType,
)
from purplship.core.utils import Serializable
from purplship.core.units import Packages
from purplship.core.models import ShipmentRequest, Payment
from purplship.providers.tnt.units import PaymentType, ShipmentOption, ShipmentService
from purplship.providers.tnt.utils import Settings


def create_label_request(activity: document, payload: ShipmentRequest, settings: Settings) -> Serializable[labelRequest]:
    package = Packages(payload.parcels).single
    payment = payload.payment or Payment(paid_by='sender')
    price: PRICE = next(activity.RATE.PRICE, PRICE())

    request = labelRequest(
        consignment=[
            labelConsignmentsType(
                key="1",
                consignmentIdentity=consignmentIdentityType(
                    consignmentNumber=cast(CREATE, activity.CREATE).CONNUMBER,
                    customerReference=payload.reference
                ),
                collectionDateTime=None,
                sender=nameAndAddressRequestType(
                    name=payload.shipper.company_name or payload.shipper.person_name,
                    addressLine1=payload.shipper.address_line1,
                    addressLine2=payload.shipper.address_line2,
                    addressLine3=None,
                    town=payload.shipper.city,
                    exactMatch=None,
                    province=payload.shipper.state_code,
                    postcode=payload.shipper.postal_code,
                    country=payload.shipper.country_code
                ),
                delivery=nameAndAddressRequestType(
                    name=payload.recipient.company_name or payload.recipient.person_name,
                    addressLine1=payload.recipient.address_line1,
                    addressLine2=payload.recipient.address_line2,
                    addressLine3=None,
                    town=payload.recipient.city,
                    exactMatch=None,
                    province=payload.recipient.state_code,
                    postcode=payload.recipient.postal_code,
                    country=payload.recipient.country_code
                ),
                contact=contactType(
                    name=payload.shipper.person_name,
                    telephoneNumber=payload.shipper.phone_number,
                    emailAddress=payload.shipper.email
                ),
                product=productType(
                    lineOfBusiness=None,
                    groupId=activity.GROUPCODE,
                    subGroupId=None,
                    id=price.SERVICE,
                    type_=price.SERVICEDESC,
                    option=price.OPTION,
                ),
                account=accountType(
                    accountNumber=settings.account_number,
                    accountCountry=settings.account_country_code
                ),
                cashAmount=price.RATE,
                cashCurrency=price.CURRENCY,
                cashType=None,
                ncolNumber=None,
                specialInstructions=None,
                bulkShipment='N',
                customControlled=('N' if payload.customs is None else 'Y'),
                termsOfPayment=PaymentType[payment.paid_by or 'sender'].value,
                totalNumberOfPieces=1,
                pieceLine=[
                    pieceLineType(
                        identifier=1,
                        goodsDescription=package.parcel.description,
                        barcodeForCustomer='Y',
                        pieceMeasurements=measurementsType(
                            length=package.length.M,
                            width=package.width.M,
                            height=package.height.M,
                            weight=package.weight.M
                        ),
                        pieces=(
                            [
                                pieceType(
                                    sequenceNumbers=(index + 1),
                                    pieceReference=piece.sku
                                )
                                for index, piece in enumerate(payload.customs.commodities)
                            ]
                            if payload.customs is not None and any(payload.customs.commodities)
                            else None
                        )
                    )
                ]
            )
        ]
    )

    return Serializable(request)
