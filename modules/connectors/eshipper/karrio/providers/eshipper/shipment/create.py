import karrio.schemas.eshipper.shipping_request as eshipper
import karrio.schemas.eshipper.shipping_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.eshipper.error as error
import karrio.providers.eshipper.utils as provider_utils
import karrio.providers.eshipper.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if "order" in response else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponseType, data)
    label = shipment.labelData.label.data
    trackingNumbers = [_.trackingNumber for _ in shipment.packages]
    # invoice = ""

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.order.orderId,
        label_type="PDF",
        docs=models.Documents(
            label=label,
            # invoice=invoice,
        ),
        meta=dict(
            carrier_tracking_link=shipment.trackingUrl,
            service_name=shipment.carrier.serviceName,
            tracking_numbers=trackingNumbers,
            trackingId=shipment.order.trackingId,
            orderId=shipment.order.orderId,
            carrierName=shipment.carrier.carrierName,
            transactionId=shipment.transactionId,
            billingReference=shipment.billingReference,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )

    request = eshipper.ShippingRequestType(
        scheduledShipDate=lib.fdate(options.shipment_date),
        shippingrequestfrom=eshipper.FromType(
            attention=shipper.contact,
            company=shipper.company_name,
            address1=shipper.address_line1,
            address2=shipper.address_line2,
            city=shipper.city,
            province=shipper.state_code,
            country=shipper.country_code,
            zip=shipper.postal_code,
            email=shipper.email_address,
            phone=shipper.phone_number,
            instructions=None,
            residential=shipper.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        to=eshipper.FromType(
            attention=recipient.contact,
            company=recipient.company_name,
            address1=recipient.address_line1,
            address2=recipient.address_line2,
            city=recipient.city,
            province=recipient.state_code,
            country=recipient.country_code,
            zip=recipient.postal_code,
            email=recipient.email_address,
            phone=recipient.phone_number,
            instructions=None,
            residential=recipient.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        packagingUnit=provider_units.PackageType.map(packages.package_type).value,
        packages=eshipper.PackagesType(
            type=None,
            packages=[
                eshipper.PackageType(
                    height=package.height.CM,
                    length=package.length.CM,
                    width=package.width.CM,
                    weight=package.weight.KG,
                    dimensionUnit=units.DimensionUnit.CM.value,
                    weight=package.weight.KG,
                    weightUnit=units.WeightUnit.KG.value,
                    type=provider_units.PackageType.map(package.package_type).value,
                    freightClass=None,
                    nmfcCode=None,
                    insuranceAmount=None,
                    codAmount=None,
                    description=package.description,
                    harmonizedCode=None,
                    skuCode=None,
                )
                for package in packages
            ],
        ),
        reference1=payload.reference,
        reference2=None,
        reference3=None,
        transactionId=None,
        signatureRequired=options.eshipper_signature_required.state,
        insuranceType=None,
        dangerousGoodsType=None,
        pickup=None,
        customsInformation=None,
        cod=None,
        isSaturdayService=options.eshipper_is_saturday_service.state,
        holdForPickupRequired=options.eshipper_hold_for_pickup_required.state,
        specialEquipment=options.eshipper_special_equipment.state,
        insideDelivery=options.eshipper_inside_delivery.state,
        deliveryAppointment=options.eshipper_delivery_appointment.state,
        insidePickup=options.eshipper_inside_pickup.state,
        saturdayPickupRequired=options.eshipper_saturday_pickup_required.state,
        stackable=options.eshipper_stackable.state,
        serviceId=service,
        thirdPartyBilling=None,
        commodityType=None,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(lib.to_json(_).replace("shippingrequestfrom", "from")),
    )
