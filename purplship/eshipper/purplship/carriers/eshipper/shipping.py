from typing import List, Tuple
from pyeshipper.shipping_request import (
    EShipper, ShippingRequestType, FromType, ToType, PackagesType, PackageType,
    PaymentType as RequestPaymentType, CODType, CODReturnAddressType, ContactType,
    ReferenceType, CustomsInvoiceType, ItemType, BillToType,
)
from pyeshipper.shipping_reply import ShippingReplyType, QuoteType, PackageType as ReplyPackageType
from purplship.core.errors import FieldError, FieldErrorCode
from purplship.core.utils import Element, Serializable, concat_str, decimal
from purplship.core.models import ShipmentRequest, ShipmentDetails, RateDetails, Message, ChargeDetails, Address
from purplship.core.units import Package, Options
from purplship.carriers.eshipper.utils import Settings, standard_request_serializer
from purplship.carriers.eshipper.units import Service, PackagingType, FreightClass, Option, PaymentType
from purplship.carriers.eshipper.error import parse_error_response


def parse_shipping_reply(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    shipping_node = next(iter(response.xpath(".//*[local-name() = $name]", name="ShippingReply")), None)
    return (
        _extract_shipment(shipping_node, settings) if shipping_node is not None else None,
        parse_error_response(response, settings)
    )


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipping = ShippingReplyType()
    shipping.build(node)
    quote: QuoteType = shipping.Quote
    package: ReplyPackageType = next(iter(shipping.Package), None)
    tracking_number = package.trackingNumber if package is not None else None

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        label=shipping.Labels,
        selected_rate=RateDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            service=Service(str(quote.serviceId)).name,
            currency=quote.currency,
            base_charge=decimal(quote.baseCharge),
            total_charge=decimal(quote.totalCharge),
            estimated_delivery=quote.transitDays,
            extra_charges=[
                ChargeDetails(
                    name="Fuel Surcharge",
                    amount=decimal(quote.fuelSurcharge),
                    currency=quote.currency
                )
            ] if quote.fuelSurcharge is not None else []
        ) if quote is not None else None
    )


def shipping_request(payload: ShipmentRequest, settings: Settings) -> Serializable[EShipper]:
    package = Package(payload.parcel)

    dimensions = [
        ("parcel.weight", package.weight.value), ("parcel.height", package.height.value),
        ("parcel.width", package.width.value), ("parcel.length", package.length.value)
    ]
    field_errors = {key: FieldErrorCode.required for key, dim in dimensions if dim is None}
    if any(field_errors.items()):
        raise FieldError(field_errors)

    packaging_type = PackagingType[package.packaging_type or "small_box"].value
    options = Options(payload.options)
    service = Service[payload.service].value
    freight_class = (
        FreightClass[payload.options["freight_class"]].value
        if payload.options.get("freight_class") in FreightClass.__members__
        else None
    )
    special_services = {
        Option[s]: "true" for s in payload.options.keys() if s in Option.__members__
    }
    payment_type = (
        PaymentType[payload.payment.paid_by] if payload.payment else None
    )
    item = next(
        iter(payload.customs.commodities if payload.customs is not None else []),
        None
    )
    payer: Address = {
        PaymentType.sender: payload.shipper,
        PaymentType.recipient: payload.recipient,
        PaymentType.third_party: payload.payment.contact if payload.payment is not None else None
    }.get(PaymentType[payload.payment.paid_by]) if payload.payment else None

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.0.0",
        ShippingRequest=ShippingRequestType(
            saturdayPickupRequired=special_services.get(Option.eshipper_saturday_pickup_required),
            homelandSecurity=special_services.get(Option.eshipper_homeland_security),
            pierCharge=None,
            exhibitionConventionSite=special_services.get(Option.eshipper_exhibition_convention_site),
            militaryBaseDelivery=special_services.get(Option.eshipper_military_base_delivery),
            customsIn_bondFreight=special_services.get(Option.eshipper_customs_in_bond_freight),
            limitedAccess=special_services.get(Option.eshipper_limited_access),
            excessLength=special_services.get(Option.eshipper_excess_length),
            tailgatePickup=special_services.get(Option.eshipper_tailgate_pickup),
            residentialPickup=special_services.get(Option.eshipper_residential_pickup),
            crossBorderFee=None,
            notifyRecipient=special_services.get(Option.eshipper_notify_recipient),
            singleShipment=special_services.get(Option.eshipper_single_shipment),
            tailgateDelivery=special_services.get(Option.eshipper_tailgate_delivery),
            residentialDelivery=special_services.get(Option.eshipper_residential_delivery),
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=special_services.get(Option.eshipper_inside_delivery),
            isSaturdayService=special_services.get(Option.eshipper_is_saturday_service),
            dangerousGoodsType=special_services.get(Option.eshipper_dangerous_goods_type),
            serviceId=service,
            stackable=special_services.get(Option.eshipper_stackable),
            From=FromType(
                id=payload.shipper.id,
                company=payload.shipper.company_name,
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=concat_str(payload.shipper.address_line1, join=True),
                address2=concat_str(payload.shipper.address_line2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code
            ),
            To=ToType(
                id=payload.recipient.id,
                company=payload.recipient.company_name,
                notifyRecipient=None,
                instructions=None,
                email=payload.recipient.email,
                attention=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                tailgateRequired=None,
                residential=payload.recipient.residential,
                address1=concat_str(payload.recipient.address_line1, join=True),
                address2=concat_str(payload.recipient.address_line2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code
            ),
            COD=CODType(
                paymentType=PaymentType.recipient.value,
                CODReturnAddress=CODReturnAddressType(
                    codCompany=payload.recipient.company_name,
                    codName=payload.recipient.person_name,
                    codAddress1=concat_str(payload.recipient.address_line1, join=True),
                    codCity=payload.recipient.city,
                    codStateCode=payload.recipient.state_code,
                    codZip=payload.recipient.postal_code,
                    codCountry=payload.recipient.country_code
                )
            ) if options.cash_on_delivery is not None else None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=package.length.value,
                        width=package.width.value,
                        height=package.height.value,
                        weight=package.weight.value,
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=payload.parcel.description,
                    )
                ]
            ),
            Payment=RequestPaymentType(
                type_=payment_type
            ) if payload.payment is not None else None,
            Reference=[
                ReferenceType(
                    name="",
                    code=payload.reference
                )
            ] if payload.reference != "" else None,
            CustomsInvoice=CustomsInvoiceType(
                BillTo=BillToType(
                    company=payer.company_name,
                    name=payer.person_name,
                    address1=concat_str(payer.address_line1, join=True),
                    city=payer.city,
                    state=payer.state_code,
                    zip=payer.postal_code,
                    country=payer.country_code,
                ),
                Contact=ContactType(
                    name=payer.person_name,
                    phone=payer.phone_number
                ),
                Item=ItemType(
                    code=item.sku,
                    description=item.description,
                    originCountry=item.origin_country,
                    quantity=item.quantity,
                    unitPrice=item.value_amount
                )
            ) if payload.customs is not None and payer is not None else None
        )
    )

    return Serializable(request, standard_request_serializer)
