from typing import Tuple, List
from karrio.schemas.dicom.shipments import (
    ShipmentRequest as DicomShipmentRequest,
    Address as DicomAddress,
    Parcel,
    Surcharge,
    Contact,
    InternationalDetails,
    Product,
    Broker,
    ShipmentResponse,
)
import karrio.lib as lib
from karrio.core.units import Packages
from karrio.core.utils import Serializable, DP
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    Message,
    Address,
    Payment,
)

from karrio.providers.dicom.units import (
    UnitOfMeasurement,
    ParcelType,
    Service,
    ShippingOption,
    PaymentType,
    Purpose,
)
from karrio.providers.dicom.error import parse_error_response
from karrio.providers.dicom.utils import Settings


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ShipmentDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    details = (
        _extract_details(response, settings)
        if all(key in response for key in ["label", "shipment"])
        else None
    )

    return details, errors


def _extract_details(response: dict, settings: Settings) -> ShipmentDetails:
    label: str = response["label"]
    shipment = DP.to_object(ShipmentResponse, response["shipment"])

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.ID,
        docs=Documents(label=label),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    packages = Packages(payload.parcels)
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    is_international = shipper.country_code != recipient.country_code
    broker_info = payload.options.get("dicom_broker_info", {})
    importer_info = (
        Address(**payload.options.get("importer_info"))
        if "importer_info" in payload.options
        else None
    )
    payment = payload.payment or Payment("prepaid")
    delivery_type = Service[payload.service].value
    options = {
        key: (value if ShippingOption[key].value in ["DCV", "COD"] else None)
        for key, value in payload.options
        if key in ShippingOption.__members__
    }

    request = DicomShipmentRequest(
        paymentType=PaymentType[payment.paid_by or "prepaid"].value,
        billingAccount=settings.billing_account,
        sender=DicomAddress(
            city=shipper.city,
            provinceCode=shipper.state_code,
            postalCode=shipper.postal_code,
            countryCode=shipper.country_code,
            customerName=shipper.company_name,
            addressLine1=shipper.street,
            addressLine2=shipper.address_line2,
            contact=Contact(
                fullName=shipper.person_name,
                email=shipper.email,
                telephone=shipper.phone_number,
            ),
        ),
        consignee=DicomAddress(
            city=recipient.city,
            provinceCode=recipient.state_code,
            postalCode=recipient.postal_code,
            countryCode=recipient.country_code,
            customerName=recipient.company_name,
            addressLine1=recipient.street,
            addressLine2=recipient.address_line2,
            contact=Contact(
                fullName=recipient.person_name,
                email=recipient.email,
                telephone=recipient.phone_number,
            ),
        ),
        parcels=[
            Parcel(
                quantity=1,
                parcelType=ParcelType[package.packaging_type or "dicom_box"].value,
                weight=package.weight.KG,
                length=package.height.CM,
                depth=package.length.CM,
                width=package.width.CM,
                note=None,
                status=None,
                FCAClass=None,
                hazmat=None,
                requestReturnLabel=None,
                returnWaybill=None,
            )
            for package in packages
        ],
        note=None,
        category="Parcel",
        pickupDate=None,
        deliveryType=delivery_type,
        trackingNumber=None,
        unitOfMeasurement=UnitOfMeasurement.KC.value,
        surcharges=[Surcharge(type=key, value=value) for key, value in options.items()],
        promoCodes=None,
        references=None,
        returnAddress=None,
        appointment=None,
        internationalDetails=(
            InternationalDetails(
                isDicomBroker=(broker_info is not None),
                descriptionOfGoods=payload.customs.content_description,
                dutyBilling=payload.customs.duty.paid_by,
                importerOfRecord=(
                    DicomAddress(
                        city=importer_info.city,
                        provinceCode=importer_info.state_code,
                        postalCode=importer_info.postal_code,
                        countryCode=importer_info.country_code,
                        customerName=importer_info.company_name,
                        addressLine1=lib.text(
                            importer_info.street_number, importer_info.address_line1
                        ),
                        addressLine2=importer_info.address_line2,
                        contact=Contact(
                            fullName=importer_info.person_name,
                            email=importer_info.email,
                            telephone=importer_info.phone_number,
                        ),
                    )
                    if importer_info is not None
                    else None
                ),
                broker=(
                    Broker(
                        id=broker_info.get("id"),
                        CSA_BusinessNumber=broker_info.get("CSA_BusinessNumber"),
                        otherBroker=broker_info.get("otherBroker"),
                    )
                    if broker_info is not None
                    else None
                ),
                purpose=(
                    Purpose[payload.customs.content_type].value
                    if payload.customs.content_type is not None
                    else None
                ),
                products=[
                    Product(id=index, Quantity=product.quantity)
                    for index, product in enumerate(payload.customs.commodities, 1)
                ],
            )
            if is_international and payload.customs is not None
            else None
        ),
    )

    return Serializable(request)
