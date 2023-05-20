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
import karrio.lib as lib
from karrio.core.utils import Serializable
from karrio.core.units import Packages
from karrio.core.models import ShipmentRequest, Payment
from karrio.providers.tnt.units import PaymentType
from karrio.providers.tnt.utils import Settings


def create_label_request(
    activity: document, payload: ShipmentRequest, settings: Settings
) -> Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = Packages(payload.parcels).single
    payment = payload.payment or Payment(paid_by="sender")
    price: PRICE = next(activity.RATE.PRICE, PRICE())

    request = labelRequest(
        consignment=[
            labelConsignmentsType(
                key="1",
                consignmentIdentity=consignmentIdentityType(
                    consignmentNumber=cast(CREATE, activity.CREATE).CONNUMBER,
                    customerReference=payload.reference,
                ),
                collectionDateTime=None,
                sender=nameAndAddressRequestType(
                    name=recipient.contact,
                    addressLine1=shipper.street,
                    addressLine2=shipper.address_line2,
                    addressLine3=None,
                    town=shipper.city,
                    exactMatch=None,
                    province=shipper.state_code,
                    postcode=shipper.postal_code,
                    country=shipper.country_code,
                ),
                delivery=nameAndAddressRequestType(
                    name=recipient.contact,
                    addressLine1=recipient.street,
                    addressLine2=recipient.address_line2,
                    addressLine3=None,
                    town=recipient.city,
                    exactMatch=None,
                    province=recipient.state_code,
                    postcode=recipient.postal_code,
                    country=recipient.country_code,
                ),
                contact=contactType(
                    name=shipper.person_name,
                    telephoneNumber=shipper.phone_number,
                    emailAddress=shipper.email,
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
                    accountCountry=settings.account_country_code,
                ),
                cashAmount=price.RATE,
                cashCurrency=price.CURRENCY,
                cashType=None,
                ncolNumber=None,
                specialInstructions=None,
                bulkShipment="N",
                customControlled=("N" if payload.customs is None else "Y"),
                termsOfPayment=PaymentType[payment.paid_by or "sender"].value,
                totalNumberOfPieces=1,
                pieceLine=[
                    pieceLineType(
                        identifier=1,
                        goodsDescription=package.parcel.description,
                        barcodeForCustomer="Y",
                        pieceMeasurements=measurementsType(
                            length=package.length.M,
                            width=package.width.M,
                            height=package.height.M,
                            weight=package.weight.M,
                        ),
                        pieces=(
                            [
                                pieceType(
                                    sequenceNumbers=(index + 1),
                                    pieceReference=piece.sku or piece.hs_code,
                                )
                                for index, piece in enumerate(
                                    payload.customs.commodities
                                )
                            ]
                            if payload.customs is not None
                            and any(payload.customs.commodities)
                            else None
                        ),
                    )
                ],
            )
        ]
    )

    return Serializable(request)
