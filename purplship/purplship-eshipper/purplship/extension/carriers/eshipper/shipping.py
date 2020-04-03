from typing import List, Tuple
from pyeshipper.shipping_request import (
    EShipper, ShippingRequestType, FromType, ToType, PackagesType, PackageType,
    PaymentType as RequestPaymentType, CODType, CODReturnAddressType, ContactType,
    ReferenceType, CustomsInvoiceType, ItemType, BillToType,
)
from pyeshipper.shipping_reply import ShippingReplyType, QuoteType, PackageType as ReplyPackageType
from purplship.core.errors import RequiredFieldError
from purplship.core.utils import Element, Serializable, concat_str
from purplship.core.models import ShipmentRequest, ShipmentDetails, RateDetails, Error, ChargeDetails, Address
from purplship.core.units import Package, Options
from purplship.extension.carriers.eshipper.utils import Settings, standard_request_serializer
from purplship.extension.carriers.eshipper.units import Service, PackagingType, FreightClass, Option, PaymentType
from purplship.extension.carriers.eshipper.error import parse_error_response


def parse_shipping_reply(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
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
        carrier=settings.carrier_name,
        tracking_number=tracking_number,
        label=shipping.Labels,
        selected_rate=RateDetails(
            carrier=settings.carrier_name,
            service=Service(str(quote.serviceId)).name,
            currency=quote.currency,
            base_charge=float(quote.baseCharge),
            total_charge=float(quote.totalCharge),
            estimated_delivery=quote.transitDays,
            extra_charges=[
                ChargeDetails(
                    name="Fuel Surcharge",
                    amount=float(quote.fuelSurcharge),
                    currency=quote.currency
                )
            ] if quote.fuelSurcharge is not None else []
        ) if quote is not None else None
    )


def shipping_request(payload: ShipmentRequest, settings: Settings) -> Serializable[EShipper]:
    package = Package(payload.parcel)
    dimensions = [("weight", package.weight.value), ("height", package.height.value), ("width", package.width.value), ("length", package.length.value)]

    for key, dim in dimensions:
        if dim is None:
            raise RequiredFieldError(key)

    packaging_type = PackagingType[package.packaging_type or "small_box"].value
    options = Options(payload.parcel.options)
    service = next(
        (Service[s].value for s in payload.parcel.services if s in Service.__members__),
        Service.eshipper_canada_post_regular.value
    )
    freight_class = next(
        (FreightClass[c].value for c in payload.parcel.options.keys() if c in FreightClass.__members__),
        None
    )
    special_services = {
        Option[s]: True for s in payload.parcel.options.keys() if s in Option.__members__
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
        PaymentType.third_party: payload.customs.duty.contact if payload.customs is not None else None
    }.get(PaymentType[payload.payment.paid_by]) if payload.payment else None

    request = EShipper(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
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
                id=payload.shipper.type,
                company=payload.shipper.company_name,
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=concat_str(payload.shipper.address_line_1, join=True),
                address2=concat_str(payload.shipper.address_line_2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code
            ),
            To=ToType(
                id=payload.recipient.type,
                company=payload.recipient.company_name,
                notifyRecipient=None,
                instructions=None,
                email=payload.recipient.email,
                attention=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                tailgateRequired=None,
                residential=payload.recipient.residential,
                address1=concat_str(payload.recipient.address_line_1, join=True),
                address2=concat_str(payload.recipient.address_line_2, join=True),
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
                    codAddress1=payload.recipient.address_line_1,
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
                    name=payload.parcel.reference,
                    code="parcelRef"
                )
            ] if payload.parcel.reference != "" else None,
            CustomsInvoice=CustomsInvoiceType(
                BillTo=BillToType(
                    company=payer.company_name,
                    name=payer.person_name,
                    address1=payer.address_line_1,
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
                    unitPrice=item.value_amount
                )
            ) if payload.customs is not None and payer is not None else None
        )
    )

    return Serializable(request, standard_request_serializer)
