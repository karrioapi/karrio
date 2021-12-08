from uuid import uuid4
from typing import Tuple, List
from asendia_us_lib.shipping_request import ShippingRequest, Item
from asendia_us_lib.shipping_response import PackageLabel
from purplship.core.units import CustomsInfo, Packages, Options, Weight
from purplship.core.utils import Serializable, DP
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message,
    Customs,
)

from purplship.providers.asendia_us.units import (
    Service,
    Option,
    LabelType,
    ProcessingLocation,
)
from purplship.providers.asendia_us.error import parse_error_response
from purplship.providers.asendia_us.utils import Settings


def parse_shipment_response(
    responses: Tuple[str, dict], settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    _, response = responses
    errors = parse_error_response(response, settings)
    details = (
        _extract_details(responses, settings)
        if response.get("packageLabel") is not None
        else None
    )

    return details, errors


def _extract_details(response: Tuple[str, dict], settings: Settings) -> ShipmentDetails:
    label, details = response
    shipment = DP.to_object(PackageLabel, details)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        label=label,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.packageId,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ShippingRequest]:
    package = Packages(payload.parcels).single
    options = Options(payload.options, Option)
    product_code = Service.map(payload.service).value_or_key
    unique_id = getattr(payload, "id", uuid4().hex)
    customs = CustomsInfo(payload.customs or Customs(commodities=[]))

    request = ShippingRequest(
        accountNumber=settings.account_number,
        subAccountNumber=options.asendia_sub_account_number,
        processingLocation=ProcessingLocation.map(
            options.asendia_processing_location or "SFO"
        ).name,
        includeRate=True,
        labelType=LabelType.map(payload.label_type or "PDF").name_or_key,
        orderNumber=unique_id,
        dispatchNumber=unique_id,
        packageID=unique_id,
        recipientTaxID=payload.recipient.state_tax_id,
        returnFirstName=payload.shipper.person_name,
        returnLastName=payload.shipper.person_name,
        returnCompanyName=payload.shipper.company_name,
        returnAddressLine1=payload.shipper.address_line1,
        returnAddressLine2=payload.shipper.address_line2,
        returnAddressLine3=None,
        returnProvince=payload.shipper.state_code,
        returnPostalCode=payload.shipper.postal_code,
        returnCountryCode=payload.shipper.country_code,
        returnPhone=payload.shipper.phone_number,
        returnEmail=payload.shipper.email,
        recipientFirstName=payload.recipient.person_name,
        recipientLastName=payload.recipient.person_name,
        recipientBusinessName=payload.recipient.company_name,
        recipientAddressLine1=payload.recipient.address_line1,
        recipientAddressLine2=payload.recipient.address_line2,
        recipientAddressLine3=None,
        recipientCity=payload.recipient.city,
        recipientProvince=payload.recipient.state_code,
        recipientPostalCode=payload.recipient.postal_code,
        recipientPhone=payload.recipient.phone_number,
        recipientEmail=payload.recipient.email,
        totalPackageWeight=package.weight.value,
        weightUnit=package.weight_unit.value.lower(),
        dimLength=package.length.value,
        dimWidth=package.width.value,
        dimHeight=package.height.value,
        dimUnit=package.dimension_unit.value,
        totalPackageValue=options.declared_value,
        currencyType=options.currency,
        productCode=product_code,
        customerReferenceNumber1=payload.reference,
        customerReferenceNumber2=None,
        customerReferenceNumber3=None,
        contentType=("D" if package.parcel.is_document else "M"),
        packageContentDescription=package.parcel.description,
        vatNumber=None,
        sellerName=payload.shipper.person_name,
        sellerAddressLine1=payload.shipper.address_line1,
        sellerAddressLine2=payload.shipper.address_line2,
        sellerAddressLine3=None,
        sellerProvince=payload.shipper.state_code,
        sellerPostalCode=payload.shipper.postal_code,
        sellerPhone=payload.shipper.phone_number,
        sellerEmail=payload.shipper.email,
        items=[
            Item(
                sku=item.sku,
                itemDescription=item.description,
                unitPrice=item.value_amount,
                quantity=item.quantity,
                unitWeight=Weight(item.weight, package.weight_unit).value,
                countryOfOrigin=item.origin_country,
                htsNumber=None,
            )
            for item in customs.commodities
        ],
    )

    return Serializable(request)
