from typing import List, Tuple, cast
from freightcom_lib.shipping_request import (
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
from freightcom_lib.shipping_reply import (
    ShippingReplyType,
    QuoteType,
    SurchargeType,
)
from karrio.core.utils import Element, Serializable, XP, SF, NF
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    RateDetails,
    Message,
    ChargeDetails,
    Address,
)
from karrio.core.units import Packages, Options
from karrio.providers.freightcom.utils import (
    Settings,
    standard_request_serializer,
    ceil,
)
from karrio.providers.freightcom.units import (
    Service,
    FreightPackagingType,
    FreightClass,
    Option,
    PaymentType,
)
from karrio.providers.freightcom.error import parse_error_response


def parse_shipping_reply(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    shipping_node = XP.find("ShippingReply", response, first=True)
    shipment = (
        _extract_shipment(shipping_node, settings)
        if shipping_node is not None
        else None
    )

    return shipment, parse_error_response(response, settings)


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipping = XP.build(ShippingReplyType, node)
    quote: QuoteType = shipping.Quote

    tracking_number = getattr(
        next(iter(shipping.Package), None), "trackingNumber", None
    )
    rate_provider, service, service_name = Service.info(
        quote.serviceId, quote.carrierId, quote.serviceName, quote.carrierName
    )
    surcharges = [
        ChargeDetails(
            name=charge.name,
            currency=quote.currency,
            amount=NF.decimal(charge.amount),
        )
        for charge in cast(List[SurchargeType], quote.Surcharge)
    ]
    fuel_surcharge = (
        ChargeDetails(
            name="Fuel surcharge",
            currency=quote.currency,
            amount=NF.decimal(quote.fuelSurcharge),
        )
        if quote.fuelSurcharge is not None
        else None
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=shipping.Order.id,
        selected_rate=(
            RateDetails(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                service=service,
                currency=quote.currency,
                base_charge=NF.decimal(quote.baseCharge),
                total_charge=NF.decimal(quote.totalCharge),
                transit_days=quote.transitDays,
                extra_charges=([fuel_surcharge] + surcharges),
                meta=dict(rate_provider=rate_provider, service_name=service_name),
            )
            if quote is not None
            else None
        ),
        docs=Documents(label=shipping.Labels),
        meta=dict(
            rate_provider=rate_provider,
            service_name=service_name,
            tracking_url=shipping.TrackingURL,
        ),
    )


def shipping_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[Freightcom]:
    packages = Packages(
        payload.parcels, required=["weight", "height", "width", "length"]
    )
    options = Options(payload.options, Option)

    service = Service.map(payload.service).value_or_key
    packaging_type = FreightPackagingType[packages.package_type or "small_box"].value
    packaging = (
        "Pallet" if packaging_type in [FreightPackagingType.pallet.value] else "Package"
    )
    freight_class = next(
        (
            FreightClass[c].value
            for c in payload.options.keys()
            if c in FreightClass.__members__
        ),
        None,
    )
    payment_type = PaymentType[payload.payment.paid_by] if payload.payment else None
    item = next(
        iter(payload.customs.commodities if payload.customs is not None else []), None
    )
    payer: Address = (
        {
            PaymentType.sender: payload.shipper,
            PaymentType.recipient: payload.recipient,
            PaymentType.third_party: payload.recipient,
        }.get(PaymentType[payload.payment.paid_by])
        if payload.payment
        else None
    )

    request = Freightcom(
        username=settings.username,
        password=settings.password,
        version="3.1.0",
        ShippingRequest=ShippingRequestType(
            saturdayPickupRequired=options.freightcom_saturday_pickup_required,
            homelandSecurity=options.freightcom_homeland_security,
            pierCharge=None,
            exhibitionConventionSite=options.freightcom_exhibition_convention_site,
            militaryBaseDelivery=options.freightcom_military_base_delivery,
            customsIn_bondFreight=options.freightcom_customs_in_bond_freight,
            limitedAccess=options.freightcom_limited_access,
            excessLength=options.freightcom_excess_length,
            tailgatePickup=options.freightcom_tailgate_pickup,
            residentialPickup=options.freightcom_residential_pickup,
            crossBorderFee=None,
            notifyRecipient=options.freightcom_notify_recipient,
            singleShipment=options.freightcom_single_shipment,
            tailgateDelivery=options.freightcom_tailgate_delivery,
            residentialDelivery=options.freightcom_residential_delivery,
            insuranceType=(options.insurance is not None),
            scheduledShipDate=None,
            insideDelivery=options.freightcom_inside_delivery,
            isSaturdayService=options.freightcom_is_saturday_service,
            dangerousGoodsType=options.freightcom_dangerous_goods_type,
            serviceId=service,
            stackable=options.freightcom_stackable,
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
            COD=(
                CODType(
                    paymentType=PaymentType.recipient.value,
                    CODReturnAddress=CODReturnAddressType(
                        codCompany=payload.recipient.company_name,
                        codName=payload.recipient.person_name,
                        codAddress1=SF.concat_str(
                            payload.recipient.address_line1, join=True
                        ),
                        codCity=payload.recipient.city,
                        codStateCode=payload.recipient.state_code,
                        codZip=payload.recipient.postal_code,
                        codCountry=payload.recipient.country_code,
                    ),
                )
                if options.cash_on_delivery is not None
                else None
            ),
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
                type_=packaging,
            ),
            Payment=(
                RequestPaymentType(type_=payment_type)
                if payload.payment is not None
                else None
            ),
            Reference=(
                [ReferenceType(name="REF", code=payload.reference)]
                if payload.reference != ""
                else None
            ),
            CustomsInvoice=(
                CustomsInvoiceType(
                    BillTo=BillToType(
                        company=payer.company_name,
                        name=payer.person_name,
                        address1=SF.concat_str(payer.address_line1, join=True),
                        city=payer.city,
                        state=payer.state_code,
                        zip=payer.postal_code,
                        country=payer.country_code,
                    ),
                    Contact=ContactType(
                        name=payer.person_name, phone=payer.phone_number
                    ),
                    Item=ItemType(
                        code=item.sku,
                        description=item.description,
                        originCountry=item.origin_country,
                        unitPrice=item.value_amount,
                    ),
                )
                if all([payload.customs, payer])
                else None
            ),
        ),
    )

    return Serializable(request, standard_request_serializer)
