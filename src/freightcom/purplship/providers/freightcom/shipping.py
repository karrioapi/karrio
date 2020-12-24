from typing import List, Tuple, cast
from pyfreightcom.shipping_request import (
    Freightcom,
    ShippingRequestType,
    FromType,
    ToType,
    PackagesType,
    PackageType,
    PaymentType as RequestPaymentType,
    CODType,
    CODReturnAddressType,
    ContactType,
    ReferenceType,
    CustomsInvoiceType,
    ItemType,
    BillToType,
)
from pyfreightcom.shipping_reply import (
    ShippingReplyType,
    QuoteType,
    PackageType as ReplyPackageType,
    SurchargeType,
)
from purplship.core.utils import Element, Serializable, XP, SF, NF
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    RateDetails,
    Message,
    ChargeDetails,
    Address,
)
from purplship.core.units import Packages, Options
from purplship.providers.freightcom.utils import (
    Settings,
    standard_request_serializer,
    ceil,
)
from purplship.providers.freightcom.units import (
    Service,
    FreightPackagingType,
    FreightClass,
    Option,
    PaymentType,
)
from purplship.providers.freightcom.error import parse_error_response


def parse_shipping_reply(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    shipping_node = next(
        iter(response.xpath(".//*[local-name() = $name]", name="ShippingReply")), None
    )
    return (
        _extract_shipment(shipping_node, settings)
        if shipping_node is not None
        else None,
        parse_error_response(response, settings),
    )


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipping = XP.build(ShippingReplyType, node)
    quote: QuoteType = shipping.Quote
    package: ReplyPackageType = next(iter(shipping.Package), None)
    tracking_number = package.trackingNumber if package is not None else None
    service = next(
        (s.name for s in Service if str(quote.serviceId) == s.value), quote.serviceId
    )
    surcharges = [
        ChargeDetails(
            name=charge.name, amount=NF.decimal(charge.amount), currency=quote.currency
        )
        for charge in cast(List[SurchargeType], quote.Surcharge)
    ]

    fuel_surcharge = (
        ChargeDetails(
            name="Fuel surcharge",
            amount=NF.decimal(quote.fuelSurcharge),
            currency=quote.currency,
        )
        if quote.fuelSurcharge is not None
        else None
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=shipping.Order.id,
        label=shipping.Labels,
        selected_rate=RateDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            service=service,
            currency=quote.currency,
            base_charge=NF.decimal(quote.baseCharge),
            total_charge=NF.decimal(quote.totalCharge),
            transit_days=quote.transitDays,
            extra_charges=[fuel_surcharge] + surcharges,
        )
        if quote is not None
        else None,
        meta=dict(carrier_name=shipping.Carrier.carrierName.lower())
    )


def shipping_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[Freightcom]:
    packages = Packages(payload.parcels, required=["weight", "height", "width", "length"])
    packaging_type = (
        FreightPackagingType[packages[0].packaging_type or "small_box"].value
        if len(packages) == 1 else "small_box"
    )

    options = Options(payload.options)
    service = next(
        (Service[payload.service].value for s in Service if s.name == payload.service),
        payload.service,
    )
    freight_class = next(
        (
            FreightClass[c].value
            for c in payload.options.keys()
            if c in FreightClass.__members__
        ),
        None,
    )
    special_services = {
        Option[s]: True for s in payload.options.keys() if s in Option.__members__
    }
    payment_type = PaymentType[payload.payment.paid_by] if payload.payment else None
    item = next(
        iter(payload.customs.commodities if payload.customs is not None else []), None
    )
    payer: Address = {
        PaymentType.sender: payload.shipper,
        PaymentType.recipient: payload.recipient,
        PaymentType.third_party: payload.customs.duty.contact
        if payload.customs is not None
        else None,
    }.get(PaymentType[payload.payment.paid_by]) if payload.payment else None

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        ShippingRequest=ShippingRequestType(
            saturdayPickupRequired=special_services.get(
                Option.freightcom_saturday_pickup_required
            ),
            homelandSecurity=special_services.get(Option.freightcom_homeland_security),
            pierCharge=None,
            exhibitionConventionSite=special_services.get(
                Option.freightcom_exhibition_convention_site
            ),
            militaryBaseDelivery=special_services.get(
                Option.freightcom_military_base_delivery
            ),
            customsIn_bondFreight=special_services.get(
                Option.freightcom_customs_in_bond_freight
            ),
            limitedAccess=special_services.get(Option.freightcom_limited_access),
            excessLength=special_services.get(Option.freightcom_excess_length),
            tailgatePickup=special_services.get(Option.freightcom_tailgate_pickup),
            residentialPickup=special_services.get(
                Option.freightcom_residential_pickup
            ),
            crossBorderFee=None,
            notifyRecipient=special_services.get(Option.freightcom_notify_recipient),
            singleShipment=special_services.get(Option.freightcom_single_shipment),
            tailgateDelivery=special_services.get(Option.freightcom_tailgate_delivery),
            residentialDelivery=special_services.get(
                Option.freightcom_residential_delivery
            ),
            insuranceType=options.insurance is not None,
            scheduledShipDate=None,
            insideDelivery=special_services.get(Option.freightcom_inside_delivery),
            isSaturdayService=special_services.get(
                Option.freightcom_is_saturday_service
            ),
            dangerousGoodsType=special_services.get(
                Option.freightcom_dangerous_goods_type
            ),
            serviceId=service,
            stackable=special_services.get(Option.freightcom_stackable),
            From=FromType(
                id=payload.shipper.id,
                company=payload.shipper.company_name,
                instructions=None,
                email=payload.shipper.email,
                attention=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                tailgateRequired=None,
                residential=payload.shipper.residential,
                address1=SF.concat_str(payload.shipper.address_line1, join=True),
                address2=SF.concat_str(payload.shipper.address_line2, join=True),
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code,
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
                address1=SF.concat_str(payload.recipient.address_line1, join=True),
                address2=SF.concat_str(payload.recipient.address_line2, join=True),
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code,
            ),
            COD=CODType(
                paymentType=PaymentType.recipient.value,
                CODReturnAddress=CODReturnAddressType(
                    codCompany=payload.recipient.company_name,
                    codName=payload.recipient.person_name,
                    codAddress1=SF.concat_str(payload.recipient.address_line1, join=True),
                    codCity=payload.recipient.city,
                    codStateCode=payload.recipient.state_code,
                    codZip=payload.recipient.postal_code,
                    codCountry=payload.recipient.country_code,
                ),
            )
            if options.cash_on_delivery is not None
            else None,
            Packages=PackagesType(
                Package=[
                    PackageType(
                        length=ceil(package.length.IN),
                        width=ceil(package.width.IN),
                        height=ceil(package.height.IN),
                        weight=ceil(package.weight.LB),
                        type_=packaging_type,
                        freightClass=freight_class,
                        nmfcCode=None,
                        insuranceAmount=None,
                        codAmount=None,
                        description=package.parcel.description,
                    )
                    for package in packages
                ],
                type_="Package",
            ),
            Payment=RequestPaymentType(type_=payment_type)
            if payload.payment is not None
            else None,
            Reference=[ReferenceType(name=payload.reference, code="parcelRef")]
            if payload.reference != ""
            else None,
            CustomsInvoice=CustomsInvoiceType(
                BillTo=BillToType(
                    company=payer.company_name,
                    name=payer.person_name,
                    address1=SF.concat_str(payer.address_line1, join=True),
                    city=payer.city,
                    state=payer.state_code,
                    zip=payer.postal_code,
                    country=payer.country_code,
                ),
                Contact=ContactType(name=payer.person_name, phone=payer.phone_number),
                Item=ItemType(
                    code=item.sku,
                    description=item.description,
                    originCountry=item.origin_country,
                    unitPrice=item.value_amount,
                ),
            )
            if payload.customs is not None and payer is not None
            else None,
        ),
    )

    return Serializable(request, standard_request_serializer)
